from django.apps import AppConfig


class LikesExtensionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    label = "likes"
    name = "bias_ext_likes.backend"
    verbose_name = "Bias Likes Extension"

