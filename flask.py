from flask import Flask, request, send_from_directory
from pydub import AudioSegment
import os
import base64

app = Flask(__name__)
