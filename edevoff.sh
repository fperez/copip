#!/usr/bin/env bash

# Deactivate a developer environment overlay.

export PATH=$_PATH_EDEV_OLD
export PIP_USER=$_PIP_USER_EDEV_OLD
export PREFIX=$_PREFIX_EDEV_OLD

unset PYTHONUSERBASE
