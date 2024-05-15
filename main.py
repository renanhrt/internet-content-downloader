from flask import Flask, render_template, request, send_file, jsonify
from pytube import YouTube
import os

app = Flask(__name__)
 
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/watch', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        url = request.form['url']

        yt = YouTube(url)
        yt.register_on_progress_callback(progress_callback)
        yt.register_on_complete_callback(complete_callback)
        thumbnail_url = yt.thumbnail_url
        title = yt.title
        views = yt.views
        author = yt.author
        date = yt.publish_date
        streams = yt.fmt_streams
        
        stream_info = {}
        for stream in streams:
            mime_type = stream.mime_type
            quality = getattr(stream, 'resolution', getattr(stream, 'abr', None))

            if mime_type not in stream_info:
                stream_info[mime_type] = {"qualities": set()}
            
            if quality:
                stream_info[mime_type]["qualities"].add(quality)

        for mime_type in stream_info:
            stream_info[mime_type]["qualities"] = list(stream_info[mime_type]["qualities"])

        return render_template('watch.html', thumbnail_url = thumbnail_url, title = title, views = views, author = author, date=date, url=url, stream_info=stream_info)
    else:
        return render_template('watch.html')

@app.route('/watch/download', methods=['POST', 'GET'])
def download():
    if request.method == 'POST':
        for key, value in request.form.items():
            print(key, value)
        url = request.form['url']

        yt = YouTube(url)
        yt.register_on_progress_callback(progress_callback)
        yt.register_on_complete_callback(complete_callback)

        stream = yt.streams.get_highest_resolution()
        filename = stream.download()

        return send_file(filename, as_attachment=True)
    else:
        return render_template('watch.html')

def progress_callback(stream, chunk, bytes_remaining):
    size = stream.filesize
    progress = int(((size - bytes_remaining) / size) * 100)
    print(progress)
    
def complete_callback(stream, file_handle):
    print("downloading finished")

if __name__ == '__main__':
    app.run(debug=True)