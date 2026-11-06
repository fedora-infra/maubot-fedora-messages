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


def test_sender_totals(dummy_cookie_with_sender_totals):
    """Assert sender totals are accepted on the v1 schema."""
    message = GiveCookieV1(body=dummy_cookie_with_sender_totals)
    message.validate()
    assert message.body["sender_total"] == 13
    assert message.body["sender_count_by_release"] == {"38": 12, "39": 1}


def test_sender_totals_keep_recipient_meaning(dummy_cookie_with_sender_totals):
    """Assert the original fields still describe the recipient."""
    message = GiveCookieV1(body=dummy_cookie_with_sender_totals)
    assert message.body["total"] == 1
    assert message.body["count_by_release"] == {"39": 1}


def test_str_with_sender_totals(dummy_cookie_with_sender_totals):
    """Assert added sender totals do not change the human-readable message."""
    expected_str = (
        "dummy-user gave a cookie to foobar. They now have 1 cookie(s), "
        "1 of which were obtained in the Fedora 39 release cycle"
    )
    message = GiveCookieV1(body=dummy_cookie_with_sender_totals)
    message.validate()
    assert expected_str == str(message)


@pytest.mark.parametrize("field", ["sender_total", "sender_count_by_release"])
def test_partial_sender_totals(dummy_cookie_with_sender_totals, field):
    """Assert each sender total is optional, so older messages still validate."""
    body = {k: v for k, v in dummy_cookie_with_sender_totals.items() if k != field}
    message = GiveCookieV1(body=body)
    message.validate()


@pytest.mark.parametrize(
    "field,value",
    [
        ("sender_total", "13"),
        ("sender_count_by_release", ["38", "39"]),
    ],
)
def test_sender_totals_types(dummy_cookie_with_sender_totals, field, value):
    """Assert sender totals are type-checked like the recipient totals."""
    message = GiveCookieV1(body={**dummy_cookie_with_sender_totals, field: value})
    with pytest.raises(ValidationError):
        message.validate()
