from flask import Flask, request, redirect
import yt_dlp
import os

app = Flask(__name__)

@app.route("/youtube")
def youtube():
    video_id = request.args.get("id")
    if not video_id:
        return "Kanal ID gerekli ?id=xxx", 400
    
    url = f"https://www.youtube.com/channel/{video_id}/live"
    
    ydl_opts = {
        "quiet": True,
        "format": "best[ext=m3u8]/best",
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            m3u8_url = info.get("url")
    except Exception as e:
        return f"Hata: {e}", 500
    
    # 302 Redirect
    return redirect(m3u8_url, code=302)

PORT = int(os.environ.get("PORT", 7860))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
