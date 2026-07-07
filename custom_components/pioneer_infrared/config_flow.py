"""Config flow for Pioneer Infrared integration."""

from typing import Any, override

import voluptuous as vol
from homeassistant.components.infrared import (
    DOMAIN as INFRARED_DOMAIN,
)
from homeassistant.components.infrared import (
    async_get_emitters,
)
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
)

from .const import (
    CONF_DEVICE_TYPE,
    CONF_INFRARED_EMITTER_ENTITY_ID,
    DOMAIN,
    PioneerDeviceType,
)


class PioneerIrConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle config flow for Pioneer Infrared."""

    VERSION = 1

    @override
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        emitter_entity_ids = async_get_emitters(self.hass)
        if not emitter_entity_ids:
            return self.async_abort(reason="no_emitters")

        if user_input is not None:
            entity_id = user_input[CONF_INFRARED_EMITTER_ENTITY_ID]

            await self.async_set_unique_id(
                f"pioneer_infrared_receiver_{entity_id}",
            )
            self._abort_if_unique_id_configured()

            user_input[CONF_DEVICE_TYPE] = PioneerDeviceType.RECEIVER

            ent_reg = er.async_get(self.hass)
            registry_entry = ent_reg.async_get(entity_id)
            entity_name = (
                registry_entry.name or registry_entry.original_name or entity_id
                if registry_entry
                else entity_id
            )
            title = f"Pioneer Receiver via {entity_name}"

            return self.async_create_entry(title=title, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_INFRARED_EMITTER_ENTITY_ID,
                    ): EntitySelector(
                        EntitySelectorConfig(
                            domain=INFRARED_DOMAIN,
                            include_entities=emitter_entity_ids,
                        ),
                    ),
                },
            ),
        )
