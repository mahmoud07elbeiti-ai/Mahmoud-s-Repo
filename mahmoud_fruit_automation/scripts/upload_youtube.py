#!/usr/bin/env python3
"""Optional YouTube upload via the official YouTube Data API v3."""
import argparse
import json
import sys
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private")
    parser.add_argument("--publish-at", help="UTC ISO timestamp, e.g. 2026-10-15T17:00:00Z; requires --privacy private")
    parser.add_argument("--client-secrets", default=str(ROOT / "client_secret.json"))
    parser.add_argument("--token", default=str(ROOT / "token.json"))
    args = parser.parse_args()

    video = Path(args.video)
    secrets = Path(args.client_secrets)
    token = Path(args.token)
    if not video.is_file():
        raise SystemExit(f"Video file not found: {video}")
    if not secrets.is_file():
        raise SystemExit(f"OAuth client file not found: {secrets}. See README.md for setup.")
    if args.publish_at and args.privacy != "private":
        raise SystemExit("Scheduled YouTube uploads must use --privacy private.")
    if args.publish_at and not args.publish_at.endswith("Z"):
        raise SystemExit("--publish-at must be a UTC timestamp ending in Z.")

    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        raise SystemExit("Install upload dependencies first: python -m pip install -r requirements.txt")

    creds = None
    if token.exists():
        creds = Credentials.from_authorized_user_file(str(token), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(secrets), SCOPES)
            creds = flow.run_local_server(port=0)
        token.write_text(creds.to_json(), encoding="utf-8")

    body = {
        "snippet": {
            "title": args.title[:100],
            "description": args.description[:5000],
            "categoryId": "24",
            "tags": ["Shorts", "AIFruit", "FruitStory"]
        },
        "status": {
            "privacyStatus": args.privacy,
            "selfDeclaredMadeForKids": False
        }
    }
    if args.publish_at:
        body["status"]["publishAt"] = args.publish_at

    youtube = build("youtube", "v3", credentials=creds)
    media = MediaFileUpload(str(video), mimetype="video/*", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
    print(json.dumps({
        "video_id": response.get("id"),
        "privacy": args.privacy,
        "url": f"https://www.youtube.com/watch?v={response.get('id')}"
    }, indent=2))

if __name__ == "__main__":
    main()
