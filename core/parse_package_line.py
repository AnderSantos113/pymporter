# ------------ EXTERNAL IMPORTS ------------
import re
import warnings

# ------------ FUNCTION DEFINITION ------------
def parse_package_line(line):
    """
    Parses a requirements line using the format:

    Python import expression [operator version] : install_name

    Examples:
    - import numpy as np : numpy
    - from numpy import pi as p >=1.20 : numpy
    - numpy as np <= 3.0.0 : numpy
    - pyimporter as pimp == 1.0.0 : https://github.com/user/repo.git

    Returns:
    - import_type: "import", "from", or "simple"
    - module: base module namea
    - object: imported object (only for "from", else None)
    - alias: alias (or None)
    - version: version specifier (str or None)
    - install_name: pip install name (or same as module if None)

    If invalid → returns (None, None, None, None, None, None)
    """

    # ------------------ CLEAN LINE ------------------ #
    line = line.split("#")[0].strip()
    if not line:
        return None, None, None, None, None, None

    # ------------------ SPLIT INSTALL PART ------------------ #
    if ":" in line:
        left, install_name = map(str.strip, line.split(":", 1))
    else:
        left = line
        install_name = None

    # ------------------ EXTRACT VERSION ------------------ #
    # Version specifiers can be anywhere in the left part, so we search for them
    version_match = re.search(r'(==|>=|<=|>|<)\s*([^\s]+)', left)

    if version_match:
        version = f"{version_match.group(1)}{version_match.group(2)}"
        # Delete version part from left to avoid parsing issues
        left = left[:version_match.start()].strip()
    else:
        version = None

    # ------------------ PARSE: FROM IMPORT ------------------ #
    # Format: from module.sub import obj [as alias]
    match_from = re.match(
        r'^from\s+([a-zA-Z0-9_\.\-]+)\s+import\s+([a-zA-Z0-9_\.\-]+)(?:\s+as\s+(\w+))?$',
        left
    )

    if match_from:
        module, obj, alias = match_from.groups()
        return "from", module, obj, alias, version, install_name or module

    # ------------------ PARSE: IMPORT ------------------ #
    # Format : import module.sub [as alias]
    match_import = re.match(
        r'^import\s+([a-zA-Z0-9_\.\-]+)(?:\s+as\s+(\w+))?$',
        left
    )

    if match_import:
        module, alias = match_import.groups()
        return "import", module, None, alias, version, install_name or module

    # ------------------ PARSE: SIMPLE / NO-KEYWORD ------------------ #

    # Format: module [as alias] (ej: numpy)
    match_simple = re.match(
        r'^([a-zA-Z0-9_\.\-]+)(?:\s+as\s+(\w+))?$',
        left
    )

    if match_simple:
        module, alias = match_simple.groups()
        return "simple", module, None, alias, version, install_name or module

    # ------------------ INVALID ------------------ #
    warnings.warn(f"Invalid requirement line: '{line}'", UserWarning)
    return None, None, None, None, None, None