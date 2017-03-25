#!/usr/bin/python
import time
from subprocess import call
import webbrowser
import notifier
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

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
            videos['title'] = search_result["snippet"]["title"]
            videos['publishedAt'] = search_result["snippet"]["publishedAt"]
            videos['videoId'] = "https://www.youtube.com/watch?v=" + str(search_result["id"]["videoId"])
    return videos

# Compare new dictionary with old one
# If any newer date appeared, return new dictionary, else return false
def check_new(namesDict):
    try:
        newNamesDict = youtube_search(args)
        if namesDict['publishedAt'] < newNamesDict['publishedAt']:
            return newNamesDict
        else:
            return False
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

def open_browser(url):
    new = 2 # open in a new tab, if possible
    webbrowser.open(url, new=new)

# Notify user that new video appeared
def notify_user(namesDict, browserarg):
    titleofvideo = namesDict['title'].encode('utf-8')
    notifier.ballun("Newest video", str(titleofvideo))     #Invoke notification on desktop
    if browserarg.open_browser != False: #Open browser after notification period if user asked for that
        open_browser(str(namesDict['videoId']))

def download_video(namesDict):
    invokeLink = str(namesDict['videoId'])
    call("youtube-dl" + " " + invokeLink)

if __name__ == "__main__":
  # Set arguments for search
    argparser.add_argument("--q", help="Search term", default="music")
    argparser.add_argument("--max-results", help="Max results", default=1)
    argparser.add_argument("--order", help="Order", default="date")
  # Set arguments for other functions
    argparser.add_argument("--open-browser", help="Open browser", default=False)
    argparser.add_argument("--dl-video", help="Download video", default=False)
    args = argparser.parse_args()

    try:
        namesDict = youtube_search(args)
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
    notify_user(namesDict, args)
    if args.dl_video != False:
        download_video(namesDict)

  # Silently check if new video appeared
    while True:
        time.sleep(60.0)
        newNamesDict = check_new(namesDict)
        if newNamesDict != False:
            namesDict = newNamesDict
            notify_user(namesDict, args)
            if args.dl_video != False:
                download_video(namesDict)

