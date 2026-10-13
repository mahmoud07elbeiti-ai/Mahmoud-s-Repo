#!/usr/bin/env python3
"""Generate a reusable AI fruit-story package without external APIs."""
import argparse
import json
import random
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDEAS_PATH = ROOT / "config" / "story_ideas.json"
OUTPUT_DIR = ROOT / "output"

def main():
    parser = argparse.ArgumentParser(description="Generate one AI fruit story package.")
    parser.add_argument("--idea", help="Specific idea ID, e.g. F001. Random idea if omitted.")
    parser.add_argument("--seed", type=int, help="Optional seed for reproducible selection.")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    data = json.loads(IDEAS_PATH.read_text(encoding="utf-8"))
    ideas = data["ideas"]
    if args.idea:
        matches = [x for x in ideas if x["id"].lower() == args.idea.lower()]
        if not matches:
            raise SystemExit(f"Unknown idea ID: {args.idea}. Available: {', '.join(x['id'] for x in ideas)}")
        idea = matches[0]
    else:
        idea = random.choice(ideas)

    characters = data["characters"]
    character_lines = "\n".join(f"- {characters[name]}" for name in idea["characters"])
    scenes = [
        ("Scene 1 — Hook (0–3 seconds)", idea["hook"], "Start with an immediate visual surprise. Tight close-up, expressive faces, vertical 9:16 framing."),
        ("Scene 2 — Conflict (3–10 seconds)", idea["premise"], "Show the conflict clearly through action and short dialogue. Keep character designs consistent."),
        ("Scene 3 — Escalation (10–18 seconds)", "The characters argue about what really happened. One character notices a clue that changes the situation.", "Fast reaction shots, clear gestures, dramatic but family-friendly expressions."),
        ("Scene 4 — Twist (18–25 seconds)", idea["twist"], "Reveal the twist visually. Pause briefly for the audience to understand it."),
        ("Scene 5 — Cliffhanger (25–30 seconds)", "One character looks directly at the camera and says: 'Wait… there's one more thing you don't know.'", "End on a strong reaction and a clear unresolved question.")
    ]

    script = f"""TITLE: {idea['title']}
HOOK: {idea['hook']}
TARGET FORMAT: YouTube Short, vertical 9:16, approximately 25–35 seconds
STYLE: Colorful cinematic 3D animated fruit characters, expressive faces, clear dialogue, quick pacing, family-friendly drama.

CHARACTER CONSISTENCY
{character_lines}

STORY PREMISE
{idea['premise']}

SCENE-BY-SCENE PROMPT
""" + "\n\n".join(f"{name}\nVisual/action: {visual}\nDirection: {direction}\nDialogue suggestion: Use short, natural lines; keep each line easy to understand and sync to the visible character." for name, visual, direction in scenes) + """

MASTER PROMPT FOR CANTINA
Create a vertical 9:16, 25–35 second cinematic 3D animated fruit drama titled \"""" + idea["title"] + """\". Keep the exact same character appearance across every shot. Use the character descriptions above. Start with the hook immediately, build a clear conflict, escalate it, reveal the twist, and end on a cliffhanger. Use expressive faces, readable actions, fast but coherent cuts, clean dialogue, and family-friendly humor/drama. Avoid random extra characters, inconsistent designs, garbled text, watermarks, and long silent openings. If the tool only supports a few shots, prioritize the hook, conflict, twist, and cliffhanger.

YOUTUBE METADATA
Title: """ + idea["title"] + """ 😳 #Shorts
Description: """ + idea["hook"] + """ Watch until the end for the twist! #Shorts #AIFruit #FruitStory
Tags: Shorts, AI fruit, fruit story, animated story, banana, strawberry, 3D animation

REVIEW CHECKLIST
[ ] Character designs stay consistent
[ ] Hook happens in the first 1–2 seconds
[ ] Dialogue is understandable
[ ] Twist is visible and makes sense
[ ] No copyrighted music or unlicensed material
[ ] Exported as vertical MP4 and watched before upload
"""

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base = f"{idea['id'].lower()}_{stamp}"
    payload = {
        "id": idea["id"],
        "title": idea["title"],
        "hook": idea["hook"],
        "premise": idea["premise"],
        "twist": idea["twist"],
        "characters": {name: characters[name] for name in idea["characters"]},
        "scenes": [{"heading": h, "visual": v, "direction": d} for h, v, d in scenes],
        "youtube_title": f"{idea['title']} 😳 #Shorts",
        "youtube_description": f"{idea['hook']} Watch until the end for the twist! #Shorts #AIFruit #FruitStory",
        "generated_at_utc": datetime.now(timezone.utc).isoformat()
    }
    (out / f"{base}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / f"{base}.txt").write_text(script, encoding="utf-8")
    print(f"Created story package: {out / (base + '.txt')}")
    print(f"Created structured data: {out / (base + '.json')}")

if __name__ == "__main__":
    main()
