"""Pioneer receiver command codes."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from infrared_protocols.commands import Command

from .protocols import PioneerCommand


@dataclass(frozen=True, slots=True)
class PioneerCodeSpec:
    """Pioneer command code pair."""

    rc_code_1: int
    rc_code_2: int = 0


class PioneerReceiverCode(StrEnum):
    """Pioneer receiver command codes from esphome-pioneer-remote.yaml."""

    POWER_ON = "power_on"
    POWER_OFF = "power_off"
    POWER_TOGGLE = "power_toggle"
    MUTE_TOGGLE = "mute_toggle"
    MUTE_ON = "mute_on"
    MUTE_OFF = "mute_off"
    VOLUME_UP = "volume_up"
    VOLUME_DOWN = "volume_down"
    TUNER = "tuner"
    CD = "cd"
    TV = "tv"
    DVD = "dvd"
    SAT_CBL = "sat_cbl"
    GAME = "game"
    BD = "bd"
    IPOD_USB = "ipod_usb"
    STATION_1 = "station_1"
    STATION_2 = "station_2"
    STATION_3 = "station_3"
    STATION_4 = "station_4"
    STATION_5 = "station_5"
    STATION_6 = "station_6"
    STATION_7 = "station_7"
    STATION_8 = "station_8"
    STATION_9 = "station_9"
    STATION_10 = "station_10"


PIONEER_RECEIVER_CODES: dict[PioneerReceiverCode, PioneerCodeSpec] = {
    PioneerReceiverCode.POWER_ON: PioneerCodeSpec(0xA51A),
    PioneerReceiverCode.POWER_OFF: PioneerCodeSpec(0xA51B),
    PioneerReceiverCode.POWER_TOGGLE: PioneerCodeSpec(0xA51C),
    PioneerReceiverCode.MUTE_TOGGLE: PioneerCodeSpec(0xA512),
    PioneerReceiverCode.MUTE_ON: PioneerCodeSpec(0xA551),
    PioneerReceiverCode.MUTE_OFF: PioneerCodeSpec(0xA552),
    PioneerReceiverCode.VOLUME_UP: PioneerCodeSpec(0xA50A),
    PioneerReceiverCode.VOLUME_DOWN: PioneerCodeSpec(0xA50B),
    PioneerReceiverCode.TUNER: PioneerCodeSpec(0xA547),
    PioneerReceiverCode.CD: PioneerCodeSpec(0xA54C),
    PioneerReceiverCode.TV: PioneerCodeSpec(0xA50C),
    PioneerReceiverCode.DVD: PioneerCodeSpec(0xA585),
    PioneerReceiverCode.SAT_CBL: PioneerCodeSpec(0xA510),
    PioneerReceiverCode.GAME: PioneerCodeSpec(0xA55C, 0xA5C5),
    PioneerReceiverCode.BD: PioneerCodeSpec(0xA55C, 0xA5C0),
    PioneerReceiverCode.IPOD_USB: PioneerCodeSpec(0xA59E, 0xA5CB),
    PioneerReceiverCode.STATION_1: PioneerCodeSpec(0x2501),
    PioneerReceiverCode.STATION_2: PioneerCodeSpec(0x2502),
    PioneerReceiverCode.STATION_3: PioneerCodeSpec(0x2503),
    PioneerReceiverCode.STATION_4: PioneerCodeSpec(0x2504),
    PioneerReceiverCode.STATION_5: PioneerCodeSpec(0x2505),
    PioneerReceiverCode.STATION_6: PioneerCodeSpec(0x2506),
    PioneerReceiverCode.STATION_7: PioneerCodeSpec(0x2507),
    PioneerReceiverCode.STATION_8: PioneerCodeSpec(0x2508),
    PioneerReceiverCode.STATION_9: PioneerCodeSpec(0x2509),
    PioneerReceiverCode.STATION_10: PioneerCodeSpec(0x2500),
}

PIONEER_SOURCE_COMMANDS: dict[str, PioneerReceiverCode] = {
    "Tuner": PioneerReceiverCode.TUNER,
    "CD": PioneerReceiverCode.CD,
    "TV": PioneerReceiverCode.TV,
    "DVD": PioneerReceiverCode.DVD,
    "SAT/CBL": PioneerReceiverCode.SAT_CBL,
    "Game": PioneerReceiverCode.GAME,
    "BD": PioneerReceiverCode.BD,
    "iPod/USB": PioneerReceiverCode.IPOD_USB,
}


def make_pioneer_receiver_command(code: PioneerReceiverCode) -> Command:
    """Make a Pioneer receiver command."""
    spec = PIONEER_RECEIVER_CODES[code]
    return PioneerCommand(rc_code_1=spec.rc_code_1, rc_code_2=spec.rc_code_2)
