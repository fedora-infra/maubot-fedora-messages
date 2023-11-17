# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unit tests for the message schema."""

import pytest
from jsonschema import ValidationError

from maubot_fedora_messages import GiveCookieV1


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
