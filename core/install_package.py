# ------------ EXTERNAL IMPORTS ------------
import subprocess
import sys
import warnings

# ------------ INTERNAL IMPORTS ------------
from ..utils.dprint import dprint, DebugWarning
from .is_installed import is_installed

# ------------ FUNCTION DEFINITION ------------
def install_package(install_name, import_name=None,
					force_reinstall=False, upgrade=False,
					version=None, show_output=True):
	"""
	Installs a package using pip with version control and output management.

	Parameters:
	- install_name: pip install target (e.g. "numpy", "git+https://...")
	- import_name: module name used to verify installation (e.g. "numpy", "bs4")
	- force_reinstall: if True, reinstalls even if already present
	- upgrade: if True, upgrades the package
	- version: version condition (e.g. ">=1.2.3") [ignored for URLs]
	- show_output: controls both dprint messages and pip output

	Key design:
	- install_name != import_name (important for pip vs import mismatch)
	- supports GitHub / URLs
	"""

	# ------------------ BUILD COMMAND ------------------ #
	cmd = [sys.executable, "-m", "pip", "install"]

	# Detect if install_name is URL / VCS → version should NOT be appended
	is_url = install_name.startswith(("git+", "http://", "https://"))

	if is_url:
		package_spec = install_name
	else:
		package_spec = f"{install_name}{version}" if version else install_name

	if not show_output:
		cmd += ["-q"]

	# ------------------ WARNING CONTROL ------------------ #
	with warnings.catch_warnings():
		if not show_output:
			warnings.simplefilter("ignore", DebugWarning)

		# ------------------ FORCE REINSTALL ------------------ #
		if force_reinstall:
			dprint(f"Reinstalling '{package_spec}'...")
			try:
				subprocess.check_call(cmd + ["--force-reinstall", package_spec])
				dprint(f"'{package_spec}' reinstalled successfully.")
			except subprocess.CalledProcessError as e:
				warnings.warn(f"Error reinstalling '{package_spec}': {e}", UserWarning)
			return

		# ------------------ INSTALL CHECK ------------------ #
		# Use import_name if provided (correct behavior)
		check_name = import_name if import_name else install_name

		# Skip version check for URLs (not meaningful)
		if not is_url:
			installed = is_installed(check_name, version)
		else:
			installed = is_installed(check_name)

		# ------------------ SKIP ------------------ #
		if installed and not upgrade:
			dprint(f"'{package_spec}' is already installed.")
			return

		# ------------------ UPGRADE ------------------ #
		if installed and upgrade:
			dprint(f"Upgrading '{package_spec}'...")
			try:
				subprocess.check_call(cmd + ["--upgrade", package_spec])
				dprint(f"'{package_spec}' upgraded successfully.")
			except subprocess.CalledProcessError as e:
				warnings.warn(f"Error upgrading '{package_spec}': {e}", UserWarning)
			return

		# ------------------ INSTALL ------------------ #
		dprint(f"Installing '{package_spec}'...")
		try:
			subprocess.check_call(cmd + [package_spec])
			dprint(f"'{package_spec}' installed successfully.")
		except subprocess.CalledProcessError as e:
			warnings.warn(f"Error installing '{package_spec}': {e}", UserWarning)