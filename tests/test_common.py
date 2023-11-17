# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unit tests for common properties of the message schemas."""

from maubot_fedora_messages import GiveCookieV1


def test_properties(dummy_cookie):
    """Assert some properties are correct."""
    message = GiveCookieV1(body=dummy_cookie)

    assert message.app_name == "Maubot Fedora"
    assert message.app_icon == "https://apps.fedoraproject.org/img/icons/maubot-fedora.png"
    assert message.agent_name == "dummy-user"
    assert message.agent_avatar == (
        "https://seccdn.libravatar.org/avatar/"
        "18e8268125372e35f95ef082fd124e9274d46916efe2277417fa5fecfee31af1"
        "?s=64&d=retro"
    )
