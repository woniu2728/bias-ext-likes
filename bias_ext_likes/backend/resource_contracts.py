from __future__ import annotations

from bias_core.extensions import (
    ResourceEndpointDefinition,
    ResourceFieldDefinition,
    ResourceFilterDefinition,
    ResourceRelationshipDefinition,
)

from bias_ext_likes.backend.constants import EXTENSION_ID
from bias_ext_likes.backend.handlers import dispatch_post_like_mutation
from bias_ext_likes.backend.resources import (
    post_like_count_annotate_resolver,
    post_like_preload_resolver,
    post_likes_relationship_preload_resolver,
    resolve_post_is_liked,
    resolve_post_like_count,
    resolve_post_likes,
)
from bias_ext_likes.backend.search import apply_liked_by_resource_filter
from bias_ext_likes.backend.services import resolve_post_can_like


def post_resource_field_definitions():
    return (
        ResourceFieldDefinition(
            resource="post",
            field="like_count",
            module_id=EXTENSION_ID,
            resolver=resolve_post_like_count,
            description="当前回复的点赞数量。",
            annotate_resolver=post_like_count_annotate_resolver,
        ),
        ResourceFieldDefinition(
            resource="post",
            field="is_liked",
            module_id=EXTENSION_ID,
            resolver=resolve_post_is_liked,
            description="当前用户是否已点赞该回复。",
            preload_resolver=post_like_preload_resolver,
        ),
        ResourceFieldDefinition(
            resource="post",
            field="can_like",
            module_id=EXTENSION_ID,
            resolver=resolve_post_can_like,
            description="当前用户是否可以点赞该回复。",
        ),
    )


def post_resource_relationship_definitions():
    return (
        ResourceRelationshipDefinition(
            resource="post",
            relationship="likes",
            module_id=EXTENSION_ID,
            resolver=resolve_post_likes,
            description="点赞该回复的用户列表。",
            preload_resolver=post_likes_relationship_preload_resolver,
            resource_type="post_user",
            many=True,
        ),
    )


def post_resource_filter_definitions():
    return (
        ResourceFilterDefinition(
            resource="post",
            filter="likedBy",
            module_id=EXTENSION_ID,
            handler=apply_liked_by_resource_filter,
            description="仅返回被指定用户点赞过的回复。",
        ),
    )


def post_resource_endpoints():
    return (
        ResourceEndpointDefinition(
            resource="post",
            endpoint="like",
            module_id=EXTENSION_ID,
            handler=dispatch_post_like_mutation,
            methods=("POST", "DELETE"),
            path="posts/{object_id}/like",
            absolute_path=True,
            auth_required=True,
        ),
    )
