"""Media player platform for Pioneer Infrared integration."""

from __future__ import annotations

from typing import ClassVar, override

from homeassistant.components.infrared import InfraredEmitterConsumerEntity
from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .codes import (
    PIONEER_SOURCE_COMMANDS,
    PioneerReceiverCode,
    make_pioneer_receiver_command,
)
from .const import CONF_DEVICE_TYPE, CONF_INFRARED_EMITTER_ENTITY_ID, PioneerDeviceType
from .entity import PioneerIrEntity

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Pioneer IR media players from config entry."""
    infrared_emitter_entity_id = entry.data[CONF_INFRARED_EMITTER_ENTITY_ID]
    device_type = entry.data[CONF_DEVICE_TYPE]
    if device_type == PioneerDeviceType.RECEIVER:
        async_add_entities(
            [PioneerReceiverMediaPlayer(entry, infrared_emitter_entity_id)],
        )


class PioneerReceiverMediaPlayer(
    PioneerIrEntity, InfraredEmitterConsumerEntity, MediaPlayerEntity,
):
    """Pioneer receiver media player controlled by IR."""

    _attr_name = None
    _attr_assumed_state = True
    _attr_device_class = MediaPlayerDeviceClass.RECEIVER
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.VOLUME_STEP
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.SELECT_SOURCE
    )
    _attr_source_list: ClassVar[list[str]] = list(PIONEER_SOURCE_COMMANDS)
    _attr_state = MediaPlayerState.ON
    _attr_is_volume_muted = False

    def __init__(self, entry: ConfigEntry, infrared_emitter_entity_id: str) -> None:
        """Initialize Pioneer receiver media player."""
        super().__init__(entry, unique_id_suffix="media_player")
        self._infrared_emitter_entity_id = infrared_emitter_entity_id

    @override
    async def async_turn_on(self) -> None:
        await self._send_command(
            make_pioneer_receiver_command(PioneerReceiverCode.POWER_ON),
        )
        self._attr_state = MediaPlayerState.ON
        self.async_write_ha_state()

    @override
    async def async_turn_off(self) -> None:
        await self._send_command(
            make_pioneer_receiver_command(PioneerReceiverCode.POWER_OFF),
        )
        self._attr_state = MediaPlayerState.OFF
        self.async_write_ha_state()

    @override
    async def async_volume_up(self) -> None:
        await self._send_command(
            make_pioneer_receiver_command(PioneerReceiverCode.VOLUME_UP),
        )

    @override
    async def async_volume_down(self) -> None:
        await self._send_command(
            make_pioneer_receiver_command(PioneerReceiverCode.VOLUME_DOWN),
        )

    @override
    async def async_mute_volume(self, mute: bool) -> None:
        await self._send_command(
            make_pioneer_receiver_command(
                PioneerReceiverCode.MUTE_ON if mute else PioneerReceiverCode.MUTE_OFF,
            ),
        )
        self._attr_is_volume_muted = mute
        self.async_write_ha_state()

    @override
    async def async_select_source(self, source: str) -> None:
        await self._send_command(
            make_pioneer_receiver_command(PIONEER_SOURCE_COMMANDS[source]),
        )
        self._attr_source = source
        self._attr_state = MediaPlayerState.ON
        self.async_write_ha_state()
