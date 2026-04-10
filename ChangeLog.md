# obs2nlm ChangeLog

## Unreleased

**Released: WiP**

- Added a `--dry-run` command line option.
  ([#12](https://github.com/davep/obs2nlm/pull/12))
- Added a `--split` command line option, to split the output source file if
  it gets close to the NotebookLM word limit.

## v1.1.2

**Released: 2026-01-11**

- Release to update the package metadata on PyPI.

## v1.1.1

**Released: 2026-01-09**

- Fixed a crash due when using additional instructions.
  ([#6](https://github.com/davep/obs2nlm/pull/6))

## v1.1.0

**Released: 2026-01-09**

- Tweaked the builtin preamble that is included in the output file.
  ([#4](https://github.com/davep/obs2nlm/pull/4))
- Added an `--instructions` switch so the builtin instructions can be
  overridden. ([#4](https://github.com/davep/obs2nlm/pull/4))

## v1.0.0

**Released: 2026-01-08**

- Added support for warning when we're near the NotebookLM word limit.
- Added `--additional-instructions` as a command line parameter.
  ([#1](https://github.com/davep/obs2nlm/pull/1))

## v0.0.1

**Released: 2026-01-07**

- Initial release.

[//]: # (ChangeLog.md ends here)
