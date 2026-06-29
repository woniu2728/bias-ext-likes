from __future__ import annotations

from bias_core.extensions import NotificationsExtender


def notification_extender():
    return (
        NotificationsExtender()
        .type(
            "postLiked",
            label="回复被点赞",
            description="通知回复作者其内容被点赞。",
            icon="fas fa-thumbs-up",
            navigation_scope="post",
            preference_key="notify_post_liked",
            preference_label="回复被点赞通知",
            preference_description="当你的回复被其他用户点赞时通知你。",
        )
    )
