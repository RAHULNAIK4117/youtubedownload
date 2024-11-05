from flask import Flask, request, jsonify, send_file, render_template
import yt_dlp
import os

app = Flask(__name__)

# Directory to save downloads
DOWNLOAD_DIR = './downloads'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Fetch video info using yt-dlp
@app.route('/get_video_info', methods=['POST'])
def get_video_info():
    data = request.json
    url = data.get('url')
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = [{'format_id': f['format_id'], 'resolution': f.get('height'), 'ext': f['ext']}
                       for f in info_dict['formats'] if f['vcodec'] != 'none']
            return jsonify({'title': info_dict['title'], 'formats': formats})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Download the selected format
@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    
    try:
        # Use yt-dlp to download the best video and audio
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',  # Ensures the output format is mp4
            'postprocessors': [{
                'key': 'FFmpegMerger'  # Merges audio and video streams
            }],
            'quiet': True,
            'no_warnings': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = os.path.join(DOWNLOAD_DIR, f"{info_dict['title']}.mp4")
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Serve frontend
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
