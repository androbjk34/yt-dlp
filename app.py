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

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "nocheckcertificate": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(live_url, download=False)

        m3u8_link = None

        for f in info.get("formats", []):
            if f.get("protocol") == "m3u8_native":
                m3u8_link = f.get("url")
                break

        if not m3u8_link:
            return "m3u8 bulunamadı", 404

        return redirect(m3u8_link, code=302)

    except Exception as e:
        return f"Hata: {str(e)}", 500


PORT = int(os.environ.get("PORT", 7860))

if __name__ == "__main__":
    print("YouTube LIVE master m3u8 proxy çalışıyor")
    app.run(host="0.0.0.0", port=PORT)
