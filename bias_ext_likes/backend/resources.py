from __future__ import annotations

from django.db.models import Count, Exists, IntegerField, OuterRef, Prefetch, Subquery
from django.db.models.functions import Coalesce

from bias_ext_likes.backend.models import PostLike


def serialize_runtime_user(*args, **kwargs):
    from bias_core.extensions.runtime import serialize_runtime_user as runtime_serialize_user

    return runtime_serialize_user(*args, **kwargs)


def post_like_preload_resolver(context: dict):
    prefetches = []
    user = context.get("user")
    if user and user.is_authenticated:
        # is_liked is annotated via Exists; keep a cache only for callers that
        # explicitly work with prefetched relations on legacy resource paths.
        prefetches.append(_post_likes_prefetch(user=user, to_attr="viewer_likes_cache"))
    return (), tuple(prefetches)


def post_likes_relationship_preload_resolver(context: dict):
    return (), (_post_likes_prefetch(to_attr="likes_cache"),)


def post_like_count_annotate_resolver(context: dict) -> dict:
    user = context.get("user")
    annotations = {
        "likes_count": Coalesce(
            Subquery(
                PostLike.objects
                .filter(post_id=OuterRef("pk"))
                .order_by()
                .values("post_id")
                .annotate(total=Count("id"))
                .values("total")[:1],
                output_field=IntegerField(),
            ),
            0,
        )
    }
    if user and getattr(user, "is_authenticated", False):
        annotations["viewer_has_liked"] = Exists(PostLike.objects.filter(post_id=OuterRef("pk"), user=user))
    return annotations


def resolve_post_like_count(post, context: dict) -> int:
    annotated_count = getattr(post, "likes_count", None)
    if annotated_count is not None:
        return int(annotated_count or 0)
    cached = getattr(post, "likes_cache", None)
    if cached is not None:
        return len(cached)
    return PostLike.objects.filter(post_id=post.id).count()


def resolve_post_is_liked(post, context: dict) -> bool:
    annotated = getattr(post, "viewer_has_liked", None)
    if annotated is not None:
        return bool(annotated)
    cached = getattr(post, "viewer_likes_cache", None)
    if cached is not None:
        return bool(cached)
    user = context.get("user")
    if not user or not user.is_authenticated:
        return False
    return PostLike.objects.filter(post_id=post.id, user=user).exists()


def resolve_post_likes(post, context: dict) -> list[dict]:
    cached = getattr(post, "likes_cache", None)
    likes = cached if cached is not None else PostLike.objects.filter(post_id=post.id).select_related("user")
    return [
        serialize_runtime_user(like.user, resource="post_user", context=context)
        for like in likes
        if getattr(like, "user", None)
    ]


def _post_likes_prefetch(*, to_attr: str, user=None):
    queryset = PostLike.objects.select_related("user")
    if user is not None:
        queryset = queryset.filter(user=user)
    return Prefetch("likes", queryset=queryset, to_attr=to_attr)


