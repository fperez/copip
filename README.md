# copip: conda-pip environment development overlays

A tool to better manage PyPI and source packages (installed using `pip`, with or without `-e .`) in a conda-based workflow.

The approach taken is to create a separate filesystem area where *all* non-conda installations go.  Then, we "hijack" the `--user` flag of Python's installation process by *always* using `--user` during any pip-based installation.  When using the conda root environment such area already exists: `~/.local/...` (on *nix, there's a Windows-specific location too).  When using custom conda environments, we set the `$PYTHONUSERBASE` variable to point to a location named the same as the conda environment but separate in the filesystem, and set `$PATH` accordingly.

This avoids the problem of conflicts arising after packages have been added to a conda environment and a conda update potentially overwrites them.

It has been tested lightly in my own workflow, but I'm sure there's still a ton of edge cases it misses.


## Setup

There's no packaging/installation yet.  You 


## Usage

Assuming your paths are properly set up as above, you can use this to manage an overlay on your conda env `foo` by running

```bash
mkedev foo
```

Since this tool is designed to direct all pip installs to the user overlay, it sets the environment variable `PIP_USER=True` unconditionally on environment activation.

If you want to have the same behavior in your root conda env, you should:

- Also set `PIP_USER=True` in your regular shell config file ( `~/.bashrc` or equivalent).

- Ensure that `~/.local/bin` is in your `PATH`, so that script entry points installed by new packages are also found first.


## Todo

Besides packaging/configurability, the key thing to test next is usage with complex C extensions built this way.  That requires setting lots more environment variables related to compilers, linkers, etc.  I have old code for that which can be reused if there's interest.


## Requirements

The 'driver' script is Python 3.6-only.  This would be easy to avoid, but I wanted to use it as an opportunity to play with some Python 3.6-specific features, like f-strings and standard library support for pathlib.  The resulting code is indeed nicer, so I'm keeping it that way.


## License

Released under the terms of the 3-clause ("new") BSD license.
