import random
import string
import os

from TikTokApi import TikTokApi
from datetime import datetime
from pregex.quantifiers import AtMost, AtLeastOnce
from pregex.classes import AnyDigit

from moviepy.editor import VideoFileClip, concatenate_videoclips


def get_video_bytes(api, tiktok_video_id):
    video = api.video(id=tiktok_video_id)
    return video.bytes()

def generate_random_file_name(lowercase = True):
    strings_choices = string.ascii_lowercase if lowercase == True else string.ascii_uppercase
    date_today = datetime.today().strftime("%Y-%m-%d")
    random_string = ''.join(random.choices(strings_choices + string.digits, k=12))
    return f"{date_today}_{random_string}"
    
def download_video(video_data, file_name):
    with open(f"{file_name}.mp4", "wb") as out_file:
        out_file.write(video_data)

def extract_tiktok_video_id(url):
    pre = (
    "/"
    + AtLeastOnce(AnyDigit())
    + AtMost("?", 1)
    )
    return pre.get_matches(url)[0].translate(str.maketrans({"?": "", "/": ""}))

# url_list = [
#     "https://www.tiktok.com/@fahrlehrerlukas/video/7125693944792452357?is_copy_url=1&is_from_webapp=v1",
#     "https://www.tiktok.com/@thenathannazareth/video/7109518118409522437?is_copy_url=1&is_from_webapp=v1&q=dropshipping&t=1659527587217",
#     "https://www.tiktok.com/@sergioramos/video/7115526674866801925?is_copy_url=1&is_from_webapp=v1",
#     "https://www.tiktok.com/@77_shumnyy_77/video/7108078504880688385?is_copy_url=1&is_from_webapp=v1"
# ]

url_dict = {
    "https://www.tiktok.com/@fahrlehrerlukas/video/7125693944792452357?is_copy_url=1&is_from_webapp=v1": 0,
    "https://www.tiktok.com/@thenathannazareth/video/7109518118409522437?is_copy_url=1&is_from_webapp=v1&q=dropshipping&t=1659527587217": 0,
    "https://www.tiktok.com/@sergioramos/video/7115526674866801925?is_copy_url=1&is_from_webapp=v1": 0,
    "https://www.tiktok.com/@77_shumnyy_77/video/7108078504880688385?is_copy_url=1&is_from_webapp=v1": 0
}

with TikTokApi() as api:
    for url in list(url_dict.keys()):
        id = extract_tiktok_video_id(url)
        video_data = get_video_bytes(api, id)
        download_video(video_data, generate_random_file_name())


L =[]

for root, dirs, files in os.walk(r"C:\Code\tiktok-downloader\downloaded_tiktoks"):
    for file in files:
        if os.path.splitext(file)[1] == '.mp4':
            filePath = os.path.join(root, file)
            video = VideoFileClip(filePath)
            L.append(video)

final_clip = concatenate_videoclips(L, method = "compose")
final_clip.to_videofile("final_output.mp4")