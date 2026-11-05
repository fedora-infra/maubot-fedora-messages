# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unit tests for the message schema."""

import pytest
from jsonschema import ValidationError

from maubot_fedora_messages import GiveCookieV1, GiveCookieV2


def test_minimal(dummy_cookie):
    """
    Assert the message schema validates a message with the required fields.
    """
    message = GiveCookieV1(body=dummy_cookie)
    message.validate()
    assert message.agent_name == "dummy-user"


def test_missing_fields():
    """Assert an exception is actually raised on validation failure."""
    minimal_message = {
        "sender": "dummy",
        "recipient": "foobar",
    }
    message = GiveCookieV1(body=minimal_message)
    with pytest.raises(ValidationError):
        message.validate()


def test_str(dummy_cookie):
    """Assert __str__ produces a human-readable message."""
    expected_str = (
        "dummy-user gave a cookie to foobar. They now have 1 cookie(s), "
        "1 of which were obtained in the Fedora 39 release cycle"
    )
    message = GiveCookieV1(body=dummy_cookie)
    message.validate()
    assert expected_str == str(message)


def test_summary(dummy_cookie):
    """Assert the summary is correct."""
    message = GiveCookieV1(body=dummy_cookie)
    assert message.summary == "dummy-user gave a cookie to foobar"


def test_usernames(dummy_cookie):
    """Assert the usernames is correct."""
    message = GiveCookieV1(body=dummy_cookie)
    assert message.usernames == ["dummy-user", "foobar"]


def test_v2_minimal(dummy_cookie_v2):
    """
    Assert the v2 message schema validates a message with the required fields.
    """
    message = GiveCookieV2(body=dummy_cookie_v2)
    message.validate()
    assert message.topic == "maubot.cookie.give.v2"
    assert message.agent_name == "dummy-user"


@pytest.mark.parametrize("missing_field", ["sender_total", "sender_count_by_release"])
def test_v2_missing_sender_fields(dummy_cookie_v2, missing_field):
    """Assert the sender totals are required in v2."""
    body = {k: v for k, v in dummy_cookie_v2.items() if k != missing_field}
    message = GiveCookieV2(body=body)
    with pytest.raises(ValidationError):
        message.validate()


def test_v2_str(dummy_cookie_v2):
    """Assert __str__ produces a human-readable message."""
    expected_str = (
        "dummy-user gave a cookie to foobar. They now have 1 cookie(s), "
        "1 of which were obtained in the Fedora 39 release cycle. "
        "dummy-user has given 13 cookie(s) in total"
    )
    message = GiveCookieV2(body=dummy_cookie_v2)
    message.validate()
    assert expected_str == str(message)


def test_v2_summary(dummy_cookie_v2):
    """Assert the summary is correct."""
    message = GiveCookieV2(body=dummy_cookie_v2)
    assert message.summary == "dummy-user gave a cookie to foobar"


def test_v2_usernames(dummy_cookie_v2):
    """Assert the usernames is correct."""
    message = GiveCookieV2(body=dummy_cookie_v2)
    assert message.usernames == ["dummy-user", "foobar"]
