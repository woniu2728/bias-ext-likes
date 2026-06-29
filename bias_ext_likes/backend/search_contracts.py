from __future__ import annotations

from bias_core.extensions import (
    ExtensionSearchDriverDefinition,
    SearchFilterDefinition,
)

from bias_ext_likes.backend.constants import EXTENSION_ID
from bias_ext_likes.backend.search import (
    apply_liked_by_filter,
    parse_liked_by_search_filter,
)


def search_filter_definitions():
    return (
        SearchFilterDefinition(
            code="likedBy",
            label="按点赞用户过滤",
            module_id=EXTENSION_ID,
            target="post",
            parser=parse_liked_by_search_filter,
            applier=apply_liked_by_filter,
            syntax="likedBy:<username>",
            description="仅返回被指定用户点赞过的回复。",
        ),
    )


def search_driver_definitions():
    return (
        ExtensionSearchDriverDefinition(
            target="post",
            driver="database",
            filters=search_filter_definitions(),
            description="按点赞用户过滤回复搜索。",
        ),
    )
