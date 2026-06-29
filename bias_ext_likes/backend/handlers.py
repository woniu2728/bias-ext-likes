from __future__ import annotations

from django.core.exceptions import PermissionDenied

from bias_core.extensions.platform import api_error
from bias_core.extensions.runtime import (
    like_runtime_post,
    unlike_runtime_post,
)
from bias_ext_likes.backend.services import PostActionContextNotFound


def dispatch_post_like_mutation(context):
    method = str(context.get("method") or "GET").upper()
    if method == "DELETE":
        return dispatch_post_unlike(context)
    return dispatch_post_like(context)


def dispatch_post_like(context):
    post_id = _post_object_id(context)
    try:
        like_runtime_post(post_id, context["user"])
        return {"message": "点赞成功"}
    except PermissionDenied as e:
        return api_error(str(e), status=403)
    except PostActionContextNotFound:
        return api_error("帖子不存在", status=404)
    except ValueError as e:
        return api_error(str(e), status=400)


def dispatch_post_unlike(context):
    post_id = _post_object_id(context)
    try:
        unlike_runtime_post(post_id, context["user"])
        return {"message": "取消点赞成功"}
    except PermissionDenied as e:
        return api_error(str(e), status=403)
    except PostActionContextNotFound:
        return api_error("帖子不存在", status=404)
    except ValueError as e:
        return api_error(str(e), status=400)


def _post_object_id(context) -> int:
    try:
        return int(context.get("object_id") or 0)
    except (TypeError, ValueError):
        return 0

