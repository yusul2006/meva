"""Command line entry point for the visual novel engine."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import VisualNovelEngine, build_story_from_dict


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="간단한 미연시 게임 엔진")
    parser.add_argument(
        "story",
        type=Path,
        help="불러올 스토리 JSON 파일 경로",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = create_parser()
    args = parser.parse_args(argv)

    story_data = json.loads(args.story.read_text(encoding="utf-8"))
    story = build_story_from_dict(story_data)

    engine = VisualNovelEngine(story, output=print, input_provider=input)
    engine.play()


if __name__ == "__main__":  # pragma: no cover - convenience CLI
    main()
