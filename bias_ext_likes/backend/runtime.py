from __future__ import annotations


def like_service_provider() -> dict:
    from bias_ext_likes.backend.models import PostLike
    from bias_ext_likes.backend.services import can_like_post, like_post, unlike_post

    return {
        "model": PostLike,
        "like_post": like_post,
        "unlike_post": unlike_post,
        "can_like_post": can_like_post,
    }


