# Pioneer Infrared for Home Assistant

Custom Home Assistant integration for Pioneer receiver IR control using the
first-class `infrared` entity platform introduced in Home Assistant 2026.4.

The integration supports Pioneer receiver power, mute, volume, source, and
tuner station commands from `esphome-pioneer-remote.yaml`.

It creates a Home Assistant config flow where you select:
1. The `infrared` emitter entity that is physically pointed at the Pioneer
   receiver.

## Installation

Use HACS as a custom integration repository, or copy
`custom_components/pioneer_infrared` into your Home Assistant `custom_components`
directory.

Restart Home Assistant, then add **Pioneer Infrared** from **Settings >
Devices & services > Add integration**.

Looking for Samsung TV support? See [ha-samsung-infrared](https://github.com/zapster/ha-samsung-infrared).

## Development

Local checks that do not require a Home Assistant checkout:

```bash
python -m compileall custom_components tests
```

The test suite expects Home Assistant 2026.4 or newer and the
`infrared-protocols` package.
