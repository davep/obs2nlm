"""obs2nlm - Obsidian vault to NotebookLM conversation tool."""

##############################################################################
# Python imports.
from importlib.metadata import version

######################################################################
# Main library information.
__author__ = "Dave Pearson"
__copyright__ = "Copyright 2026, Dave Pearson"
__credits__ = ["Dave Pearson"]
__maintainer__ = "Dave Pearson"
__email__ = "davep@davep.org"
__version__ = version("obs2nlm")
__licence__ = "GPLv3+"


##############################################################################
# Local imports.
from .obs2nlm import main

##############################################################################
# Exports.
__all__ = ["main"]

### __init__.py ends here
