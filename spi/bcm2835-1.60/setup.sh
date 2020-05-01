#!/bin/bash

if [ -z "$(command -v automake)" ]; then echo "Please install automake; sudo apt install -qq -y automake"; exit 1; fi

./configure
make install
