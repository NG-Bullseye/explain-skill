#!/usr/bin/env python3
"""Print what the user typed in earlier Claude Code sessions about a topic.

usage: user_words.py [--limit N] [--all-projects] keyword [keyword ...]

Reads the session histories below ~/.claude/projects, keeps the messages the
user typed himself that contain one of the keywords (case-insensitive), and
prints them newest first. Default scope is the project of the current working
directory; --all-projects searches every project.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"


def typed_messages(path):
    """Yield (timestamp, text) for every message the user typed in one history."""
    with open(path, encoding="utf-8", errors="replace") as lines:
        for line in lines:
            if '"type":"user"' not in line and '"type": "user"' not in line:
                continue
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            if entry.get("type") != "user" or entry.get("isMeta") or entry.get("isSidechain"):
                continue
            content = (entry.get("message") or {}).get("content")
            if isinstance(content, list):
                content = "\n".join(
                    part.get("text", "") for part in content
                    if isinstance(part, dict) and part.get("type") == "text"
                )
            if not isinstance(content, str):
                continue
            # Pasted material is not the user's own wording.
            text = re.sub(r"<pasted_content.*?</pasted_content[^>]*>", "", content, flags=re.DOTALL).strip()
            # Tool results, command echoes and injected reminders start with a tag.
            if not text or text.startswith("<") or text.startswith("[Request interrupted"):
                continue
            yield entry.get("timestamp", ""), text


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("keywords", nargs="+")
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--all-projects", action="store_true")
    args = parser.parse_args()

    pattern = re.compile("|".join(re.escape(word) for word in args.keywords), re.IGNORECASE)
    if args.all_projects:
        folders = [folder for folder in PROJECTS.iterdir() if folder.is_dir()]
    else:
        # Claude Code names a project folder after its path, separators as dashes.
        folders = [PROJECTS / re.sub(r"[^A-Za-z0-9]", "-", os.getcwd())]

    hits = []
    for folder in folders:
        for history in folder.glob("*.jsonl"):
            for timestamp, text in typed_messages(history):
                if pattern.search(text):
                    hits.append((timestamp, folder.name.rsplit("-", 1)[-1], text))

    if not hits:
        print("no earlier messages of the user contain: " + ", ".join(args.keywords))
        return 0
    hits.sort(reverse=True)
    for timestamp, project, text in hits[: args.limit]:
        print(f"--- {timestamp[:10]} {project}")
        print(text[:600])
    print(f"\n{min(len(hits), args.limit)} of {len(hits)} messages shown")
    return 0


if __name__ == "__main__":
    sys.exit(main())
