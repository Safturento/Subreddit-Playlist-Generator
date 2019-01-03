# Subreddit Playlist Generator
This script scrapes a given subreddit (can scrape any sort method and timeline) for youtube videos and then creates a youtube playlist with the results. The default parameters scrape [r/youtubehaiku](http://reddit.com/r/youtubehaiku)'s top 100 posts sorted by top of the month. In order to make use of this script you must access the reddit and youtube apis.

## Reddit api access
To gain access to the reddit api go to the [reddit apps page](https://www.reddit.com/prefs/apps/) and create a new app. Select script and name it whatever you wish. Once created you will be given a client id (alphanumeric string under the name you gave to your app) and a client secret (click edit if you do not see it). With this information create a file named `praw.ini` in this project's directory with the lines shown below, filling in with your information.

<b>DO NOT SHARE THIS FILE WITH ANYONE.</b>
```ini
[scraper]
username=
password=
client_id=
client_secret=
```

## Youtube api access
To access the youtube api go to [google's developer console](https://console.developers.google.com/apis) and create a new project (name it whatever you wish). Once you're on the new project dashboard click `ENABLE APIS AND SERVICES`, then search for and add the `YouTube Data API v3` service. Then click on Credentials and create credentials for `OAuth client ID`. Once done with this process you will be given the option to download a json file with your client secret information. rename the downloaded file to `client_secret.json` and place it in the project's root directory.

## Usage
To have it generate a playlist with the defaults ([r/youtubehaiku](http://reddit.com/r/youtubehaiku), top-month) just go into the root directory and type `python .`. To change these parameters you can modify the `get_youtube_posts` call in the __main__ block of __main__.py. The optional parameters are:
* subreddit (__str__) - the name of the subreddit to scrape
* count (__int__) - how many posts to scrape
* time (__str__) - timeline to sort by

## Future additions
* Add progress bar when populating playlist
* Move optional parameters to cli args
* Add setup.py so script can be ran from anywhere