"""Tests for Pioneer IR protocol encoder."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

pytest.importorskip("infrared_protocols")

_PROTOCOLS_PATH = (
    Path(__file__).parents[1]
    / "custom_components"
    / "pioneer_infrared"
    / "protocols.py"
)
_SPEC = importlib.util.spec_from_file_location(
    "pioneer_infrared_protocols", _PROTOCOLS_PATH,
)
assert _SPEC is not None
assert _SPEC.loader is not None
protocols = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(protocols)


def test_pioneer_command_timings() -> None:
    """Test Pioneer command encoder timing shape."""
    command = protocols.PioneerCommand(rc_code_1=0xA51A, repeat_count=0)

    assert command.modulation == protocols.PIONEER_MODULATION
    timings = command.get_raw_timings()
    assert timings[:2] == [9000, -4500]
    assert len(timings) == 67
    assert timings[-1] == 560


def test_pioneer_two_part_command_timings() -> None:
    """Test Pioneer two-part command encoder timing shape."""
    command = protocols.PioneerCommand(
        rc_code_1=0xA55C, rc_code_2=0xA5C5, repeat_count=0,
    )

    timings = command.get_raw_timings()
    assert len(timings) == 135
    assert timings[66] == 560
    assert timings[67] == -25500
    assert timings[68:70] == [9000, -4500]


def test_repeats_add_inter_frame_space() -> None:
    """Test repeated frames contain the configured inter-frame space."""
    timings = protocols.PioneerCommand(
        rc_code_1=0xA51A, repeat_count=1,
    ).get_raw_timings()

    assert len(timings) == 135
    assert timings[66] == 560
    assert timings[67] == -10000
    assert timings[68:70] == [9000, -4500]
