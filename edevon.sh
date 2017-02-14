#!/usr/bin/env bash

# Activate a developer environment overlay.

EDEV_PREFIX=$HOME/usr/edev
PREFIX=$EDEV_PREFIX/$CONDA_DEFAULT_ENV

# Save some variables we need to restore on deactivation
export _PATH_EDEV_OLD=$PATH
export _PIP_USER_EDEV_OLD=$PIP_USER
export _PREFIX_EDEV_OLD=$PREFIX

# Make pip *always* install as if --user had been typed
export PATH=$PREFIX/bin:$PATH
export PIP_USER=True
export PREFIX
export PYTHONUSERBASE=$PREFIX

echo "*** Environment developer overlay active"  # dbg

# This will require some extra utilities if we want to also manage multiple
# other environment variables.  For later.
#export_paths "$PREFIX"
