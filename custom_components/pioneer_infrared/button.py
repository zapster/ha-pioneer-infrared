"""Button platform for Pioneer Infrared integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import override

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.components.infrared import InfraredEmitterConsumerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .codes import (
    PioneerReceiverCode,
    make_pioneer_receiver_command,
)
from .const import CONF_DEVICE_TYPE, CONF_INFRARED_EMITTER_ENTITY_ID, PioneerDeviceType
from .entity import PioneerIrEntity

PARALLEL_UPDATES = 1


@dataclass(frozen=True, kw_only=True)
class PioneerIrButtonEntityDescription(ButtonEntityDescription):
    """Describes Pioneer IR button entity."""

    command_code: PioneerReceiverCode


PIONEER_RECEIVER_BUTTON_DESCRIPTIONS: tuple[PioneerIrButtonEntityDescription, ...] = (
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.POWER_ON,
        translation_key="power_on",
        command_code=PioneerReceiverCode.POWER_ON,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.POWER_OFF,
        translation_key="power_off",
        command_code=PioneerReceiverCode.POWER_OFF,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.POWER_TOGGLE,
        translation_key="power_toggle",
        command_code=PioneerReceiverCode.POWER_TOGGLE,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.MUTE_TOGGLE,
        translation_key="mute_toggle",
        command_code=PioneerReceiverCode.MUTE_TOGGLE,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.MUTE_ON,
        translation_key="mute_on",
        command_code=PioneerReceiverCode.MUTE_ON,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.MUTE_OFF,
        translation_key="mute_off",
        command_code=PioneerReceiverCode.MUTE_OFF,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.VOLUME_UP,
        translation_key="volume_up",
        command_code=PioneerReceiverCode.VOLUME_UP,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.VOLUME_DOWN,
        translation_key="volume_down",
        command_code=PioneerReceiverCode.VOLUME_DOWN,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.TUNER,
        translation_key="tuner",
        command_code=PioneerReceiverCode.TUNER,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.CD,
        translation_key="cd",
        command_code=PioneerReceiverCode.CD,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.TV,
        translation_key="tv",
        command_code=PioneerReceiverCode.TV,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.DVD,
        translation_key="dvd",
        command_code=PioneerReceiverCode.DVD,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.SAT_CBL,
        translation_key="sat_cbl",
        command_code=PioneerReceiverCode.SAT_CBL,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.GAME,
        translation_key="game",
        command_code=PioneerReceiverCode.GAME,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.BD,
        translation_key="bd",
        command_code=PioneerReceiverCode.BD,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.IPOD_USB,
        translation_key="ipod_usb",
        command_code=PioneerReceiverCode.IPOD_USB,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.STATION_1,
        translation_key="station_1",
        command_code=PioneerReceiverCode.STATION_1,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.STATION_2,
        translation_key="station_2",
        command_code=PioneerReceiverCode.STATION_2,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.STATION_3,
        translation_key="station_3",
        command_code=PioneerReceiverCode.STATION_3,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.STATION_4,
        translation_key="station_4",
        command_code=PioneerReceiverCode.STATION_4,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.STATION_5,
        translation_key="station_5",
        command_code=PioneerReceiverCode.STATION_5,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.STATION_6,
        translation_key="station_6",
        command_code=PioneerReceiverCode.STATION_6,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.STATION_7,
        translation_key="station_7",
        command_code=PioneerReceiverCode.STATION_7,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.STATION_8,
        translation_key="station_8",
        command_code=PioneerReceiverCode.STATION_8,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.STATION_9,
        translation_key="station_9",
        command_code=PioneerReceiverCode.STATION_9,
    ),
    PioneerIrButtonEntityDescription(
        key=PioneerReceiverCode.STATION_10,
        translation_key="station_10",
        command_code=PioneerReceiverCode.STATION_10,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Pioneer IR buttons from a config entry."""
    infrared_emitter_entity_id = entry.data[CONF_INFRARED_EMITTER_ENTITY_ID]
    device_type = entry.data[CONF_DEVICE_TYPE]
    if device_type != PioneerDeviceType.RECEIVER:
        return
    async_add_entities(
        [
            PioneerIrButton(entry, infrared_emitter_entity_id, description)
            for description in PIONEER_RECEIVER_BUTTON_DESCRIPTIONS
        ],
    )


class PioneerIrButton(PioneerIrEntity, InfraredEmitterConsumerEntity, ButtonEntity):
    """Pioneer IR button entity."""

    entity_description: PioneerIrButtonEntityDescription

    def __init__(
        self,
        entry: ConfigEntry,
        infrared_emitter_entity_id: str,
        description: PioneerIrButtonEntityDescription,
    ) -> None:
        """Initialize Pioneer IR button."""
        super().__init__(entry, unique_id_suffix=description.key)
        self._infrared_emitter_entity_id = infrared_emitter_entity_id
        self.entity_description = description

    @override
    async def async_press(self) -> None:
        """Press the button."""
        await self._send_command(
            make_pioneer_receiver_command(self.entity_description.command_code),
        )
