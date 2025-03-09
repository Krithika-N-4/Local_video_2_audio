from flask import Flask, render_template, request, send_file, jsonify
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/audio"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extract", methods=["POST"])
def extract_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    # Save the uploaded video
    video_path = os.path.join(UPLOAD_FOLDER, file.filename)
    audio_filename = file.filename.rsplit(".", 1)[0] + ".mp3"
    audio_path = os.path.join(OUTPUT_FOLDER, audio_filename)
    
    file.save(video_path)
    
    try:
        # Extract audio using moviepy
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path)
        clip.close()
        
        return jsonify({"success": True, "audio_file": audio_filename})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    
    # Ensure file exists before allowing download
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

if __name__ == "__main__":
    app.run(debug=True)
