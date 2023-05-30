import os
import pickle

from google.auth.transport import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from src import gmail_rule_runner

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    "https://www.googleapis.com/auth/gmail.modify"
]


def set_token():
    """
    The get_token function checks to see if a token file exists. If it does, the function opens the file and loads
    the credentials into memory. The function then returns those credentials.

    :return: A creds object
    :doc-author: prabhakarant
    """
    secrets_file= gmail_rule_runner.secrets_path
    if os.path.exists(secrets_file):
        with open(secrets_file, 'rb') as token_file:
            creds = pickle.load(token_file)
            return creds


def get_token():
    """
    The set_token function is used to set the token for the Google API.
        It first checks if there is a token already, and if so, it checks whether or not that token has expired.
        If it has expired, then we refresh the token using our refresh_token (which was generated when we created our credentials).
        If there isn't a valid existing token, then we create one by running an InstalledAppFlow from client secrets file 'credentials.json' with SCOPES as defined above.  We run this flow locally on port 0 (a random port).  Then we save this new access_

    :return: An object of type credentials
    :doc-author: prabhakarant
    """
    token = set_token()
    if not token:
        if token and token.expired and token.refresh_token:
            token.refresh(Request())
        else:
            creds_file= gmail_rule_runner.credentials_path
            flow = InstalledAppFlow.from_client_secrets_file(creds_file, SCOPES)
            token = flow.run_local_server(port=0)
        secrets_file= gmail_rule_runner.secrets_path
        with open(secrets_file, 'wb') as token_file:
            pickle.dump(token, token_file)
    return token
