import os
from googleapiclient.discovery import build
from isodate import parse_duration
from youtube_transcript_api import YouTubeTranscriptApi

# Set up the API key and build the YouTube Data API client
api_key = "api"  # Replace with your own API key
youtube = build('youtube', 'v3', developerKey=api_key)

def search_videos(query):
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        videoCaption='closedCaption',
        order='relevance',
        safeSearch='none'
    )
    response = request.execute()

    for item in response['items']:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        video_url = f"https://www.youtube.com/watch?v={video_id}"        
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        match = False
        for element in transcript_list:
            transcript = element.fetch()
            for text in transcript:   
                string = text['text']
                if query.lower() in string.lower():
                    match = True

        video_response = youtube.videos().list(
            part='contentDetails',
            id=video_id
        ).execute()
        duration = video_response['items'][0]['contentDetails']['duration']
        video_duration = parse_duration(duration).total_seconds()

        video_description = item['snippet']['description']

        if video_duration > 30 and not is_educational(video_description) and not has_educational_title(video_title) and match == True:
            print(f"Title: {video_title}")
            print(f"URL: {video_url}")
            print()

def is_educational(description):
    educational_patterns = ['how to', 'learn', 'guide', 'lesson','news','weather update','weather updates','alert','kids','music','music video','offcial music video','lyrics','song']

    if any(pattern in description.lower() for pattern in educational_patterns):
        return True

    return False

def has_educational_title(title):
    educational_keywords = ['tutorial', 'lecture', 'educational', 'informational','news','weather update','weather updates','alert','kids','offical music video','official video','lyrics']

    if any(keyword in title.lower() for keyword in educational_keywords):
        return True

    return False

query = input("Enter your query: ")
search_videos(query)
