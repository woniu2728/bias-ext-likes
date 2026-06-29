from __future__ import annotations

from bias_core.extensions import ExtensionEventListenerDefinition

from bias_ext_likes.backend.events import PostLikedEvent, PostUnlikedEvent
from bias_ext_likes.backend.listeners import (
    handle_post_liked_notification,
    handle_post_unliked_notification,
)


def event_listener_definitions():
    return (
        ExtensionEventListenerDefinition(
            event_type=PostLikedEvent,
            handler=handle_post_liked_notification,
            description="点赞后发送回复被点赞通知。",
        ),
        ExtensionEventListenerDefinition(
            event_type=PostUnlikedEvent,
            handler=handle_post_unliked_notification,
            description="取消点赞后同步回复被点赞通知。",
        ),
    )
