#!/usr/bin/env bash

# Activate a developer environment overlay.

EDEV_PREFIX=$HOME/usr/edev

PREFIX=$EDEV_PREFIX/$CONDA_DEFAULT_ENV

export PYTHONUSERBASE=$PREFIX
export _PATH_EDEV_OLD=$PATH
export PATH=$PREFIX/bin:$PATH

echo "Environment Developer Overlay ON"

#export_paths "$PREFIX"
