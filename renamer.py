import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
load_dotenv(api_key)

TIMESTAMP_FILE = "last_run.txt"


def get_last_run_time():
    if os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, "r") as f:
            return float(f.read().strip())
    return 0


def save_run_time():
    with open(TIMESTAMP_FILE, "w") as f:
        f.write(str(time.time()))


last_run_time = get_last_run_time()
with open("./prompt.txt", "r") as file:
    prompt = file.read()


client = genai.Client()
host = sys.argv[1]
print("Image files in the Downloads folder of {} \n".format(host))
directory = "/home/{}/Downloads/".format(host)
extensions = [".png", ".jpg"]
files = os.listdir(directory)
matching_files = [f for f in files if f.endswith(tuple(extensions))]

last_file = None
last_file_stat = None


for i, file in enumerate(matching_files):
    file_stat = os.stat(os.path.join(directory, file))
    if file_stat.st_ctime > last_run_time:
        img_path = Path(os.path.join(directory, file))
        img = client.files.upload(file=img_path)
        response = client.models.generate_content(
            model="gemini-3-flash-preview", contents=[img, prompt]
        )
        new_path = img_path.with_name(f"{response.text}{img_path.suffix}")
        os.rename(str(img_path), new_path)
    last_file = file
    last_file_stat = file_stat


save_run_time()
