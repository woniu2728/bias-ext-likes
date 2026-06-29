from bias_ext_likes.backend.events import PostLikedEvent, PostUnlikedEvent


def get_runtime_user_by_id(*args, **kwargs):
    from bias_core.extensions.runtime import get_runtime_user_by_id as runtime_get_user_by_id

    return runtime_get_user_by_id(*args, **kwargs)


def notify_runtime_notification(*args, **kwargs):
    from bias_core.extensions.runtime import notify_runtime_notification as runtime_notify_notification

    return runtime_notify_notification(*args, **kwargs)


def handle_post_liked_notification(event: PostLikedEvent) -> None:
    from_user = _resolve_user_or_none(event.actor_user_id)
    if from_user is None:
        return

    notify_runtime_notification("notify_post_liked_from_event", event=event, from_user=from_user)


def handle_post_unliked_notification(event: PostUnlikedEvent) -> None:
    from_user = _resolve_user_or_none(event.actor_user_id)
    if from_user is None:
        return

    notify_runtime_notification("delete_post_liked_for_post_user", post_id=event.post_id, from_user=from_user)


def _resolve_user_or_none(user_id: int):
    try:
        return get_runtime_user_by_id(user_id)
    except Exception:
        return None
