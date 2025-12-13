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
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(live_url, download=False)

        # SADECE m3u8 olanları al
        m3u8s = [
            f for f in info.get("formats", [])
            if f.get("protocol") == "m3u8_native" and f.get("height")
        ]

        if not m3u8s:
            return "m3u8 bulunamadı", 404

        # EN YÜKSEK ÇÖZÜNÜRLÜK
        best = max(m3u8s, key=lambda x: x["height"])

        return redirect(best["url"], code=302)

    except Exception as e:
        return f"Hata: {e}", 500


PORT = int(os.environ.get("PORT", 7860))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
