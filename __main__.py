import praw
import os
import sys
import re
import datetime
import argparse

from tqdm import tqdm

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

######## Reddit api #########
#############################

def reddit_service(user = 'scraper', user_agent = 'subreddit-playlist/0.1 by /u/safturento'):
	reddit = praw.Reddit(user, user_agent=user_agent)
	reddit.read_only = True
	return reddit


def youtube_link(url):
	youtube_regex = '^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'
	result = re.match(youtube_regex, url)
	if result:
		return result.groups()[4]
	return False

def get_youtube_posts(reddit, subreddit = 'youtubehaiku', time='month', count = 100):
	posts = []
	for post in reddit.subreddit(subreddit).top(time, limit=100):
		video_id = youtube_link(post.url)
		if video_id:
			posts.append(video_id)
	return posts

######## Youtube api ########
#############################
root = os.path.dirname(os.path.abspath(__file__))
def youtube_service(client_secret = os.path.join(root, 'client_secret.json'), api_service = 'youtube', api_version = 'v3',
							scope = 'https://www.googleapis.com/auth/youtube'):	
	flow = flow_from_clientsecrets(client_secret, scope=scope)
	storage = Storage(os.path.join(root, 'oauth2.json'))
	credentials = storage.get()
	if credentials is None or credentials.invalid:
		credentials = run_flow(flow, storage)
	
	return build(api_service, api_version, http=credentials.authorize(httplib2.Http()))

def get_playlist(youtube, subreddit, time):
	try:
		
		title = f'{subreddit} top-{time} [{datetime.datetime.today().strftime("%y-%m-%d")}]'

		my_playlists = youtube.playlists().list(
			part = 'snippet',mine = True).execute()

		for playlist in my_playlists['items']:
			if playlist['snippet']['title'] == title:
				print(f'playlist {title} already found.')
				return playlist

		return youtube.playlists().insert(
			part = 'snippet,status',
			body = dict(
				snippet = dict(
					title = title,
					description = ''
				),
				status=dict(
					privacyStatus='public'
				)
			)
		).execute()
	except HttpError as e:
		print(f'An HTTP error {e.resp.status} occurred:\n {e.content}')
			
def populate_playlist(youtube, playlist, video_ids):
	for video_id in tqdm(video_ids):
		try:
			youtube.playlistItems().insert(
				part = 'snippet',
				body = dict(
					snippet = dict(
						playlistId = playlist['id'],
						resourceId = dict(
							kind = 'youtube#video',
							videoId = video_id
						)
					)
				)
			).execute()
		except HttpError as e:
			if e.resp.status == 404:
				tqdm.write(f'{e.resp.status}: video not found, skipping video.')
			elif e.resp.status == 403:
				tqdm.write(f'{e.resp.status}: insufficient permissions, skipping video.')
			else:
				tqdm.write(f'An HTTP error {e.resp.status} occurred:\n {e.content}')
	
	print('https://www.youtube.com/playlist?list=' + playlist['id'])

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'Generate a youtube playlist from a chosen subreddit')
	parser.add_argument('subreddit', nargs='?', default='youtubehaiku',
		help = 'Which subreddit(s) to scrape (default=%(default)s)')
	parser.add_argument('time', nargs='?', default='month',
		help = 'Which sort timeline to use: all, day, hour, month, week, year (default=%(default)s)')
	parser.add_argument('count', nargs='?', default=100, type=int,
		help = 'How many subreddit entries to scrape (default=%(default)s)')
	args = parser.parse_args()

	'''This try-except combined with a gitignore ensures that this is only ever loaded
		locally if the user creates a file named isdev.py in the root directory.
		This file will never be pushed to github so you cannot accidentally have it.'''
	# try:
	# 	import isdev
	# 	os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
	# except: pass
	

	# youtube = youtube_service()
	# reddit = reddit_service()

	# video_ids = get_youtube_posts(reddit, args.subreddit, args.time, args.count)

	# playlist = get_playlist(youtube, args.subreddit, args.time)
	# populate_playlist(youtube, playlist, video_ids)