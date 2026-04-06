# ------------ EXTERNAL IMPORTS ------------
import warnings
# ------------ INTERNAL IMPORTS ------------
from .. core import parse_package_line, install_package, is_installed

def installer(file_path, force_reinstall=False, upgrade=False, 
              show_output=True):
    
    """
    Installs packages from a requirements file without importing them.

    Designed for scenarios where you ONLY want to install packages.
    Useful in setup scripts or CI/CD pipelines.

    Parameters:
    - file_path: path to the requirements file
    - force_reinstall: if True, reinstalls all packages
    - upgrade: if True, upgrades packages even if already installed
    - show_output: controls both prints (dprint) and pip output

    Flow:
    - Reads line by line
    - Installs/updates according to options
    - Does NOT import packages
    - Ignores aliases in requirements.txt

    Notes:
    - More aggressive than importer() (can upgrade)
    - Useful for CI/CD or pre-setup before using importer()
    Raises:

    - FileNotFoundError: if the file does not exist

    """

    try:
		with open(file_path, "r") as f:
			for line in f:
				(
					import_type,
					module,
					obj,
					alias,
					version,
					install_name
				) = parse_package_line(line)

				if not import_type:
					continue  # invalid or empty line

				# ------------------ INSTALL ------------------ #
				install_package(
					install_name=install_name,
					import_name=module,
					force_reinstall=force_reinstall,
					upgrade=upgrade,
					version=version,
					show_output=show_output
				)

	except FileNotFoundError:
		warnings.warn(f"File not found: '{file_path}'", UserWarning)
	except Exception as e:
		warnings.warn(f"Error processing file: {e}", UserWarning)