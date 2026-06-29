from bias_ext_likes.backend.extenders import (
    event_extenders,
    forum_extenders,
    frontend_extenders,
    model_extenders,
    optional_integration_extenders,
    policy_extenders,
    resource_extenders,
    search_extenders,
    service_extenders,
    settings_extenders,
)


def extend():
    return [
        *frontend_extenders(),
        *forum_extenders(),
        *event_extenders(),
        *optional_integration_extenders(),
        *settings_extenders(),
        *search_extenders(),
        *policy_extenders(),
        *service_extenders(),
        *model_extenders(),
        *resource_extenders(),
    ]
