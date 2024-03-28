from flask import Flask, render_template, request, redirect, url_for, send_file
from pytube import YouTube
import os

app = Flask(__name__)
 
 
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/download', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        url = request.form['url']

        yt = YouTube(url)
        yt.register_on_progress_callback(progress_callback)
        yt.register_on_complete_callback(complete_callback)

        stream = yt.streams.get_highest_resolution()
        #filename = stream.download()

        return render_template('index.html')
        #return send_file(filename, as_attachment=True)
    else:
        return render_template('index.html')



def progress_callback(stream, chunk, bytes_remaining):
    size = stream.filesize
    progress = int(((size - bytes_remaining) / size) * 100)
    print(progress)
    # do call progress bar from GUI here

def complete_callback(stream, file_handle):
    print("downloading finished")

if __name__ == '__main__':
    app.run(debug=True)