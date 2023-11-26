
from flask import Flask, request, send_from_directory
from pydub import AudioSegment
import os
import base64

app = Flask(__name__)

def file_to_binary(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    return binary_data

def encode_base64(binary_data):
    encoded_data = base64.b64encode(binary_data)
    return encoded_data

def write_to_bin_file(encoded_data, bin_file_path):
    with open(bin_file_path, 'wb') as file:
        file.write(encoded_data)
    return bin_file_path

def create_cue_file(bin_file_path, cue_file_path):
    with open(cue_file_path, 'w') as cue_file:
        cue_file.write(f"FILE "{bin_file_path}" BINARY\n")
    return cue_file_path

def compress_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    byte_coded_music = audio.raw_data
    return byte_coded_music

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    file_path = os.path.join('uploads', uploaded_file.filename)
    uploaded_file.save(file_path)

    if uploaded_file.filename.endswith('.mp3'):
        byte_coded_music = compress_audio(file_path)
        encoded_data = encode_base64(byte_coded_music)
    else:
        binary_data = file_to_binary(file_path)
        encoded_data = encode_base64(binary_data)

    bin_file_path = file_path + '.bin'
    cue_file_path = file_path + '.cue'

    write_to_bin_file(encoded_data, bin_file_path)
    create_cue_file(bin_file_path, cue_file_path)

    return send_from_directory('uploads', bin_file_path), send_from_directory('uploads', cue_file_path)

if __name__ == '__main__':
    app.run(debug=True)
