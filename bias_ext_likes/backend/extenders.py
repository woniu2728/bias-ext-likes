from __future__ import annotations

from bias_core.extensions import (
    ApiResourceExtender,
    ConditionalExtender,
    EventListenersExtender,
    ForumCapabilitiesExtender,
    LifecycleExtender,
    ModelExtender,
    PolicyExtender,
    SearchDriverExtender,
    ServiceProviderExtender,
    SettingsExtender,
)

from bias_ext_likes.backend.frontend import frontend_extender
from bias_ext_likes.backend.listener_contracts import event_listener_definitions
from bias_ext_likes.backend.model_contracts import model_relation_definitions, owned_models
from bias_ext_likes.backend.notification_contracts import notification_extender
from bias_ext_likes.backend.resource_contracts import (
    post_resource_endpoints,
    post_resource_field_definitions,
    post_resource_filter_definitions,
    post_resource_relationship_definitions,
)
from bias_ext_likes.backend.runtime import like_service_provider
from bias_ext_likes.backend.search_contracts import search_driver_definitions, search_filter_definitions
from bias_ext_likes.backend.services import LikePostPolicy
from bias_ext_likes.backend.settings import setting_definitions


def frontend_extenders():
    return (frontend_extender(),)


def forum_extenders():
    return (
        ForumCapabilitiesExtender(
            search_filters=search_filter_definitions(),
        ),
    )


def event_extenders():
    return ()


def notification_integration_extenders():
    return (
        notification_extender(),
        EventListenersExtender(
            listeners=event_listener_definitions(),
        ),
    )


def optional_integration_extenders():
    return (
        ConditionalExtender().when_extension_enabled("notifications", notification_integration_extenders),
    )


def settings_extenders():
    return (
        SettingsExtender(fields=setting_definitions()).default("like_own_post", False),
    )


def search_extenders():
    return (
        SearchDriverExtender(
            drivers=search_driver_definitions(),
        ),
    )


def policy_extenders():
    return (
        PolicyExtender(mounts=(("post.like", LikePostPolicy),)),
    )


def model_extenders():
    extender = ModelExtender(
        relations=model_relation_definitions(),
    )
    for model, description in owned_models():
        extender = extender.owns(model, description=description)
    return (extender,)


def resource_extenders():
    return (
        ApiResourceExtender("post")
        .fields(post_resource_field_definitions)
        .relationships(post_resource_relationship_definitions)
        .filters(post_resource_filter_definitions)
        .endpoints(post_resource_endpoints)
        .add_default_include(("index", "show"), ("likes",)),
    )


def service_extenders():
    return (
        ServiceProviderExtender(
            key="likes.service",
            provider=like_service_provider,
        ),
        LifecycleExtender(),
    )
