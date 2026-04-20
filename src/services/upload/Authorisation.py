# imports
from google_auth_oauthlib.flow import InstalledAppFlow
import json, time
from pathlib import Path
import json

from src.utils.data import Configuration, Temporary
from src.utils.io import JSON

# constants
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload'
]

def Fetch(
) -> dict:
    
    # init file
    file : Path = Configuration.TEMPORARY /'secrets.json'
    
    # get controller
    controller = InstalledAppFlow.from_client_secrets_file(
        file,
        SCOPES
    )

    # fetch credentials
    credentials = controller.run_local_server(
        port=0
    )

    return json.loads(
        credentials.to_json()
    )

def __Temporary(
    secrets : dict
) -> None:
    
    # save secrets to temp file
    JSON.Write(
        path=Configuration.TEMPORARY /'secrets.json',
        contents=secrets
    )

def Run(
) -> None:
    
    # load secrets .json5
    secrets : dict = JSON.Read(
        path=Configuration.DATA /'secrets.json'
    )

    # load oauths .json5
    oauths : dict = JSON.Read(
        path=Configuration.DATA /'oauth.json'
    )

    # process all oauths
    for unique, package in secrets.items():

        # already processed
        if unique in oauths:

            continue

        __Temporary(
            secrets=package
        )

        # fetch oauth
        credentials : dict = Fetch()

        # append oauth to key | item
        oauths[unique] = credentials

    # save updated oauths.json
    JSON.Write(
        path=Configuration.DATA /'oauth.json',
        contents=oauths
    )


        