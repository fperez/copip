#!/usr/bin/env bash

# Activate a conda/pip developer environment overlay.

PREFIX=$CONDA_PREFIX/copip

# Before further changes, save some variables we need to restore on deactivation.
export _PATH_COPIP_OLD=$PATH
export _PIP_USER_COPIP_OLD=$PIP_USER
export _PREFIX_COPIP_OLD=$PREFIX

# Make pip *always* install as if --user had been typed, and then configure
# various variables so packages installed this way are found for execution, use
# by Jupyter, etc.
export PIP_USER=True
export PREFIX
export PYTHONUSERBASE=$PREFIX
export PATH=$PREFIX/bin:$PATH
export JUPYTER_PATH=$PREFIX/share/jupyter:$JUPYTER_PATH

echo "*** Environment developer overlay active at PREFIX=$PREFIX"  # dbg

# TODO: This will require some extra utilities if we want to also manage multiple
# other environment variables.  For later.
#export_paths "$PREFIX"
