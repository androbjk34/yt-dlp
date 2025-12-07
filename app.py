from flask import Flask, request, redirect
import yt_dlp
import os

app = Flask(__name__)

@app.route("/youtube.m3u8")
def youtube_direct():
    channel_id = request.args.get("id")
    if not channel_id:
        return "Kanal ID gerekli ?id=KANAL_ID", 400

    try:
        live_url = f"https://www.youtube.com/channel/{channel_id}/live"

        # yt-dlp ile canlı yayının gerçek linkini al
        ydl_opts = {
            "quiet": True,
            "format": "bestvideo+bestaudio/best",  # tüm formatları destekler
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(live_url, download=False)
            m3u8_link = info.get("url")

        if not m3u8_link:
            return "Canlı yayın linki alınamadı.", 404

        # IPTV uyumu: 302 redirect
        return redirect(m3u8_link, code=302)

    except Exception as e:
        return f"Hata oluştu: {e}", 500

# Railway otomatik PORT kullanır
PORT = int(os.environ.get("PORT", 7860))

if __name__ == "__main__":
    print("YouTube /live Direct Proxy başlatılıyor...")
    print("TV player link formatı: http://127.0.0.1:7860/youtube.m3u8?id=KANAL_ID")
    app.run(host="0.0.0.0", port=PORT)
