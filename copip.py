#!/usr/bin/env python
"""
Create a conda-pip 'copip' development overlay.

Usage:
  mkcopip env_name
"""

# Stdlib imports

import os
import sys
import typing as T

from pathlib import Path
from subprocess import check_output as sh

# Config global constants
CONDA_BASE = Path(sh(['conda', 'info', '--base']).decode().strip())/'envs'
COPIP_DIR  = Path(__file__).parent
COPIP_ON   = Path('copipon.sh')
COPIP_OFF  = Path('copipoff.sh')


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
    copip_dir = CONDA_BASE/ename/'copip'
    acti_dir  = CONDA_BASE/ename/'etc/conda/activate.d'
    deac_dir  = CONDA_BASE/ename/'etc/conda/deactivate.d'

    if not (CONDA_BASE/ename).is_dir():
        print(f"Environment {ename} doesn't exist, exiting.", file=sys.stderr)
        return 64

    for d in [copip_dir, acti_dir, deac_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Symlink env. config scripts inside conda activ/deact directories
    for script, cdir in [(COPIP_ON, acti_dir), (COPIP_OFF, deac_dir)]:
        dest = cdir/script
        if not dest.is_file():
            os.link(COPIP_DIR/script, dest)

    print(f"Environment dev overlay `{ename}` ready at `{copip_dir}`")

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

    ename = '__tmp_copip_env__'
    copip  = CONDA_BASE/ename
    sh(f"conda create -n {ename} --yes")
    try:
        assert main([ename]) == 0
        assert copip.is_dir()

        for script, cdir in [(COPIP_ON, 'activate.d'),
                             (COPIP_OFF, 'deactivate.d')]:
            src = CONDA_BASE/ename/'etc/conda'/cdir/script
            assert src.is_file()
            assert src.samefile(COPIP_DIR/script)
    finally:
        sh(f"conda remove -n {ename} --all --yes")


# Main entry point
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
