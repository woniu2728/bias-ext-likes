from __future__ import annotations

from bias_core.extensions import setting_field


def setting_definitions():
    return (
        setting_field({
            "key": "like_own_post",
            "label": "允许点赞自己的回复",
            "type": "boolean",
            "default": False,
            "help_text": "开启后用户可以给自己的回复点赞。",
            "order": 10,
        }),
    )
