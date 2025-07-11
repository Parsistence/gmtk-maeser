# How to Use These Tools

These tools will allow you to pull the transcripts of each video essay from the Gamemaker's Toolkit Series and create a vectorstore for use with the chatbot. The procedure involves 3 main steps:

1. [**Download the playlist page as an html file**](#download-the-playlist-page-as-an-html-file).
2. [**Get the video transcripts**](#get-the-video-transcripts) using [`get_transcripts/get_ids_from_playlist_html.py`](./get_transcripts/get_ids_from_playlist_html.py).
3. [**Vectorize the video transcripts**](#vectorize-the-video-transcripts) using [`make_gmtk_vectorstore/make_vectorstore.py`](./make_gmtk_vectorstore/make_vectorstore.py).

## Prerequisite Requirements
Before using these tools, make sure to install the required libraries using [`GMTK/requirements/requirements_tools.txt`](./../requirements/requirements_tools.txt).

## Download the Playlist Page as an HTML File

Navigate to [https://www.youtube.com/playlist?list=PLc38fcMFcV_s7Lf6xbeRfWYRt7-Vmi_X9](https://www.youtube.com/playlist?list=PLc38fcMFcV_s7Lf6xbeRfWYRt7-Vmi_X9) (the GTMK playlist) and **scroll all the way down** until all videos in the playlist are loaded. You may need to do this a couple of times before you make it to the bottom of the list.

Once the page is fully loaded, **save the page** (using `Ctrl+S` in most browsers) to `get_transcripts/` as `playlist.html`.

---

## Get the Video Transcripts

Once you have `playlist.html` in the `get_transcripts/` directory, create a `transcripts/` folder in the same directory and run [`get_ids_from_playlist_html.py`](./get_transcripts/get_ids_from_playlist_html.py). The script will fetch the transcript for each video and save it into `transcripts/`.

> **Note:** `get_ids_from_playlist_html.py` uses [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) to fetch video transcripts, but YouTube has been changing its requirements recently for fetching data from its API, so it is possible that this api may break. If this happens, a separate implementation of `get_transcript_text` has been implemented with the [yt-dlp](https://pypi.org/project/yt-dlp/) library. It's slower, but it's more reliable. You can switch between the youtube-transcript-api and yt-dlp library by replacing `from get_yt_transcript` (in the `get_ids_from_playlist_html.py` script) with `from get_yt_transcript_yt_dlp` or vice versa.

---

## Vectorize the Video Transcripts

Once all video transcripts have been saved into the `transcripts/` folder, move `transcripts/` into `tools/make_gmtk_vectorstore` and run [make_vectorstore.py](./make_gmtk_vectorstore/make_vectorstore.py). The script will create a new folder named `gmtk/` and will save the vectorstore into this directory. Once this is generated, move `gmtk/` into `GMTK/vectorstores`, and you are all set!
