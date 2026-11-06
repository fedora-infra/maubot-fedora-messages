# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import pytest


@pytest.fixture
def dummy_cookie():
    """A v1 message published before sender totals were added."""
    return {
        "sender": "dummy-user",
        "recipient": "foobar",
        "fedora_release": "39",
        "total": 1,
        "count_by_release": {"39": 1},
    }


@pytest.fixture
def dummy_cookie_with_sender_totals(dummy_cookie):
    """A v1 message published after sender totals were added."""
    return {
        **dummy_cookie,
        "sender_total": 13,
        "sender_count_by_release": {"38": 12, "39": 1},
    }
