from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from dataclasses import dataclass
from typing import Any

from bias_core.extensions.platform import AuthorizationPolicy
from bias_core.extensions.platform import dispatch_forum_event_after_commit
from bias_core.extensions.platform import evaluate_extension_policy
from bias_core.extensions.platform import get_extension_settings
from bias_core.extensions.runtime import (
    can_runtime_view_post,
    ensure_runtime_user_not_suspended,
    get_runtime_post_action_context,
)
from bias_ext_likes.backend.events import PostLikedEvent, PostUnlikedEvent
from bias_ext_likes.backend.models import PostLike


class PostActionContextNotFound(ValueError):
    pass


@dataclass(frozen=True)
class PostActionContext:
    id: int
    discussion_id: int
    user_id: int | None
    number: int | None
    discussion_title: str = ""


def like_post(post_id: int, user: Any) -> bool:
    ensure_runtime_user_not_suspended(user, "点赞帖子")
    post = _require_post_action_context(post_id, user)
    if post.user_id == user.id and not can_like_own_post():
        raise ValueError("不能给自己的帖子点赞")
    if not evaluate_extension_policy("post.like", default=True, user=user, post=post, post_context=post):
        raise PermissionDenied("没有权限点赞此帖子")
    if PostLike.objects.filter(post_id=post.id, user=user).exists():
        raise ValueError("已经点赞过了")

    try:
        PostLike.objects.create(post_id=post.id, user=user)
    except IntegrityError:
        raise ValueError("已经点赞过了")

    dispatch_forum_event_after_commit(
        PostLikedEvent(
            post_id=post.id,
            discussion_id=post.discussion_id,
            actor_user_id=user.id,
            post_user_id=post.user_id,
            post_number=post.number,
            discussion_title=post.discussion_title,
        )
    )
    return True


def unlike_post(post_id: int, user: Any) -> bool:
    ensure_runtime_user_not_suspended(user, "点赞帖子")
    post = _require_post_action_context(post_id, user)

    deleted_count, _ = PostLike.objects.filter(post_id=post.id, user=user).delete()
    if deleted_count == 0:
        raise ValueError("还没有点赞")
    dispatch_forum_event_after_commit(
        PostUnlikedEvent(
            post_id=post.id,
            discussion_id=post.discussion_id,
            actor_user_id=user.id,
            post_user_id=post.user_id,
            post_number=post.number,
            discussion_title=post.discussion_title,
        )
    )
    return True


def can_like_post(post: Any, user: Any) -> bool:
    if not _can_like_post_without_extension_policy(post, user):
        return False
    return bool(evaluate_extension_policy(
        "post.like",
        default=True,
        user=user,
        post=post,
    ))


def _can_like_post_without_extension_policy(post: Any, user: Any) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_suspended:
        return False
    if post.user_id == user.id and not can_like_own_post():
        return False
    return can_runtime_view_post(post, user)


def can_like_own_post() -> bool:
    return bool(get_extension_settings("likes").get("like_own_post", False))


def _require_post_action_context(post_id: int, user: Any) -> PostActionContext:
    context = get_runtime_post_action_context(post_id, user=user, require_visible=True)
    if context is None:
        raise PostActionContextNotFound("帖子不存在")
    return PostActionContext(
        id=int(context["id"]),
        discussion_id=int(context["discussion_id"]),
        user_id=context.get("user_id"),
        number=context.get("number"),
        discussion_title=str(context.get("discussion_title") or ""),
    )


class LikePostPolicy(AuthorizationPolicy):
    def can(self, user, ability, model, **context):
        if ability != "post.like":
            return None
        post = context.get("post") or model
        if isinstance(post, PostActionContext):
            if not user or not user.is_authenticated:
                return False
            if user.is_suspended:
                return False
            if post.user_id == user.id and not can_like_own_post():
                return False
            return None
        return _can_like_post_without_extension_policy(post, user) if post is not None else None


def resolve_post_can_like(post, context: dict) -> bool:
    user = context.get("user")
    return bool(user and can_like_post(post, user))
