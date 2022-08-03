import random
import string

from TikTokApi import TikTokApi
from datetime import datetime
from pregex.quantifiers import AtMost, AtLeastOnce
from pregex.classes import AnyDigit


def get_video_bytes(api, tiktok_video_id):
    video = api.video(id=tiktok_video_id)
    return video.bytes()

def generate_random_file_name():
    date_today = datetime.today().strftime("%Y-%m-%d")
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
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




with TikTokApi() as api:
    video_data = get_video_bytes(api, "7122878927755922694")
    download_video(video_data, generate_random_file_name())