# &#x1f5bc; `openoled` - OLED control

This repository contains software to control both `i2c` and `spi` OLED displays connected to a RaspberryPi on Raspian Buster.
The [Open Horizon](http://github.com/dcmartin/open-horizon) _service_ [`oled`](http://github.com/dcmartin/open-horizon/tree/master/services/oled/README.md)  utilizes this repository to build Docker containers.  Please refer to the [Dockerfile](http://github.com/dcmartin/open-horizon/tree/master/services/oled/Dockerfile) for details.

## About
OpenOLED is an open source *OLED* library written in C and Python.  The library displays images and text to OLED panels.

## Installation

```
sudo apt update -qq -y && sudo apt install -qq -y git
git clone http://github.com/dcmartin/openoled.git
cd openoled
sudo ./sh/get.required.sh
make
```

&#9995; Remember to specify **`http://github.com/dcmartin/openoled.git`** as the repository.

## Usage
OpenOLED includes command line utilities for the `i2c` and `spi` OLED panels.  In addition, there is an example Python _Flask_ server to display pictures and annotations.

## Example

```
```

# Changelog & Releases

Releases are based on Semantic Versioning, and use the format
of ``MAJOR.MINOR.PATCH``. In a nutshell, the version will be incremented
based on the following:

- ``MAJOR``: Incompatible or major changes.
- ``MINOR``: Backwards-compatible new features and enhancements.
- ``PATCH``: Backwards-compatible bugfixes and package updates.

# Authors & contributors

David C Martin (github@dcmartin.com)
