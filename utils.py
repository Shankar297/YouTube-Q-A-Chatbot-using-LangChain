import yt_dlp
import os
import re

def extract_clean_transcript(lines):
    clean_lines = []
    for line in lines:
        line = line.strip()

        if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue

        line = re.sub(r'<[^>]+>', '', line)

        if re.match(r'^\d+$', line) or '-->' in line:
            continue

        clean_lines.append(line)

    # Remove duplicates
    seen = set()
    final_lines = []
    for line in clean_lines:
        if line not in seen:
            seen.add(line)
            final_lines.append(line)

    return "\n".join(final_lines)

def download_subtitles(video_url, lang='en'):
    try:
        output_path = "subtitles"
        os.makedirs(output_path, exist_ok=True)

        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': [lang],
            'skip_download': True,
            'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_id = info.get('id')
            subtitle_filename = os.path.join(output_path, f"{video_id}.{lang}.vtt")

            if os.path.exists(subtitle_filename):
                # print(f"Subtitles downloaded: {subtitle_filename}")
                with open(subtitle_filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                return extract_clean_transcript(lines), 200
            else:
                return "Subtitles file not found. May not be available.", 400
    except Exception as e:
        return e, 500

