import random
import string
import os
import math
import sys
from tkinter import filedialog
from tkinter import *


from TikTokApi import TikTokApi
from datetime import date, datetime, time, timedelta
from pregex.quantifiers import AtMost, AtLeastOnce
from pregex.classes import AnyDigit
from collections import OrderedDict


from moviepy.editor import VideoFileClip, concatenate_videoclips

def get_video_bytes(api, tiktok_video_id):
    video = api.video(id=tiktok_video_id)
    return video.bytes()

def generate_random_file_name(lowercase = True):
    strings_choices = string.ascii_lowercase if lowercase == True else string.ascii_uppercase
    date_today = datetime.today().strftime("%Y-%m-%d")
    # random_string = ''.join(random.choices(strings_choices + string.digits, k=12))
    return f"{date_today}_{random_string}"
    
def download_video(video_data, file_name):
    path = r".\downloaded_tiktoks"
    with open(f"{path}\{file_name}.mp4", "wb") as out_file:
        out_file.write(video_data)

def extract_tiktok_video_id(url):
    pre = (
    "/"
    + AtLeastOnce(AnyDigit())
    + AtMost("?", 1)
    )
    return pre.get_matches(url)[0].translate(str.maketrans({"?": "", "/": ""}))

# LINKS = [
#     "https://www.tiktok.com/@fahrlehrerlukas/video/7125693944792452357?is_copy_url=1&is_from_webapp=v1",
#     "https://www.tiktok.com/@thenathannazareth/video/7109518118409522437?is_copy_url=1&is_from_webapp=v1&q=dropshipping&t=1659527587217",
#     "https://www.tiktok.com/@sergioramos/video/7115526674866801925?is_copy_url=1&is_from_webapp=v1",
#     "https://www.tiktok.com/@77_shumnyy_77/video/7108078504880688385?is_copy_url=1&is_from_webapp=v1",
#     "https://www.tiktok.com/@clever_fit_muenster/video/7114345756215020806?is_copy_url=1&is_from_webapp=v1",
#     "https://www.tiktok.com/@boneym.official/video/7068624584412581125?is_copy_url=1&is_from_webapp=v1",
#     "https://www.tiktok.com/@bundesliga/video/7123953974834744581?is_copy_url=1&is_from_webapp=v1&lang=de-DE",
#     "https://www.tiktok.com/@stardust_games/video/7126817418818768133?is_copy_url=1&is_from_webapp=v1&lang=de-DE"
# ]

def main():
    LINKS = inputtxt.get(1.0, "end-1c")
    LINKS = LINKS.split("\n")
    print(LINKS)
    url_file_name_map = OrderedDict()

    with TikTokApi() as api:
        for i, url in enumerate(LINKS):
            id = extract_tiktok_video_id(url)
            video_data = get_video_bytes(api, id)
            download_video(video_data, i)

            url_file_name_map[f"{i}.mp4"] = [url]

    L =[]
    for root, dirs, files in os.walk(r".\downloaded_tiktoks"):
        for i, file in enumerate(files):
            if os.path.splitext(file)[1] == '.mp4':
                filePath = os.path.join(root, file)
                video = VideoFileClip(filePath)
                url_file_name_map[file].append(video.duration)
                L.append(video)

    final_clip = concatenate_videoclips(L, method = "compose")
    print(DOWNLOAD_PATH)
    print(os.path.join(gui_win.DOWNLOAD_PATH, 'final_output.mp4'))
    final_clip.to_videofile(f"{os.path.join(gui_win.DOWNLOAD_PATH, 'final_output.mp4')}", fps = 128)

    lines = []
    start_time = time(0, 0)
    with open(f"{os.path.join(gui_win.DOWNLOAD_PATH, 'timestamp.txt')}", 'a') as f:
        for key, value in url_file_name_map.items():
            duration = math.floor(value[1])
            start_time = datetime.combine(date.today(), start_time) + timedelta(seconds=duration)
            start_time = start_time.time()
            lines.append(f"{value[0]} / {start_time}\n")

        f.writelines(lines)

DOWNLOAD_PATH = ""
LINKS = ""

gui_win = Tk()
gui_win.geometry('400x400')
gui_win.grid_rowconfigure(0, weight = 1)
gui_win.grid_columnconfigure(0, weight = 1)

inputtxt = Text(gui_win,
                   height = 30,
                   width = 50)

inputtxt.pack()

def get_download_directory():
    gui_win.DOWNLOAD_PATH=filedialog.askdirectory(title="Dialog box")
    print(DOWNLOAD_PATH)

dialog_btn = Button(gui_win, text='Wähle einen Speicherort aus', command = get_download_directory)
dialog_btn.pack()

download_btn = Button(gui_win, text='dwnld', command = main)

download_btn.pack()

gui_win.mainloop()