#!/usr/bin/env bash

# Deactivate a developer environment overlay.

export PATH=$_PATH_COPIP_OLD
export PIP_USER=$_PIP_USER_COPIP_OLD
export PREFIX=$_PREFIX_COPIP_OLD

unset PYTHONUSERBASE
