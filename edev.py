#!/usr/bin/env python
"""
Create a developer environment overlay.

Usage:
  mkedev env_name
"""

# Stdlib imports

import sys
import typing as T

from pathlib import Path

# Config global constants

BIN        = Path('~/usr/bin').expanduser()
CONDA_BASE = Path('~/usr/conda/envs').expanduser()
EDEV_BASE  = Path('~/usr/edev').expanduser()
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
        return 64

    # Create directories for holding installed files and env. config
    edev_dir = EDEV_BASE/ename
    acti_dir = CONDA_BASE/ename/'etc/conda/activate.d'
    deac_dir = CONDA_BASE/ename/'etc/conda/deactivate.d'

    if not (CONDA_BASE/ename).is_dir():
        print(f"Environment {ename} doesn't exist, exiting.", file=sys.stderr)
        return 64

    for d in [edev_dir, acti_dir, deac_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Symlink env. config scripts inside conda activ/deact directories
    for script, cdir in [(EDEV_ON, acti_dir), (EDEV_OFF, deac_dir)]:
        src = cdir/script
        if not src.is_symlink():
            src.symlink_to(BIN/script)

    print(f"Environment dev overlay `{ename}` ready at `{edev_dir}`")

    return 0


# Unit tests
def test_no_args():
    assert main([]) == 64


def test_noenv():
    assert main(['__BADENV_NAME_zyxw__']) == 64


def test_normal():
    import functools
    import subprocess

    sh = functools.partial(subprocess.run, shell=True, check=True)

    ename = '__tmp_edev_env__'
    edev  = EDEV_BASE/ename
    sh(f"conda create -n {ename} --yes")
    try:
        assert main([ename]) == 0
        assert edev.is_dir()

        for script, cdir in [(EDEV_ON, 'activate.d'),
                             (EDEV_OFF, 'deactivate.d')]:
            src = CONDA_BASE/ename/'etc/conda'/cdir/script
            assert src.is_symlink()
            assert src.samefile(script)
    finally:
        edev.rmdir()
        sh(f"conda remove -n {ename} --all --yes")


# Main entry point
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
