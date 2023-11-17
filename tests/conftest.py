# SPDX-FileCopyrightText: 2023 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import pytest


@pytest.fixture
def dummy_cookie():
    return {
        "sender": "dummy-user",
        "recipient": "foobar",
        "fedora_release": "39",
        "total": 1,
        "count_by_release": {"39": 1},
    }
