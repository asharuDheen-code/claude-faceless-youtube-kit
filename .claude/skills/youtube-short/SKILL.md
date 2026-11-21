---
name: youtube-short
description: Make a faceless YouTube Short with this kit and upload it through the official YouTube Data API, only after the user says "approve". Writes the script, makes a free voice + caption video (make_short.py), writes title/description/tags, dry-runs the upload, then uploads. Triggers - youtube short, faceless video, make a short, upload to youtube, യൂട്യൂബ്, ഷോർട്ട്സ്
---

# YouTube Short maker (free kit by Orbynex)

Tools in this repo: `make_short.py` (script → voice + captions → 1080x1920 MP4) and `youtube_upload.py`
(dry run by default; real upload only with `--approve`). Talk in the user's language (Malayalam or English).

## Steps
1. **Topic.** Ask once (if not given): the idea or a link to study, language (en / ml), voice
   (`en-male`, `en-female`, `in-male`, `in-female`, `ml-male`, `ml-female`), length (20–45 s).
2. **Script.** Write 6–10 short lines (one sentence per line, ~2.5 words per second of video): a hook in
   line 1, one idea per line, a call to action in the last line. Only true, checkable claims. Save it as
   `work/<slug>/script.txt` and show it. Wait for OK or changes.
3. **Video.** First time only: `pip install -r requirements.txt` and `pip install edge-tts`; ffmpeg must be on PATH.
   `python make_short.py work/<slug>/script.txt work/<slug> --voice <voice>` → `short.mp4` + `captions.srt`.
   If the user has their own video, skip this and use their file.
4. **Text.** Write a title (≤ 100 characters, no `<` `>`), a description (2–4 lines + 3–5 hashtags) saved to
   `work/<slug>/description.txt`, and 5–10 tags.
5. **Dry run.** `python youtube_upload.py work/<slug>/short.mp4 --title "..." --description-file work/<slug>/description.txt --tags "..." --short --srt work/<slug>/captions.srt --srt-lang <en|ml> --language <en|ml> --privacy private`
   Show the plan it prints (file, length, title, description, tags, privacy).
6. **Approve.** Upload ONLY when the user replies "approve" for this exact video: rerun the same command with
   `--approve`. Give back the link. Never add `--approve` on your own, never change privacy to public unless asked.

## First-time login
If the script says "Not logged in": the user needs `client_secret.json` (see README step 3), then runs
`python youtube_upload.py --login` themselves (it opens Google sign-in in the browser). Never ask for or print
their password, client secret or token.json.

## Honest limits (tell the user when relevant)
- Claude Code needs a paid Claude plan. The YouTube Data API has no charge, but it has a daily quota
  (default 10,000 units); each upload uses a large part of it, so plan a few uploads a day, not dozens.
- New Google Cloud projects that are not verified (audited) by YouTube can only upload **private** videos.
  Make them public by hand in YouTube Studio, or apply for the API audit (YouTube API Services form).
- The free Edge voice uses an unofficial endpoint: fine for your own channel; use a licensed voice for paid ads.
- Use only music, images and footage you have the rights to.
