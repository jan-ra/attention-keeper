from flask import Flask, json
from moviepy.editor import *
import threading
import subprocess

companies = [{"id": 1, "name": "Company One"},
             {"id": 2, "name": "Company Two"}]

api = Flask(__name__)


@api.route('/', methods=['GET'])
def set_start():
    return "START"


@api.route('/', methods=['POST'])
def test():
    # print("POST")
    t = threading.Thread(target=show_vid)
    t.start()
    return "tests"


if __name__ == '__main__':
    api.run()


def show_vid():
    clip = VideoFileClip('speedup2.mp4')
    clip.preview()
