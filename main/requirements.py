# ------------ EXTERNAL IMPORTS ------------
import warnings
# ------------ INTERNAL IMPORTS ------------
from .. core import parse_package_line, install_package, import_package

# ------------ FUNCTION DEFINITION ------------
def requirements(file_path, force_reinstall=False, upgrade=False,
				 show_output=True):
	"""
	Reads a requirements file, installs and imports all dependencies.

	Expected line format:
		Python import expression [operator version] : install_name

	Flow:
	1. Parse each line
	2. Install dependency (using install_name)
	3. Import dependency (using import_type logic)

	Notes:
	- Supports pip/install name ≠ import name
	- Supports GitHub / URL installs
	- Supports "import" and "from import"

	Raises:
	- FileNotFoundError if file does not exist
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

				# ------------------ IMPORT ------------------ #
				import_package(
					import_type=import_type,
					module=module,
					obj=obj,
					alias=alias
				)

	except FileNotFoundError:
		warnings.warn(f"File not found: '{file_path}'", UserWarning)
	except Exception as e:
		warnings.warn(f"Error processing file: {e}", UserWarning)