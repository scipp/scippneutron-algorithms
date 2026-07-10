# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2026 Scipp contributors (https://github.com/scipp)

"""Tests of package integrity."""

import scippneutron_algorithms as pkg
import scippneutron_algorithms.normalization


def test_has_version() -> None:
    assert hasattr(pkg, "__version__")
