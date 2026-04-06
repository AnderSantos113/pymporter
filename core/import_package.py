# ------------ EXTERNAL IMPORTS ------------
import importlib
import warnings

# ------------ FUNCTION DEFINITION ------------
def import_package(import_type, module, obj=None, alias=None):
    """
    Dynamically imports a module or object based on parsed requirements.

    Parameters:
    - import_type: "import", "from", or "simple"
    - module: base module name (e.g. "numpy")
    - obj: object to import (only for "from", e.g. "pi")
    - alias: alias to assign in globals (optional)

    Returns:
    - tuple: (imported_object, target_name)
    """

    try:
        # ------------------ IMPORT LOGIC ------------------ #
        if import_type == "import":
            result = importlib.import_module(module)

        elif import_type == "from":
            parent = importlib.import_module(module)
            try:
                result = getattr(parent, obj)
            except AttributeError:
                raise ImportError(
                    f"Module '{module}' has no attribute '{obj}'"
                )

        elif import_type == "simple":
            result = importlib.import_module(module)

        else:
            raise ValueError(f"Invalid import_type: '{import_type}'")

    except ImportError as e:
        raise ImportError(f"Failed to import ({import_type}): {module}") from e

    # ------------------ NAME RESOLUTION ------------------ #
    # Determine the name to be used for the variable in the caller scope
    target_name = alias or obj or module
    
    return result, target_name