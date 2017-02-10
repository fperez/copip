#!/usr/bin/env python
"""
Create a developer environment overlay.

Usage:
  mkedev env_name
"""

# Stdlib imports

import os
import sys
import typing as T

from pathlib import Path

# Config global constants

BIN        = Path(os.path.expandvars('$HOME/usr/bin'))
CONDA_BASE = Path(os.path.expandvars('$HOME/usr/conda/envs'))
EDEV_BASE  = Path(os.path.expandvars('$HOME/usr/edev'))
EDEV_ON    = Path('edevon.sh')
EDEV_OFF   = Path('edevoff.sh')


# Function definitions
def main(args: T.Optional[list]=None) -> int:
    if args is None:
        args = sys.argv[1:]

    try:
        ename = args[0]
    except IndexError:
        print(__doc__, file=sys.stderr)
        return 1

    # Create directories for holding installed files and env. config
    edev_dir = EDEV_BASE/ename
    acti_dir = CONDA_BASE/ename/'etc/conda/activate.d'
    deac_dir = CONDA_BASE/ename/'etc/conda/deactivate.d'

    if not (CONDA_BASE/ename).is_dir():
        print(f"Environment {ename} doesn't exist, exiting.", file=sys.stderr)
        return 1

    for d in [edev_dir, acti_dir, deac_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Symlink env. config scripts inside conda activ/deact directories
    eon  = acti_dir/EDEV_ON
    eoff = deac_dir/EDEV_OFF

    if not eon.is_symlink():
        eon.symlink_to(BIN/EDEV_ON)
    if not eoff.is_symlink():
        eoff.symlink_to(BIN/EDEV_OFF)

    print(f"Environment dev overlay `{ename}` ready at `{edev_dir}`")

    return 0


# Unit tests
def test_noenv():
    assert main(['__BADENV_NAME_zyxw__']) == 1


def test_no_args():
    assert main([]) == 1


def test_normal():
    import functools
    import subprocess

    sh = functools.partial(subprocess.run, shell=True, check=True)

    ename = '__tmp_edev_env__'
    sh(f"conda create -n {ename} --yes")
    try:
        assert main([ename]) == 0
        assert (EDEV_BASE/ename).is_dir()

        for script, cdir in [(EDEV_ON, 'activate.d'),
                             (EDEV_OFF, 'deactivate.d')]:
            src = CONDA_BASE/ename/'etc/conda'/cdir/script
            assert src.is_symlink()
            assert src.samefile(script)
    finally:
        sh(f"conda remove -n {ename} --all --yes")


# Main entry point
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
