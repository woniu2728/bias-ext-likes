from __future__ import annotations

from bias_core.extensions import ExtensionModelRelationDefinition

from bias_ext_likes.backend.constants import POST_MODEL, USER_MODEL
from bias_ext_likes.backend.models import PostLike


def model_relation_definitions():
    return (
        ExtensionModelRelationDefinition(
            model=POST_MODEL,
            name="likes",
            resolver=lambda post: [
                like.user
                for like in post.likes.select_related("user").all()
            ],
            relation_type="belongsToMany",
            related_model=USER_MODEL,
            description="点赞该回复的用户。",
            inject_attribute=False,
        ),
    )


def owned_models():
    return (
        (
            PostLike,
            "帖子点赞记录由 likes 扩展拥有。",
        ),
    )
