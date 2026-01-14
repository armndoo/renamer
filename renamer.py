import datetime
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
load_dotenv(api_key)

with open("./prompt.txt", "r") as file:
    prompt = file.read()


client = genai.Client()
host = sys.argv[1]
print("Image files in the Downloads folder of {} \n".format(host))
directory = "/home/{}/Downloads/".format(host)
extensions = [".png", ".jpg"]

for file in os.listdir(directory):
    if file.endswith(tuple(extensions)):
        img_path = Path(os.path.join(directory, file))
        img = client.files.upload(file=img_path)
        response = client.models.generate_content(
            model="gemini-3-flash-preview", contents=[img, prompt]
        )
        new_path = img_path.with_name(f"{response.text}{img_path.suffix}")
        os.rename(str(img_path), new_path)
