import os
import sys

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


with open("./prompt.txt", "r") as file:
    content = file.read()

host = sys.argv[1]
print("Image files in the Downloads folder of {} \n".format(host))
directory = "/home/{}/Downloads/".format(host)
extensions = [".png", ".jpg", ".ico", ".webp", ".svg"]


try:
    for file in os.listdir(directory):
        if file.endswith(tuple(extensions)):
            img = os.path.join(directory, file)
except FileNotFoundError:
    print("Directory not found! Probably the host name is wrong")
