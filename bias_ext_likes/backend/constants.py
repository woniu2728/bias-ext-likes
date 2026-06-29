from __future__ import annotations

from bias_core.extensions import RuntimeModel


EXTENSION_ID = "likes"
POST_MODEL = RuntimeModel("content.posts", description="content 基础包提供的帖子模型。")
USER_MODEL = RuntimeModel("users.service", description="users 扩展提供的用户模型。")
