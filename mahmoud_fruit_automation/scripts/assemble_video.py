#!/usr/bin/env python3
"""Join ordered MP4 scene clips with FFmpeg; FFmpeg must be installed separately."""
import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="input/scenes", help="Folder containing scene1.mp4, scene2.mp4, ...")
    parser.add_argument("--output", default="output/fruit_short.mp4")
    args = parser.parse_args()

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("FFmpeg was not found. Install FFmpeg first, then reopen your terminal.")
    source = Path(args.input_dir)
    clips = sorted(source.glob("*.mp4"), key=lambda p: p.name.lower())
    if not clips:
        raise SystemExit(f"No MP4 clips found in {source.resolve()}")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    # Re-encode each clip to consistent vertical H.264/AAC, then concatenate.
    with tempfile.TemporaryDirectory(prefix="fruit_video_") as tmp:
        tmpdir = Path(tmp)
        normalized = []
        for index, clip in enumerate(clips, start=1):
            target = tmpdir / f"clip_{index:03d}.mp4"
            command = [
                ffmpeg, "-y", "-i", str(clip),
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(target)
            ]
            subprocess.run(command, check=True)
            normalized.append(target)

        list_file = tmpdir / "concat.txt"
        list_file.write_text("".join(f"file '{p.as_posix()}'\n" for p in normalized), encoding="utf-8")
        subprocess.run([
            ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
            "-c", "copy", "-movflags", "+faststart", str(out.resolve())
        ], check=True)
    print(f"Created: {out.resolve()}")

if __name__ == "__main__":
    main()
