from __future__ import annotations

from dataclasses import dataclass

from bias_core.extensions.platform import DomainEvent


@dataclass(frozen=True)
class PostLikedEvent(DomainEvent):
    post_id: int
    discussion_id: int
    actor_user_id: int
    post_user_id: int | None = None
    post_number: int | None = None
    discussion_title: str = ""


@dataclass(frozen=True)
class PostUnlikedEvent(DomainEvent):
    post_id: int
    discussion_id: int
    actor_user_id: int
    post_user_id: int | None = None
    post_number: int | None = None
    discussion_title: str = ""

