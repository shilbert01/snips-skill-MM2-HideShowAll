# Snips-skill-MM2-HideShowAll

This is an app for [Snips.ai](https://snips.ai/) that allows the user to hide, show all modules on [MagicMirror²](https://github.com/MichMich/MagicMirror). 

It is based on the [hide, show, move module](https://github.com/maxbachmann-snips/MM2-HideShowMove) by maxbachmann

## Installation 
The following instructions assume an installation according to [this](https://github.com/maxbachmann-magicmirror2/MMM-HideShowMove) guide.

The app is avaible in the skill store and needs to be added to a assistant in the according language. A instruction on how to setup a assistant and add a app can be found [here](https://snips.gitbook.io/getting-started/install-an-assistant)
The app is currently avaible in following languages:

| language  | link to the app in the skill store  |
|---|---|
| `German`  | [MMM-SnipsHideShow](https://console.snips.ai/store/de/skill_kz69bqq1x4y)|

## Configuration 

IP address of device that mqtt enabled mqtt-mm2-bridge (in other words MagicMirror2) is running on

`MagicMirror2_mqtt_ip=`

Site id of the satellite(s) the mmm-snipshideshow module should react on. Set to "all" to activate it on all devices
`site_id=`

## Contributing Guidelines

Contributions of all kinds are welcome, not only in the form of code but also with regards bug reports and documentation.

Please keep the following in mind:

- **Bug Reports**:  Make sure you're running the latest version. If the issue(s) still persist: please open a clearly documented issue with a clear title.
- **Minor Bug Fixes**: Please send a pull request with a clear explanation of the issue or a link to the issue it solves.
- **Major Bug Fixes**: please discuss your approach in an GitHub issue before you start to alter a big part of the code.
- **New Features**: please please discuss in a GitLab issue before you start to alter a big part of the code. Without discussion upfront, the pull request will not be accepted / merged.

## Planned
1. English version
