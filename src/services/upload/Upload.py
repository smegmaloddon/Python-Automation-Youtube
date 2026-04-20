# imports
from pathlib import Path
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# user imports
from src.utils.data import Configuration, Temporary
from src.utils.io import JSON

# functions
def __Fetch(
) -> any:
    
    # fetch oauth & verify
    oauth : dict = JSON.Read(
        path=Configuration.DATA /'oauth.json'
    ).get(
        Temporary.Channel, None
    )
    if not oauth:

        return None

    creds = Credentials(
        token=oauth["token"],
        refresh_token=oauth["refresh_token"],
        token_uri=oauth["token_uri"],
        client_id=oauth["client_id"],
        client_secret=oauth["client_secret"],
        scopes=oauth["scopes"]
    )

    youtube = build("youtube", "v3", credentials=creds)
    return youtube

def Upload(
    title : str = None,
    description : str = None
) -> None:
    
    # verify parameters
    assert title is not None and description is not None

    # fetch credentials
    youtube : build = __Fetch()
    if not youtube:

        return

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(
            str(
                Configuration.TEMPORARY /'video.mp4'
            ),
            resumable=True
        )
    )

    response = request.execute()
    print(response)