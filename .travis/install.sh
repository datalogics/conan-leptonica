#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    brew update || brew update
    brew install cmake || true
    brew install pkg-config || true
else
    sudo apt-get install -y pkg-config
fi

pip install conan --upgrade
pip install conan_package_tools bincrafters_package_tools

conan user
