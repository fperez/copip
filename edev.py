#!/usr/bin/env python
"""
Create a developer environment overlay.

Usage:
  mkedev env_name
"""

import os
import sys
import typing as T

from pathlib import Path

# Config global constants

BIN        = Path(os.path.expandvars('$HOME/usr/bin'))
CONDA_BASE = Path(os.path.expandvars('$HOME/usr/conda/envs'))
EDEV_BASE  = Path(os.path.expandvars('$HOME/usr/edev'))


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

    for d in [edev_dir, acti_dir, deac_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Symlink env. config scripts inside conda activ/deact directories
    eon  = acti_dir/'edevon.sh'
    eoff = deac_dir/'edevoff.sh'

    if not eon.is_symlink():
        eon.symlink_to(BIN/'edevon.sh')
    if not eoff.is_symlink():
        eoff.symlink_to(BIN/'edevoff.sh')

    print(f"Environment dev overlay `{ename}` ready at `{edev_dir}`")

    return 0

# Unit tests


def test_main():
    1


def test_args():
    assert main([]) == 1


# Main entry point
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
