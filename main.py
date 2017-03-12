#!/usr/bin/python
import time
import notifier
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


# Compare new dictionary with old one
# If any newer date appeared, return new dictionary, else return false
# Notify user that new video appeared
def check_new(namesDict):
    try:
        newDict = youtube_search(args)
        if namesDict < newDict:
            for key, value in newDict.iteritems():
                titleofvideo = key.encode('utf-8')
           #Invoke notification
            notifier.ballun("Newest video", str(titleofvideo))
            return newDict
        else:
            return False
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "YOUR DEVELOPER KEY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results,
        order=options.order,
    ).execute()

    videos = {}
  # Add each result to dictionary
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos[search_result["snippet"]["title"]] = search_result["snippet"]["publishedAt"]
    return videos


if __name__ == "__main__":
  # Set arguments for search
    argparser.add_argument("--q", help="Search term", default="music")
    argparser.add_argument("--max-results", help="Max results", default=1)
    argparser.add_argument("--order", help="Order", default="date")
    args = argparser.parse_args()
    try:
        namesDict = youtube_search(args)
        for key, value in namesDict.iteritems():
            titleofvideo = key.encode('utf-8')
       #Invoke notification
        notifier.ballun("Newest video", str(titleofvideo))
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

  # Silently check if new video appeared
    while True:
        time.sleep(60.0)
        value = check_new(namesDict)
        if value != False:
            namesDict = value
