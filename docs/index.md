## Introduction

[`obs2nlm`](https://github.com/davep/obs2nlm) is a simple command line tool
designed to turn an [Obsidian](https://obsidian.md) vault into a single
[Markdown](https://en.wikipedia.org/wiki/Markdown) file that can be uploaded
to Google's [NotebookLM](https://notebooklm.google.com/) (or presumably used
with other LLM tools for similar purposes).

It's probably fair to say that it's "opinionated" in that I wrote this to
serve my specific purpose; but where possible I've attempted to make it
generic and configurable.

## Installing

`obs2nlm` is a Python application and [is distributed via
PyPI](https://pypi.org/project/obs2nlm/). It can be installed with tools such
as [pipx](https://pipx.pypa.io/stable/):

```sh
pipx install obs2nlm
```

or [`uv`](https://docs.astral.sh/uv/):

```sh
uv tool install obs2nlm
```

Also, if you do have uv installed, you can simply use
[`uvx`](https://docs.astral.sh/uv/guides/tools/):

```sh
uvx obs2nlm
```

to run `obs2nlm`.

## Command line options

The command is called `obs2nlm` and all command line options can be found
with:

```sh
obs2nlm --help
```

giving output like this:

```bash exec="on" result="text"
obs2nlm --help
```

The key options are:

### `--vault`

This tells `obs2nlm` which Obsidian vault you want to convert. This can
either be a path to the root directory of a vault, or simply the name of a
vault.

!!! note

    Currently, if you pass just the name of a vault, it will look for that
    vault in `~/Library/Mobile Documents/iCloud~md~obsidian/Documents` --
    this is where my vaults live because I use Obsidian on macOS and sync
    with iCloud. If I figure out what other possible default locations are
    for other platforms and sync methods, I will extend this.

### `---source`

This tells `obs2nlm` the name of the source file to create (the name of the
file that you will use as a source for NotebookLM). If `--source` isn't
supplied then the name of the vault plus an `.md` extension is assumed.

!!! important

    `obs2nlm` will always overwrite the source; think carefully before
    siumply using the default name.

### `-a`, `--additional-instructions`

This switch lets you provide some optional additional instructions to
include at the top of the generated file. By default `obs2nlm` adds some
instructions for the LLM to help and encourage it to "comprehend" the
content of the file; using this switch you can add instructions specific to
the vault you're generating the file for.

!!! note

    This switch serves two purposes: if the value passed to the switch
    matches the name of a file in your filesystem, the content of that file
    will be read and used; otherwise the value given to the switch will be used.

## Examples

Create a NotebookLM source from a vault named "Observations":

```sh
obs2nlm --vault Observations
```

This will read Observations vault from the default vault location, and will
create `Observations.md` in the current working directory.

On the other hand, if you wanted to create the notebook source in a
different location and with a different name:

```sh
obs2nlm --vault Observations --source ~/sources/obs.md
```

To add a simple additional instruction when creating the output:

```sh
obs2nlm --vault Observations --additional-instructions "Always be sarcastric when you reply to me"
```

or to do the same but pull the additional instruction from a file:

```sh
obs2nlm --vault Observations --additional-instructions ~/.llm/rules.md
```

## Getting help

If you need some help using `obs2nlm`, or have ideas for improvements, please
feel free to drop by [the
discussions](https://github.com/davep/obs2nlm/discussions) and ask or
suggest. If you believe you've found a bug please feel free to [raise an
issue](https://github.com/davep/obs2nlm/issues).

[//]: # (index.md ends here)
