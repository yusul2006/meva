"""Data structures describing a visual novel story."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional


@dataclass(frozen=True)
class Character:
    """Represents a character in the story."""

    name: str
    description: str = ""


@dataclass(frozen=True)
class Dialogue:
    """A piece of dialogue spoken by a character."""

    speaker: str
    text: str


@dataclass(frozen=True)
class Choice:
    """A choice presented to the player."""

    text: str
    next_scene: str


@dataclass
class Scene:
    """A single scene of the visual novel."""

    identifier: str
    description: str = ""
    dialogues: List[Dialogue] = field(default_factory=list)
    choices: List[Choice] = field(default_factory=list)
    next_scene: Optional[str] = None

    def has_choices(self) -> bool:
        return bool(self.choices)


@dataclass
class Story:
    """A complete story consisting of scenes and characters."""

    title: str
    scenes: Dict[str, Scene]
    opening_scene: str
    characters: Dict[str, Character] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.opening_scene not in self.scenes:
            raise ValueError(f"Opening scene '{self.opening_scene}' does not exist.")

    def iter_scenes(self) -> Iterable[Scene]:
        return self.scenes.values()

    def get_scene(self, identifier: str) -> Scene:
        try:
            return self.scenes[identifier]
        except KeyError as exc:
            raise KeyError(f"Scene '{identifier}' was not found in the story.") from exc
