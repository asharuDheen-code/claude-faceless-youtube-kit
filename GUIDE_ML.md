# Claude Faceless YouTube Kit: മലയാളം ഗൈഡ്

**Orbynex** തയ്യാറാക്കിയത് · English: [README.md](README.md)

Camera-യുടെ മുന്നിൽ വരേണ്ട. ഒരു idea പറഞ്ഞാൽ Claude Code:
1. **Script** എഴുതി ആദ്യം നിങ്ങളെ കാണിക്കും.
2. **Video** ഉണ്ടാക്കും: free AI voice-ഉം വലിയ captions-ഉം (Malayalam അല്ലെങ്കിൽ English), 1080×1920.
3. **Title, description, tags, #Shorts** എഴുതും.
4. **Dry run:** upload ചെയ്യുന്നതിന് മുമ്പ് എല്ലാം check ചെയ്യും. ഈ ഘട്ടത്തിൽ ഒന്നും upload ആകില്ല.
5. നിങ്ങൾ **"approve"** എന്ന് പറഞ്ഞാൽ മാത്രം YouTube-ന്റെ official API വഴി upload ചെയ്ത് link തരും.

## വേണ്ടത്
- **Claude Code** (paid Claude plan വേണം: Pro അല്ലെങ്കിൽ അതിനു മുകളിൽ): https://claude.com/claude-code
- **Python 3.10+**: https://www.python.org/downloads/
- **ffmpeg** (Windows-ൽ: `winget install Gyan.FFmpeg`)
- YouTube channel ഉള്ള ഒരു Google account

## Setup (ഒരിക്കൽ മാത്രം, ഏകദേശം 15 മിനിറ്റ്)
1. ഈ page-ൽ പച്ച **Code → Download ZIP** അമർത്തി unzip ചെയ്യുക.
2. ആ folder-ൽ terminal തുറന്ന് ഇത് run ചെയ്യുക:
   `pip install -r requirements.txt edge-tts`
3. **Google Cloud (free):**
   1. https://console.cloud.google.com/ തുറന്ന് ഒരു പുതിയ project ഉണ്ടാക്കുക.
   2. **APIs & Services → Library**-ൽ പോയി **YouTube Data API v3** enable ചെയ്യുക.
   3. **OAuth consent screen**-ൽ External തിരഞ്ഞെടുത്ത്, നിങ്ങളുടെ Gmail **test user** ആയി ചേർക്കുക.
   4. **Credentials → Create credentials → OAuth client ID → Desktop app** എടുത്ത് JSON download ചെയ്യുക.
   5. ആ file-ന്റെ പേര് `client_secret.json` എന്നാക്കി ഈ folder-ൽ ഇടുക.
4. ഒരിക്കൽ login ചെയ്യുക: `python youtube_upload.py --login`. Browser തുറക്കും; channel ഉള്ള account തിരഞ്ഞെടുക്കുക.
5. ഈ folder-ൽ `claude` എന്ന് type ചെയ്ത് Claude Code തുടങ്ങുക. [PROMPT.md](PROMPT.md)-ലെ ഒരു prompt paste ചെയ്യുക.

> 🔒 `client_secret.json`-ഉം `token.json`-ഉം നിങ്ങളുടെ താക്കോലുകളാണ്. ആർക്കും കൊടുക്കരുത്, GitHub-ൽ ഇടരുത്.

## ഉദാഹരണ prompt
```
"ചെറിയ കടകൾക്ക് ഉപയോഗിക്കാവുന്ന 3 free AI tools" എന്ന വിഷയത്തിൽ 30 സെക്കൻഡ് YouTube Short ഉണ്ടാക്കൂ.
Malayalam, ml-male voice. ആദ്യം script കാണിക്കൂ. ഞാൻ approve എന്ന് പറഞ്ഞാൽ private ആയി upload ചെയ്യൂ.
```

## സത്യസന്ധമായി അറിയേണ്ടത്
- **ചെലവ്:** ഈ kit-നും YouTube API-ക്കും പണം വേണ്ട. പക്ഷേ Claude Code-ന് paid Claude plan വേണം.
- **Quota:** API ദിവസവും 10,000 units തരും. ഒരു upload അതിൽ വലിയൊരു ഭാഗം എടുക്കും, അതുകൊണ്ട് ദിവസം കുറച്ച് uploads മാത്രം.
- **ആദ്യം private:** പുതിയ (verify ചെയ്യാത്ത) Google Cloud project-ൽ നിന്നുള്ള uploads YouTube private ആക്കി വെക്കും.
  [YouTube Studio](https://studio.youtube.com/)-ൽ പോയി public ആക്കാം, അല്ലെങ്കിൽ YouTube API audit-ന് apply ചെയ്യാം.
- **Voice:** free Edge voice ഒരു unofficial Microsoft endpoint ആണ്. സ്വന്തം channel-ന് കുഴപ്പമില്ല; paid ads-ന് licensed voice ഉപയോഗിക്കുക.
- Video style simple ആണ് (നിറമുള്ള background + captions). Animation-ഉം music-ഉം വേണമെങ്കിൽ Claude-നോട് `make_short.py` മെച്ചപ്പെടുത്താൻ പറയാം.
  മുഴുവൻ pipeline നിങ്ങൾക്കായി set ചെയ്യണമെങ്കിൽ Instagram-ൽ [@orbynex.io](https://www.instagram.com/orbynex.io/)-ന് message ചെയ്യൂ.
- Rights ഉള്ള music-ഉം images-ഉം clips-ഉം മാത്രം ഉപയോഗിക്കുക.
