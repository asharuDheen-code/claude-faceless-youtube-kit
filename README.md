# Claude Faceless YouTube Kit (free)

**by [Orbynex](https://manageme.orbynex.io/)** · Malayalam guide: [GUIDE_ML.md](GUIDE_ML.md)

No camera, no face. Tell Claude Code an idea and it:

| Step | What happens |
|---|---|
| 1. **Script** | Claude writes a short script (hook → points → call to action) and shows it to you |
| 2. **Video** | `make_short.py` makes a 1080×1920 video: free AI voice + big captions (English or Malayalam) |
| 3. **Text** | Claude writes the title, description, tags and `#Shorts` |
| 4. **Check** | `youtube_upload.py` does a **dry run**: length, title limit, tags, subtitles. Nothing is uploaded |
| 5. **Upload** | Only after you say **"approve"**: uploads through YouTube's official Data API and gives you the link |

## You need
- **Claude Code**: needs a paid Claude plan (Pro or above). Install: https://claude.com/claude-code
- **Python 3.10+**: https://www.python.org/downloads/
- **ffmpeg**: https://ffmpeg.org/download.html (Windows: `winget install Gyan.FFmpeg`)
- A **Google account** with a YouTube channel

## Setup (about 15 minutes, once)
1. Download this kit (green **Code → Download ZIP**, then unzip) or `git clone` it.
2. In a terminal in this folder:
   ```
   pip install -r requirements.txt edge-tts
   ```
3. **Google Cloud (free):**
   1. Open https://console.cloud.google.com/ → create a project.
   2. **APIs & Services → Library** → enable **YouTube Data API v3**.
   3. **OAuth consent screen** → External → add your own Gmail as a **test user**.
   4. **Credentials → Create credentials → OAuth client ID → Desktop app** → download the JSON.
   5. Rename it to `client_secret.json` and put it in this folder.
4. Log in once: `python youtube_upload.py --login` (a browser opens; choose your channel's Google account).
5. Start Claude Code here: `claude` → paste a prompt from [PROMPT.md](PROMPT.md).

> 🔒 `client_secret.json` and `token.json` are your keys. Never share them or upload them to GitHub
> (this repo's `.gitignore` already skips them).

## Without Claude (plain Python)
```
python make_short.py script.txt out --voice en-male
python youtube_upload.py out/short.mp4 --title "My first Short" --short --srt out/captions.srt   # dry run
python youtube_upload.py out/short.mp4 --title "My first Short" --short --srt out/captions.srt --approve
```
Voices: `en-male` `en-female` `in-male` `in-female` `ml-male` `ml-female`. Options: `--bg "#FFF4D6"`
`--fg "#1B1B3A"` `--music bgm.mp3` · upload: `--privacy private|unlisted|public` `--tags "a,b"`
`--description-file d.txt` `--language ml` `--srt-lang ml`.

## Honest limits
- **Cost:** the kit and the YouTube API have no charge. Claude Code needs a paid Claude plan.
- **Quota:** the API gives 10,000 units a day by default and each upload uses a large part of it:
  a few uploads a day, not dozens.
- **Private first:** YouTube keeps uploads from new, unverified API projects **private**. Switch them to
  public in [YouTube Studio](https://studio.youtube.com/), or apply for YouTube's API audit.
- **Voice:** the free Edge voice uses an unofficial Microsoft endpoint. Fine for your own channel; use a
  licensed voice for paid ads.
- The video style is simple (colour background + captions). For animation, music and better visuals, ask Claude to
  improve `make_short.py`, or [ask Orbynex](https://www.instagram.com/orbynex.io/) to build a full pipeline for you.
- Use only music, images and clips you have the rights to.

MIT licence · Made by Orbynex · Instagram [@orbynex.io](https://www.instagram.com/orbynex.io/)
