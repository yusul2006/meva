from __future__ import annotations

import pytest

from meva.engine import VisualNovelEngine, build_story_from_dict


@pytest.fixture
def sample_payload() -> dict:
    return {
        "title": "테스트 스토리",
        "opening_scene": "intro",
        "characters": [{"name": "주인공"}],
        "scenes": [
            {
                "id": "intro",
                "description": "첫 만남",
                "dialogues": [
                    {"speaker": "주인공", "text": "안녕?"},
                    {"speaker": "친구", "text": "반가워!"},
                ],
                "choices": [
                    {"text": "미소로 답한다", "next_scene": "happy"},
                    {"text": "모른 척 지나간다", "next_scene": "sad"},
                ],
            },
            {
                "id": "happy",
                "description": "즐거운 시간",
                "dialogues": [
                    {"speaker": "친구", "text": "오늘 같이 놀자!"}
                ],
                "next_scene": None,
            },
            {
                "id": "sad",
                "description": "어색한 공기",
                "dialogues": [
                    {"speaker": "주인공", "text": "괜히 그랬나...?"}
                ],
                "next_scene": None,
            },
        ],
    }


def test_engine_follows_choice(sample_payload: dict) -> None:
    story = build_story_from_dict(sample_payload)

    responses = iter(["1"])
    captured: list[str] = []
    engine = VisualNovelEngine(
        story,
        output=captured.append,
        input_provider=lambda prompt: next(responses),
    )

    engine.play()

    assert any("선택지를 골라주세요" in message for message in captured)
    assert captured[-1].strip() == "*** 이야기의 끝에 도달했습니다. 감사합니다! ***"


def test_engine_reprompts_on_invalid_input(sample_payload: dict) -> None:
    story = build_story_from_dict(sample_payload)

    responses = iter(["틀림", "5", "2"])
    captured: list[str] = []
    engine = VisualNovelEngine(
        story,
        output=captured.append,
        input_provider=lambda prompt: next(responses),
    )

    engine.play()

    invalid_messages = [
        message for message in captured if "유효한 번호를 선택해주세요." in message or "숫자를 입력" in message
    ]
    assert len(invalid_messages) == 2
    assert captured[-1].strip() == "*** 이야기의 끝에 도달했습니다. 감사합니다! ***"
