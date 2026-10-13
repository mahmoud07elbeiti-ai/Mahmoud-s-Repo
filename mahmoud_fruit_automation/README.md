# Mahmoud's AI Fruit Video Automation

A $0-first starter project for making AI fruit-story YouTube Shorts.

## Reality check: what is and isn't automated

This starter can automatically generate a story package (hook, scenes, dialogue, title, description, and tags) using local Python templates. GitHub Actions can run that story generator on a schedule and save the result as a downloadable workflow artifact.

**Cantina video generation is a manual step for now.** This project does not assume Cantina has a public API or that its free plan supports external automation. Generate the story in Cantina, export the finished MP4, then use the optional local assembly/upload steps below. Do not pay for an API or subscription just to make this starter run.

## Files

- `scripts/generate_story.py` — creates one story package without paid APIs.
- `scripts/assemble_video.py` — optionally joins exported MP4 scene clips using FFmpeg.
- `scripts/upload_youtube.py` — optional YouTube upload helper using the official YouTube Data API.
- `config/story_ideas.json` — story ideas and reusable character setups.
- `.github/workflows/generate-story.yml` — scheduled/manual story generation on GitHub.
- `requirements.txt` — dependencies for optional YouTube upload only.

## Part 1 — Add these files to GitHub

1. Open your repository: `https://github.com/mahmoud07elbeiti-ai/Mahmoud-s-Repo`
2. For each file in this ZIP, create the same path using **Add file → Create new file** and paste its contents. You can also extract the ZIP on your computer and upload the files through GitHub's web interface.
3. Commit the files to your repository's default branch.
4. Open **Actions** and enable workflows if GitHub asks.

## Part 2 — Generate a story for free

### On GitHub
1. Open the **Actions** tab.
2. Select **Generate fruit story**.
3. Click **Run workflow**.
4. Open the completed run and download the `fruit-story-package` artifact.
5. Extract it and open `story.txt` or `story.json`.

The workflow also runs on a schedule (once a day, around 13:00 UTC). Scheduled workflows can be delayed by GitHub, so don't rely on the exact minute.

### On your computer
Install Python 3.10+ if needed. In a terminal, run:

```bash
python scripts/generate_story.py
```

The generated package is saved under `output/`. You can choose an idea by ID:

```bash
python scripts/generate_story.py --idea F001
```

This script uses templates and needs no API key. It does **not** call ChatGPT or generate video by itself.

## Part 3 — Create the video in Cantina (free plan)

1. Open the generated `output/story.txt`.
2. Copy the story/prompt into Cantina and choose your preferred character.
3. Generate with the free credits available in your Cantina account.
4. Export/download the result as an MP4.
5. Put the exported file in `input/` on your computer (create that folder if needed).

If Cantina cannot export an MP4 or only gives you a share page, stop here and tell us what export options it shows. Don't buy a plan just to proceed.

## Part 4 — Optional scene assembly with FFmpeg

This is optional. If Cantina exports one complete video, you don't need assembly. If it exports several separate scene clips:

1. Install FFmpeg from the official FFmpeg website for your operating system.
2. Put scene files in `input/scenes/`, named in order, such as `scene1.mp4`, `scene2.mp4`, `scene3.mp4`.
3. Run:

```bash
python scripts/assemble_video.py --input-dir input/scenes --output output/fruit_short.mp4
```

The script attempts to normalize the clips to vertical 1080x1920, 30 fps, and H.264/AAC. FFmpeg must be installed separately. Keep your exported source clips; this script creates a new output file.

## Part 5 — Optional YouTube Shorts upload

Uploading requires a one-time Google Cloud / YouTube Data API setup and OAuth consent. API quota limits apply; the API generally doesn't require a paid subscription, but Google can change policies and quota limits.

1. Follow Google's official YouTube Data API Python quickstart and enable **YouTube Data API v3** for a Google Cloud project.
2. Create OAuth client credentials for a **Desktop app** and save the downloaded file as `client_secret.json` in the project root. **Never commit this file.**
3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Upload a finished video:

```bash
python scripts/upload_youtube.py --video output/fruit_short.mp4 --title "The Broke Banana Was Secretly Rich 😳" --description "A fruit drama with a twist. #Shorts #AIFruit"
```

The first run opens a browser for your own account authorization and saves `token.json`. Both files are ignored by Git. The upload defaults to **private** so you can review it first. To publish publicly, pass `--privacy public`; to schedule, set `--publish-at 2026-10-15T17:00:00Z` and use `--privacy private` (YouTube requires scheduled uploads to be private). Review the title, content, music rights, and audience settings before publishing.

**Do not put OAuth tokens, client secrets, passwords, or API keys in source code or GitHub commits.**

## What this starter does not do yet

- It cannot remotely click Cantina or bypass Cantina's interface.
- It does not create unlimited videos; Cantina free credits may be limited.
- It does not guarantee views or monetization.
- It does not auto-publish videos directly from Cantina. That requires a supported integration or a separate computer-side process and should be added only after export and upload work reliably.

## Recommended first test

Generate one story → create one video in Cantina → export an MP4 → review it → upload privately to YouTube. Don't automate public publishing until you have verified the full process.
