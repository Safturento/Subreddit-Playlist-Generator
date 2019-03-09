# Subreddit Playlist Generator
This script scrapes a given subreddit (can scrape any sort method and timeline) for youtube videos and then creates a youtube playlist with the results. The default parameters scrape [r/youtubehaiku](http://reddit.com/r/youtubehaiku)'s top 100 posts sorted by top of the month. In order to make use of this script you must access the reddit and youtube apis.

## Installation
To install clone the repository and then cd to it. Then run the following to install all required modules
```
pip install -r requirements.txt
pip install --upgrade google-api-python-client oauth2client
```
The second line solves an issue with importing `oauth2client.client` [(source)](https://stackoverflow.com/a/48921881)
Once that's done all that's left is to setup your and reddit and youtube api access.

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
Navigate into the directory of the application and type ```python . -h``` to view all optional commands and defaults.
```
$python . -h
usage: . [-h] [subreddit] [time] [count]

Generate a youtube playlist from a chosen subreddit

positional arguments:
  subreddit   Which subreddit(s) to scrape (default=youtubehaiku)
  time        Which sort timeline to use: all, day, hour, month, week, year
              (default=month)
  count       How many subreddit entries to scrape (default=100)

optional arguments:
  -h, --help  show this help message and exit
  ```


## Future additions
[x] Add progress bar when populating playlist

[x] Move optional parameters to cli args

[ ] Add setup.py so script can be ran from anywhere