"""Upload a video to YouTube through the official YouTube Data API v3.

Free setup kit by Orbynex (https://manageme.orbynex.io/). MIT licence.

Safe by default: without --approve it only checks the file and prints what WOULD be uploaded (dry run).

  python youtube_upload.py --login                                   # one time: opens Google sign-in
  python youtube_upload.py video.mp4 --title "My Short" --short      # dry run (nothing is uploaded)
  python youtube_upload.py video.mp4 --title "My Short" --short --description-file desc.txt \
      --tags "ai,claude,shorts" --srt captions.srt --srt-lang ml --privacy private --approve

Needs client_secret.json (an OAuth "Desktop app" client from Google Cloud) in this folder.
The login token is saved to token.json. Keep both files private; never share or commit them.
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET = os.path.join(HERE, "client_secret.json")
TOKEN = os.path.join(HERE, "token.json")
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",  # needed only for --srt captions
]


def get_credentials(interactive):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    elif interactive:
        if not os.path.exists(CLIENT_SECRET):
            sys.exit("client_secret.json not found. See README step 3 (Google Cloud OAuth client).")
        from google_auth_oauthlib.flow import InstalledAppFlow
        creds = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES).run_local_server(port=0)
    else:
        sys.exit("Not logged in. Run once:  python youtube_upload.py --login")
    with open(TOKEN, "w", encoding="utf-8") as f:
        f.write(creds.to_json())
    return creds


def video_seconds(path):
    """Duration via ffprobe if installed; None otherwise (the check is then skipped)."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
            capture_output=True, text=True, timeout=30)
        return float(out.stdout.strip())
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description="Upload a video to YouTube (dry run unless --approve).")
    ap.add_argument("video", nargs="?")
    ap.add_argument("--login", action="store_true", help="one-time Google sign-in, saves token.json")
    ap.add_argument("--title")
    ap.add_argument("--description", default="")
    ap.add_argument("--description-file", help="read the description from a UTF-8 text file")
    ap.add_argument("--tags", default="", help="comma separated")
    ap.add_argument("--short", action="store_true", help="vertical video under 3 min: adds #Shorts")
    ap.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"])
    ap.add_argument("--category", default="28", help="28 = Science & Technology, 22 = People & Blogs")
    ap.add_argument("--language", default="en", help="video language, e.g. en or ml")
    ap.add_argument("--srt", help="optional subtitles file (.srt)")
    ap.add_argument("--srt-lang", default="en")
    ap.add_argument("--made-for-kids", action="store_true")
    ap.add_argument("--approve", action="store_true", help="really upload (without it: dry run only)")
    a = ap.parse_args()

    if a.login:
        get_credentials(interactive=True)
        print("Logged in. token.json saved (keep it private).")
        return

    if not a.video or not a.title:
        ap.error("video and --title are required (or use --login)")

    description = a.description
    if a.description_file:
        with open(a.description_file, encoding="utf-8") as f:
            description = f.read().strip()
    title = a.title.strip()
    tags = [t.strip() for t in a.tags.split(",") if t.strip()]
    if a.short:
        if "#shorts" not in (title + " " + description).lower():
            description = (description + "\n\n#Shorts").strip()
        if "shorts" not in [t.lower() for t in tags]:
            tags.append("Shorts")

    problems = []
    if not os.path.isfile(a.video):
        problems.append(f"video not found: {a.video}")
    if len(title) > 100:
        problems.append(f"title is {len(title)} characters (YouTube max 100)")
    if "<" in title or ">" in title or "<" in description or ">" in description:
        problems.append("YouTube does not allow < or > in title/description")
    if len(description.encode("utf-8")) > 5000:
        problems.append("description is over 5000 bytes")
    if sum(len(t) for t in tags) + 2 * len(tags) > 500:
        problems.append("tags are over 500 characters in total")
    if a.srt and not os.path.isfile(a.srt):
        problems.append(f"subtitles not found: {a.srt}")
    secs = video_seconds(a.video) if os.path.isfile(a.video) else None
    if a.short and secs and secs > 180:
        problems.append(f"video is {secs:.0f} s; Shorts must be 3 minutes or less")

    plan = {
        "file": a.video,
        "size_mb": round(os.path.getsize(a.video) / 1e6, 1) if os.path.isfile(a.video) else None,
        "duration_s": round(secs, 1) if secs else "unknown (install ffmpeg to check)",
        "title": title,
        "description": description,
        "tags": tags,
        "privacy": a.privacy,
        "category": a.category,
        "language": a.language,
        "made_for_kids": a.made_for_kids,
        "subtitles": f"{a.srt} ({a.srt_lang})" if a.srt else None,
    }
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    if problems:
        sys.exit("NOT READY:\n- " + "\n- ".join(problems))
    if not a.approve:
        print("\nDRY RUN only. Nothing was uploaded. Add --approve to upload this exact video.")
        return

    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    yt = build("youtube", "v3", credentials=get_credentials(interactive=False), cache_discovery=False)
    body = {
        "snippet": {"title": title, "description": description, "tags": tags, "categoryId": a.category,
                    "defaultLanguage": a.language, "defaultAudioLanguage": a.language},
        "status": {"privacyStatus": a.privacy, "selfDeclaredMadeForKids": a.made_for_kids},
    }
    media = MediaFileUpload(a.video, chunksize=8 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"uploading {int(status.progress() * 100)}%")
    vid = resp["id"]
    print("uploaded:", vid)

    if a.srt:
        yt.captions().insert(
            part="snippet",
            body={"snippet": {"videoId": vid, "language": a.srt_lang, "name": a.srt_lang, "isDraft": False}},
            media_body=MediaFileUpload(a.srt, mimetype="application/octet-stream"),
        ).execute()
        print("subtitles added:", a.srt_lang)

    print("link:", f"https://youtube.com/shorts/{vid}" if a.short else f"https://youtu.be/{vid}")
    print("Check it in YouTube Studio: https://studio.youtube.com/")


if __name__ == "__main__":
    main()
