from flask import Flask, render_template, request, send_file, jsonify
from pytube import YouTube

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
            print(stream)
            quality = getattr(stream, 'resolution') if 'video' in mime_type else getattr(stream, 'abr')

            if mime_type not in stream_info:
                stream_info[mime_type] = []
            if quality:
                stream_info[mime_type].append(quality)

        for mime_type in stream_info:
            stream_info[mime_type] = list(stream_info[mime_type])

        for key, value in stream_info.items():
            seen = set()
            stream_info[key] = [x for x in value if not (x in seen or seen.add(x))]

        print(stream_info) 

        return render_template('watch.html', thumbnail_url = thumbnail_url, title = title, views = views, author = author, date=date, url=url, stream_info=stream_info)
    else:
        return render_template('watch.html')

@app.route('/watch/download', methods=['POST', 'GET'])
def download():
    if request.method == 'POST':
        url = request.form['url']
        type = request.form['type']
        quality = request.form['quality']
        print(url, type, quality)

        yt = YouTube(url)
        yt.register_on_progress_callback(progress_callback)
        yt.register_on_complete_callback(complete_callback)

        stream = yt.streams.filter(mime_type=type, res=quality).first()
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