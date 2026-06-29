from __future__ import annotations


def like_service_provider() -> dict:
    from bias_ext_likes.backend.models import PostLike
    from bias_ext_likes.backend.services import can_like_post, like_post, unlike_post

    return {
        "model": PostLike,
        "event_types": like_event_type_aliases(),
        "like_post": like_post,
        "unlike_post": unlike_post,
        "can_like_post": can_like_post,
    }


def like_event_type_aliases() -> dict[str, type]:
    from bias_ext_likes.backend.events import PostLikedEvent, PostUnlikedEvent

    return {
        "likes.post.liked": PostLikedEvent,
        "likes.post.unliked": PostUnlikedEvent,
    }


like_service_provider.event_types = like_event_type_aliases


