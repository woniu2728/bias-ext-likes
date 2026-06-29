from __future__ import annotations

from typing import Any

from bias_ext_likes.backend.models import PostLike


def parse_liked_by_search_filter(token: str) -> str | None:
    if not token or ":" not in token:
        return None

    prefix, value = token.split(":", 1)
    if prefix.strip().lower() not in {"likedby", "liked-by"}:
        return None

    username = value.strip()
    return username or None


def apply_liked_by_filter(queryset, username: str, context: dict):
    normalized = str(username or "").strip()
    if not normalized:
        return queryset

    return queryset.filter(pk__in=PostLike.objects.filter(user__username=normalized).values("post_id"))


def resolve_liked_by_profile_filter(queryset, user_id: int | str | None, context: dict):
    if not user_id:
        return queryset

    return queryset.filter(pk__in=PostLike.objects.filter(user_id=user_id).values("post_id"))


def apply_liked_by_resource_filter(queryset, value, context: dict):
    normalized = str(value or "").strip()
    if not normalized:
        return queryset

    if normalized == "me":
        user = context.get("user")
        if not user or not getattr(user, "is_authenticated", False):
            return queryset.none()
        return queryset.filter(pk__in=PostLike.objects.filter(user=user).values("post_id"))

    if normalized.isdigit():
        return queryset.filter(pk__in=PostLike.objects.filter(user_id=int(normalized)).values("post_id"))

    return queryset.filter(pk__in=PostLike.objects.filter(user__username=normalized).values("post_id"))


def resolve_liked_posts_for_user(user: Any, context: dict) -> dict:
    return {
        "href": f"/api/posts?filter[likedBy]={user.id}",
        "filter": {
            "likedBy": str(user.id),
        },
    }
