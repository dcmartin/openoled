#!/bin/bash
${0%/*}/i2c.sh  | jq -r '.i2c[]|select(.key==30)."3"=="33"'
