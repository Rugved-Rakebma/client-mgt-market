from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import click


def _format_time(seconds: float) -> str:
    """Convert seconds to H:MM:SS or M:SS format."""
    total = int(seconds)
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    if h > 0:
        return "{}:{:02d}:{:02d}".format(h, m, s)
    return "{}:{:02d}".format(m, s)


@click.command("format-transcript")
@click.argument("raw_json_path")
def format_transcript(raw_json_path: str) -> None:
    """Format a raw Fireflies JSON file into readable markdown.

    Outputs speaker-attributed transcript to stdout.
    """
    path = Path(raw_json_path)
    if not path.exists():
        click.echo(json.dumps({"error": "File not found: {}".format(raw_json_path)}, indent=2))
        sys.exit(1)

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        click.echo(json.dumps({"error": "Invalid JSON: {}".format(str(e))}, indent=2))
        sys.exit(1)

    sentences = data.get("sentences", [])  # type: List[Dict[str, Any]]
    speakers = data.get("speakers", [])  # type: List[Dict[str, Any]]
    title = data.get("title", "")
    date_str = data.get("dateString", data.get("date", ""))

    if not sentences:
        click.echo(json.dumps({"error": "No sentences found in transcript"}), indent=2)
        sys.exit(1)

    # Build speaker list
    speaker_names = []  # type: List[str]
    for s in speakers:
        if isinstance(s, dict):
            name = s.get("name", "")
            if name and name not in speaker_names:
                speaker_names.append(name)

    # Build formatted transcript — group consecutive sentences by same speaker
    lines = []  # type: List[str]

    lines.append("## Speakers\n")
    for name in speaker_names:
        lines.append("- {}".format(name))
    lines.append("")
    lines.append("## Transcript\n")

    current_speaker = ""
    current_block = []  # type: List[str]
    block_start = 0.0

    for sentence in sentences:
        speaker = sentence.get("speaker_name", "Unknown")
        text = sentence.get("text", "").strip()
        start = sentence.get("start_time", 0.0)

        if not text:
            continue

        if speaker != current_speaker:
            # Flush previous block
            if current_block:
                lines.append("**{}** ({})\n".format(current_speaker, _format_time(block_start)))
                lines.append(" ".join(current_block))
                lines.append("")

            current_speaker = speaker
            current_block = [text]
            block_start = start
        else:
            current_block.append(text)

    # Flush last block
    if current_block:
        lines.append("**{}** ({})\n".format(current_speaker, _format_time(block_start)))
        lines.append(" ".join(current_block))
        lines.append("")

    output = "\n".join(lines)

    # Output as JSON with metadata so skills can parse it
    click.echo(json.dumps({
        "title": title,
        "date": date_str,
        "speakers": speaker_names,
        "transcript_md": output,
    }, indent=2))
