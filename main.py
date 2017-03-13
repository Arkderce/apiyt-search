#!/usr/bin/python
import time
import webbrowser
import notifier
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser


# Compare new list with old one
# If any newer date appeared, return new list, else return false
def check_new(namesList):
    try:
        newList = youtube_search(args)
        if namesList[1] < newList[1]:
            return newList
        else:
            return False
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

def open_browser(url):
    new = 2 # open in a new tab, if possible
    webbrowser.open(url,new=new)

# Notify user that new video appeared
def notify_user(namesList, browserarg):
    titleofvideo = namesList[0].encode('utf-8')
    notifier.ballun("Newest video", str(titleofvideo))     #Invoke notification on desktop
    if browserarg.open_browser != False: #Open browser after notification period if user asked for that
        open_browser(str(namesList[2]))

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

    videos = []
  # Add each result to dictionary
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result["snippet"]["title"])
            videos.append(search_result["snippet"]["publishedAt"])
            videos.append("https://www.youtube.com/watch?v=" + str(search_result["id"]["videoId"]))
    return videos


if __name__ == "__main__":
  # Set arguments for search
    argparser.add_argument("--q", help="Search term", default="music")
    argparser.add_argument("--max-results", help="Max results", default=1)
    argparser.add_argument("--order", help="Order", default="date")
  # Set arguments for other functions
    argparser.add_argument("--open-browser", help="Open browser", default=False)
    args = argparser.parse_args()

    try:
        namesList = youtube_search(args)
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
    notify_user(namesList, args)

  # Silently check if new video appeared
    while True:
        time.sleep(60.0)
        value = check_new(namesList)
        if value != False:
            namesList = value
            notify_user(namesList, args)
