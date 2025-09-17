"""Interactive engine for running a visual novel story."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from .story import Choice, Dialogue, Scene, Story


class OutputHandler(Protocol):
    """Protocol describing output behaviour for the engine."""

    def __call__(self, message: str) -> None:  # pragma: no cover - simple protocol stub
        ...


class InputProvider(Protocol):
    """Protocol describing input behaviour for the engine."""

    def __call__(self, prompt: str) -> str:  # pragma: no cover - simple protocol stub
        ...


@dataclass
class VisualNovelEngine:
    """A simple engine that plays through a :class:`Story`."""

    story: Story
    output: OutputHandler
    input_provider: InputProvider

    def play(self, starting_scene: Optional[str] = None) -> None:
        """Begin the story and continue until no next scene is available."""

        current_scene_id = starting_scene or self.story.opening_scene
        while current_scene_id:
            scene = self.story.get_scene(current_scene_id)
            self._render_scene(scene)

            if scene.has_choices():
                current_scene_id = self._choose_next_scene(scene)
            else:
                current_scene_id = scene.next_scene

        self.output("\n*** 이야기의 끝에 도달했습니다. 감사합니다! ***\n")

    def _render_scene(self, scene: Scene) -> None:
        if scene.description:
            self.output(f"\n[{scene.identifier}] {scene.description}")
        else:
            self.output(f"\n[{scene.identifier}]")

        for dialogue in scene.dialogues:
            self._render_dialogue(dialogue)

        if scene.has_choices():
            self.output("\n선택지를 골라주세요:")
            for index, choice in enumerate(scene.choices, start=1):
                self.output(f"  {index}. {choice.text}")

    def _render_dialogue(self, dialogue: Dialogue) -> None:
        self.output(f"{dialogue.speaker}: {dialogue.text}")

    def _choose_next_scene(self, scene: Scene) -> Optional[str]:
        while True:
            response = self.input_provider("번호를 입력하세요: ")
            try:
                selected = int(response)
            except ValueError:
                self.output("숫자를 입력해주세요.")
                continue

            index = selected - 1
            if 0 <= index < len(scene.choices):
                return scene.choices[index].next_scene

            self.output("유효한 번호를 선택해주세요.")


def build_story_from_dict(payload: dict) -> Story:
    """Build a :class:`Story` from a dictionary structure."""

    scenes = {}
    for scene_payload in payload.get("scenes", []):
        choices = [
            Choice(text=choice["text"], next_scene=choice["next_scene"])
            for choice in scene_payload.get("choices", [])
        ]
        dialogues = [
            Dialogue(speaker=dialogue["speaker"], text=dialogue["text"])
            for dialogue in scene_payload.get("dialogues", [])
        ]
        scenes[scene_payload["id"]] = Scene(
            identifier=scene_payload["id"],
            description=scene_payload.get("description", ""),
            dialogues=dialogues,
            choices=choices,
            next_scene=scene_payload.get("next_scene"),
        )

    characters = {}
    for character_payload in payload.get("characters", []):
        characters[character_payload["name"]] = Character(
            name=character_payload["name"],
            description=character_payload.get("description", ""),
        )

    return Story(
        title=payload.get("title", "미연시"),
        scenes=scenes,
        opening_scene=payload["opening_scene"],
        characters=characters,
    )


# Lazily import Character to avoid circular import in type checking.
from .story import Character  # noqa: E402  # isort:skip
