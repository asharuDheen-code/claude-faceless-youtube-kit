"""Make a simple faceless vertical Short from a script: free voice + big captions + colour background.

Free setup kit by Orbynex (https://manageme.orbynex.io/). MIT licence.

  python make_short.py script.txt out           # English male voice
  python make_short.py script.txt out --voice ml-male --bg "#FFF4D6" --fg "#1B1B3A"

script.txt: one sentence per line. Writes out/short.mp4 (1080x1920), out/voice.mp3 and out/captions.srt.
Voice: Microsoft Edge online neural voices through the free `edge-tts` package (unofficial endpoint:
fine for your own channel; for paid ads use a licensed voice). Needs ffmpeg on PATH.
"""
import argparse
import asyncio
import os
import subprocess
import sys

VOICES = {
    "en-male": "en-US-AndrewNeural", "en-female": "en-US-AvaNeural",
    "in-male": "en-IN-PrabhatNeural", "in-female": "en-IN-NeerjaNeural",
    "ml-male": "ml-IN-MidhunNeural", "ml-female": "ml-IN-SobhanaNeural",
}


def ts(t):
    h, r = divmod(int(t * 1000), 3600000)
    m, r = divmod(r, 60000)
    s, ms = divmod(r, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


async def speak(lines, voice, rate, mp3):
    import edge_tts
    cues, offset = [], 0.0
    with open(mp3, "wb") as out:
        for line in lines:
            part = mp3 + ".part.mp3"
            com = edge_tts.Communicate(line, voice, rate=rate)
            with open(part, "wb") as f:
                async for ch in com.stream():
                    if ch["type"] == "audio":
                        f.write(ch["data"])
            dur = float(subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", part],
                capture_output=True, text=True).stdout.strip())
            cues.append((offset, offset + dur, line))
            offset += dur + 0.3
            out.write(open(part, "rb").read())
            os.remove(part)
    return cues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("out")
    ap.add_argument("--voice", default="en-male", help=", ".join(VOICES) + " or any Edge voice name")
    ap.add_argument("--rate", default="+0%")
    ap.add_argument("--bg", default="#FFF4D6", help="background colour (light looks best on phones)")
    ap.add_argument("--fg", default="#1B1B3A", help="caption colour")
    ap.add_argument("--music", help="optional background music file (use music you have rights to)")
    a = ap.parse_args()

    lines = [l.strip() for l in open(a.script, encoding="utf-8") if l.strip()]
    if not lines:
        sys.exit("script is empty")
    os.makedirs(a.out, exist_ok=True)
    voice = VOICES.get(a.voice, a.voice)

    # Each line is spoken separately with a 0.3 s pause; the pauses are rebuilt with ffmpeg concat below.
    parts, cues, t = [], [], 0.0
    import edge_tts  # noqa: F401  (fail early with a clear error if missing)
    for i, line in enumerate(lines):
        p = os.path.join(a.out, f"_l{i:02}.mp3")
        asyncio.run(speak([line], voice, a.rate, p))
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                 capture_output=True, text=True).stdout.strip())
        parts.append(p)
        cues.append((t, t + d, line))
        t += d + 0.3
    total = t + 0.5

    voice_mp3 = os.path.join(a.out, "voice.mp3")
    inputs, filt = [], ""
    for i, p in enumerate(parts):
        inputs += ["-i", p]
        filt += f"[{i}:a]apad=pad_dur=0.3[a{i}];"
    filt += "".join(f"[a{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=0:a=1[v]"
    subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", filt, "-map", "[v]", voice_mp3], check=True)
    for p in parts:
        os.remove(p)

    srt = os.path.join(a.out, "captions.srt")
    with open(srt, "w", encoding="utf-8") as f:
        for n, (s, e, txt) in enumerate(cues, 1):
            f.write(f"{n}\n{ts(s)} --> {ts(e)}\n{txt}\n\n")

    def ass_colour(hexc):
        h = hexc.lstrip("#")
        return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}".upper()

    style = (f"FontName=Arial,FontSize=20,Bold=1,PrimaryColour={ass_colour(a.fg)},BorderStyle=1,Outline=0,"
             f"Shadow=0,Alignment=10,MarginL=70,MarginR=70")
    vf = f"subtitles=captions.srt:force_style='{style}'"
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c={a.bg}:s=1080x1920:r=30:d={total:.2f}",
           "-i", "voice.mp3"]
    amap = "1:a"
    if a.music:
        cmd += ["-stream_loop", "-1", "-i", os.path.abspath(a.music)]
        cmd += ["-filter_complex", "[2:a]volume=0.12[m];[1:a][m]amix=inputs=2:duration=first[aout]"]
        amap = "[aout]"
    cmd += ["-vf", vf, "-map", "0:v", "-map", amap, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
            "-b:a", "160k", "-shortest", "-movflags", "+faststart", "short.mp4"]
    subprocess.run(cmd, check=True, cwd=a.out)  # run inside out/ so the subtitles path has no drive letter
    print("made:", os.path.join(a.out, "short.mp4"), f"({total:.1f} s)")
    print("captions:", srt)


if __name__ == "__main__":
    main()
