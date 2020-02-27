from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    creds = None
    
    token_path = 'token.pickle' #created after


    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # I save the picture in root
    file_metadata = {'name': 'processed.jpeg'}

    # if you want to save the picture in folder
    # file_metadata = {'name': '111sample.pdf',
    #                  'parents': ['1OPKOAFatLfHakCZfPPuZ3sF3CzHv8NCO']}
    
    media = MediaFileUpload(os.path.abspath(
        "processed.jpeg"), mimetype='Image/jpeg')
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

if __name__ == '__main__':
    main()