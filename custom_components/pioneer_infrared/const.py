"""Constants for the Pioneer Infrared integration."""

from __future__ import annotations

from enum import StrEnum

DOMAIN = "pioneer_infrared"

CONF_DEVICE_TYPE = "device_type"
CONF_INFRARED_EMITTER_ENTITY_ID = "infrared_emitter_entity_id"


class PioneerDeviceType(StrEnum):
    """Pioneer device types."""

    RECEIVER = "receiver"
