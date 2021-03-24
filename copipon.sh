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
# Note - ideally JUPYTER_PATH wouldn't need to be set separately of other Python
# variables, as e.g. JupyterLab extensions can be pip-installed. But the process
# of finding their non-python pieces is complex and how to do it without extra
# info isn't settled, so for now we need an extra explicit variable.
# See https://github.com/jupyter/jupyter_core/pull/209 for lots of details...
export JUPYTER_PATH=$PREFIX/share/jupyter:$JUPYTER_PATH

echo "*** Environment developer overlay active at PREFIX=$PREFIX"  # dbg

# TODO: This will require some extra utilities if we want to also manage multiple
# other environment variables.  For later.
#export_paths "$PREFIX"
