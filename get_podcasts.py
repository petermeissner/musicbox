#! /usr/bin/env python3

import getpodcast
import datetime
import os
import time
import sys

# get date from 7 days ago as iso format
seven_days_ago = str(datetime.datetime.now() - datetime.timedelta(days=7))[0:10]

opt = getpodcast.options(
    date_from=seven_days_ago,
    root_dir='./music/Aaa_Podcast')

podcasts = {
    "Mikado": "https://www.ndr.de/nachrichten/info/sendungen/mikado/mikado_am_morgen/podcast4223.xml",
    "Kakadu": "https://www.kakadu.de/kakadu-104.xml",
    "CheckPod": "https://feeds.br.de/checkpod-der-podcast-mit-checker-tobi/feed.xml"

}

getpodcast.getpodcast(podcasts, opt)


# go through directory music/podcast and keep only files from the last 7 days
def list_dir_recursive(path: str):
    """
    Goes through folder and lists all its files. 

    Args:
        path (str): path to look for files

    Returns:
        List[str]: a list of file paths
    """
    res = []
    for currentpath, folders, files in os.walk(path):
        for file in files:
            res.append(os.path.join(currentpath, file))
    return res

# remove all files older than 7 days
def remove_old_files(path: str):
    """
    Removes all files older than 7 days.

    Args:
        path (str): path to look for files
    """
    now = datetime.datetime.now()
    for file in list_dir_recursive(path):
        if os.path.getmtime(file) < (now - datetime.timedelta(days=7)).timestamp():
            os.remove(file)
            print(f"Removed {file}")
    else:
        print("No old files found")
        print("Removed old files")
    return


# remove old files from music/Aaa_Podcast
remove_old_files('./music/Aaa_Podcast')