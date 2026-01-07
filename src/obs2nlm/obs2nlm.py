"""A tool to turn an Obsidian vault into a source useful for NotebookLM."""

##############################################################################
# Python imports.
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Final

##############################################################################
# Local imports.
from . import __version__

##############################################################################
DEFAULT_VAULT_ROOT: Final[Path] = Path(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents"
).expanduser()
"""The default root to search for vaults.

Note:
    I'm on macOS, so this is specific to macOS.
"""

##############################################################################
PREAMBLE: Final[str] = """\
# AI NAVIGATION & BEHAVIOR RULES

1. This file is a 'mega-source' containing an entire Obsidian vault.
2. Every individual note starts with 'BEGIN SOURCE: [path]' and ends with 'END SOURCE: [path]'.
3. Always cite the specific 'BEGIN SOURCE' filename when providing information.
4. YAML frontmatter (between --- near the start of a source) contains valid metadata; prioritise it for dating and tagging.
5. At the end of the file is a table of contents, marked with BEGIN TABLE OF CONTENT and END TABLE OF CONTENT.
6. Use the table of contents to search for specific files and to cite the source for any answer created.
7. If a user asks for a 'summary of the vault', refer to the table of contents.
8. Files in the format YYYY-MM-DD.md are going to be daily note files; parse the name as a date and refer to it where possible.
"""

##############################################################################
WORD_LIMIT: Final[int] = 500_000
"""The word limit for a source in NotebookLM."""


##############################################################################
def resolve_vault(vault: Path) -> Path:
    """Work out the full path to the vault.

    Args:
        vault: The name of the vault to look for.

    Returns:
        The full path to the vault, or `None` if there isn't one.
    """
    if vault.is_dir():
        return vault
    if (default_vault := DEFAULT_VAULT_ROOT / vault).is_dir():
        return default_vault
    print(f"Can't find an Obsidian vault named '{vault}'")
    exit(1)


##############################################################################
def resolve_source(args: Namespace) -> Path:
    """Work out the name to use for the source file to create.

    Args:
        args: The command line arguments.

    Returns:
        The full path for the source file, or `None` if we couldn't
        work out a name.
    """
    return args.source or Path(args.vault.stem).with_suffix(".md")


##############################################################################
def additional_instructions(instructions: str | None) -> str | None:
    """Loads up any additional instructions to place in the output.

    Args:
        instructions: The instructions to look at and use.

    Returns:
        The instructions if there are any, or `None`.

    Notes:
        If there is a file in the filesystem that matches the content of
        `instructions` then the content of that file will be used, otherwise
        the text will be used.
    """
    if instructions is not None:
        if Path(instructions).is_file():
            instructions = Path(instructions).read_text(encoding="uft-8")
    return instructions


##############################################################################
def make_source(args: Namespace) -> None:
    """Make a source file for NotebookLM.

    Args:
        args: The command line arguments.
    """

    vault = resolve_vault(args.vault)
    source = resolve_source(args)

    print(f"Converting {vault} to {source}")
    table_of_content: list[Path] = []
    extra_preamble = additional_instructions(args.additional_instructions)
    estimated_word_count = len((PREAMBLE + (extra_preamble or "")).split())
    with source.open("w", encoding="utf-8") as notebook_source:
        notebook_source.write(PREAMBLE)
        if extra_preamble:
            notebook_source.write(f"\n\n## ADDITIONAL RULES\n\n{extra_preamble}")
        notebook_source.write("\n\n---\n\n")
        for vault_file in vault.rglob("*.md"):
            table_of_content.append(vault_file.relative_to(vault))
            notebook_source.write(f"BEGIN SOURCE: {vault_file.relative_to(vault)}\n\n")
            notebook_source.write(content := vault_file.read_text(encoding="utf-8"))
            estimated_word_count += len(content.split())
            notebook_source.write(
                f"\n\nEND SOURCE: {vault_file.relative_to(vault)}\n\n"
            )
        notebook_source.write("\n\nBEGIN TABLE OF CONTENT\n\n")
        for entry in sorted(table_of_content):
            notebook_source.write(f"* {entry}\n")
        notebook_source.write("\n\nEND TABLE OF CONTENT\n\n")
    # Add some extra word count for the TOC itself, and also include a rough
    # estimate for the begin/end markers for the content.
    estimated_word_count += len(table_of_content) * 7
    print(f"Estimated word count: {estimated_word_count:,}")
    if estimated_word_count > WORD_LIMIT:
        print("NotebookLM will truncate this source!")
    else:
        print(f"{(estimated_word_count / WORD_LIMIT) * 100:.1f}% of the limit")


##############################################################################
def get_args() -> Namespace:
    """Get the command line arguments."""

    # Version information.
    version = f"v{__version__}"

    # Create the argument parser object.
    parser = ArgumentParser(
        prog=Path(__file__).stem,
        description="Turn an Obsidian vault into a NotebookLM source",
        epilog=version,
    )

    # Add additional instructions.
    parser.add_argument(
        "-a",
        "--additional-instructions",
        help="Additional instructions to pass on to NotebookLM at the top of the source",
    )

    # Add the vault.
    parser.add_argument(
        "--vault",
        type=Path,
        help="The name of or the path to the source vault",
        required=True,
    )

    # Add the name of the source file that will be created.
    parser.add_argument(
        "--source",
        type=Path,
        help="The path to the file to create as the source for NotebookLM",
        required=False,
    )

    # Add --version
    parser.add_argument(
        "-v",
        "--version",
        help="Show version information",
        action="version",
        version=f"%(prog)s {version}",
    )

    # Parse the command line.
    return parser.parse_args()


##############################################################################
def main() -> None:
    """Main entry point."""
    make_source(get_args())


### obs2nlm.py ends here
