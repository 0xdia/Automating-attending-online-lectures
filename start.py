#!/usr/bin/env python3

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
          'https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar'
         ]

#def is_currently_happening(event):

def start():
  creds = None   
  
  if os.path.exists('token.pickle'):  
    creds = pickle.load(open('token.pickle', 'rb'))

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        SCOPES
      )
     
      creds = flow.run_local_server(port=0)

    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)
  
  service = build('calendar', 'v3', credentials=creds)

  now = datetime.datetime.utcnow().isoformat() + 'Z'

  events_result = service.events().list(
                            calendarId='primary',
                            timeMin=now,
                            maxResults=4,
                            singleEvents=True,
                            orderBy='startTime'
                          ).execute()

  events = events_result.get('items', [])

  os.system(f"firefox {events[0]['hangoutLink']}")

  """
  for event in events:
    if is_currently_happening(event):
      os.system(f'firefox {event["hangoutLink"]}') 
      break
  """ 

if __name__=='__main__':
  start()
