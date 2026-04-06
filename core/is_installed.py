# ------------ EXTERNAL IMPORTS ------------
import importlib.util
import importlib.metadata
# ------------ INTERNAL IMPORTS ------------
from ..utils.compare_versions import compare_versions

# ------------ FUNCTION DEFINITION ------------
def is_installed(import_name, version=None, install_name=None):
    """
    Checks if a package is installed and optionally if it satisfies
    a version constraint.

    Parameters:
    - import_name: name used in Python import (e.g. "numpy", "bs4", "PIL")
    - version: optional version specifier (e.g. ">=1.2.3")
    - install_name: pip install name (e.g. "numpy", "Pillow", or git URL)

    Behavior:
    1. Verifies module existence using import_name
    2. If no version → return True
    3. Tries to obtain version using install_name (preferred)
    4. Falls back safely if version cannot be resolved (e.g. git installs)

    Returns:
    - True if installed (and matches version if provided)
    - False otherwise
    """

    # ------------------ EXISTENCE CHECK ------------------ #
    # This is the ONLY reliable check for importability
    if importlib.util.find_spec(import_name) is None:
        return False

    # If no version constraint → existence is enough
    if version is None:
        return True

    # ------------------ DETERMINE METADATA NAME ------------------ #
    # Prefer install_name for metadata (pip name)
    pkg_name = install_name if install_name else import_name

    # Git installs or invalid names cannot be resolved via metadata
    if pkg_name.startswith("git+"):
        # Cannot reliably check version → assume OK if import works
        return True

    # ------------------ VERSION CHECK ------------------ #
    try:
        installed_version = importlib.metadata.version(pkg_name)
    except importlib.metadata.PackageNotFoundError:
        # Metadata not found → cannot verify version reliably
        return False

    # Compare versions using your internal comparator
    return compare_versions(installed_version, version)