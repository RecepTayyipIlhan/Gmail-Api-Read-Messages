import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import email
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
label_id1='inbox'
label_id2='unread'

def get_message(service,user_id,msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,format='raw').execute()
        msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        msg_str = email.message_from_bytes(msg_raw)
        content_types = msg_str.get_content_maintype()
        if content_types == 'multipart':
            #part 1 is plain text part 2 is html text
            part1, part2 = msg_str.get_payload()
            return part1
        else:
            return msg_str.get_payload()
    except HttpError as err:
        print("An error occured: %s") # % err




#Search_string ile arama kutusundaki stringleri döndürür.
def search_message(service,user_id,search_string):
    try:
        search_id = service.users().messages().list(userId=user_id, q=search_string ).execute()
        number_results = search_id['resultSizeEstimate']

        final_list = []

        if number_results > 0:
            message_ids=search_id['messages']
            for ids in message_ids :
                final_list.append(ids['id'])
            return final_list
        else :
            print('There is no result returning empty string')
            return ""



    except HttpError as err:
        print("An error occured: %s") # % err





def get_service():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    service = build('gmail', 'v1', credentials=creds)
    return  service

if __name__ == "__main__":
    service=get_service()
    search_string="muratgilindami"
    message=search_message(service,'me',search_string)
    for mes in message:
        print(get_message(service,'me',mes))
   # print(message)
