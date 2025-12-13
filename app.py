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

        m3u8_link = None

        # TÜM ÇÖZÜNÜRLÜKLERİ İÇEREN MASTER M3U8
        for f in info.get("formats", []):
            if f.get("protocol") == "m3u8_native" and f.get("format_note") == "live":
                m3u8_link = f.get("url")
                break

        if not m3u8_link:
            return "Master m3u8 bulunamadı", 404

        return redirect(m3u8_link, code=302)

    except Exception as e:
        return f"Hata oluştu: {e}", 500


PORT = int(os.environ.get("PORT", 7860))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
