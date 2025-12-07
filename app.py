from flask import Flask, request, redirect
import subprocess
import sys

app = Flask(__name__)

@app.route("/youtube.m3u8")
def youtube_direct():
    channel_id = request.args.get("id")
    if not channel_id:
        return "Kanal ID gerekli", 400

    try:
        live_url = f"https://www.youtube.com/channel/{channel_id}/live"

        # yt-dlp ile canlı yayının gerçek m3u8 linkini al
        cmd = [sys.executable, "-m", "yt_dlp", "-g", live_url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0 or not result.stdout.strip():
            return f"Canlı yayın linki alınamadı:\n{result.stderr}", 404

        m3u8_link = result.stdout.strip()

        # Direkt gerçek m3u8 linkine yönlendir
        return redirect(m3u8_link, code=302)

    except subprocess.TimeoutExpired:
        return "Zaman aşımı: Canlı yayın linki alınamadı.", 500

if __name__ == "__main__":
    print("YouTube /live Direct Proxy başlatılıyor...")
    print("TV player link formatı: http://127.0.0.1:7860/youtube.m3u8?id=KANAL_ID")
    app.run(host="0.0.0.0", port=7860, debug=True)
