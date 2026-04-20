# imports
import warnings

warnings.filterwarnings(
    action='ignore',
    category=FutureWarning
)

import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from json import JSONDecodeError
import uuid
import json
import time 

# user imports
from src.utils.data import Configuration, Temporary

MODELS : list = [
    'gemini-2.5-flash',
    'gemini-2.5-flash-preview-09-2025',
    'gemini-2.5-flash-lite',
    'gemini-2.5-flash-lite-preview-09-2025',
    'gemini-2.0-flash',
    'gemini-2.0-flash-lite',
    'gemini-flash-latest'
]
TIMEOUT : int = 32

def Cleanse(
    text : str
) -> str:
    
    text = text.strip()
    if text.startswith(
        "```json"
    ):
        text = text[
            len("```json"):
        ].strip()

    if text.startswith(
        "```"
    ):
        
        text = text[
            3:
        ].strip()

    if text.endswith(
        "```"
    ):
        
        text = text[
            :-3
        ].strip()

    return text

def Create(
    prompt : str = None
) -> None:
    
    # verify
    assert prompt is not None
    
    # init variables
    response : str = None
    number = 0          
    key = 0 

    # configure            
    genai.configure(
        api_key=Configuration.ARTIFICIAL[key]
    )

    while True:
        try:
            model = genai.GenerativeModel(
                model_name=MODELS[number]
            )

            response: str = model.generate_content(
                contents=prompt
            )
            break  # ✅ SUCCESS

        except ResourceExhausted:
            
            print(
                'warn : resource-limited'
            )

            number += 1  # try next model

            # ❗ all models exhausted → rotate key
            if number >= len(MODELS):
                number = 0
                key += 1

                # ❌ no more keys
                if key >= len(Configuration.ARTIFICIAL):
                    raise RuntimeError("All Gemini keys exhausted")

                # ✅ configure next key
                genai.configure(
                    api_key=Configuration.ARTIFICIAL[key]
                )
            
    text : str = Cleanse(
        text=response.text
    )
    try:

        dictionary : json = json.loads(
            text
        )
        return dictionary
    except JSONDecodeError:

        print(
            'error : jsondecode'
        )
        return {}