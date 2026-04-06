# ------------ EXTERNAL IMPORTS ------------
import warnings

# ------------ FUNCTION DEFINITION ------------
class DebugWarning(UserWarning):
    # Waring class for debug messages, can be filtered or ignored as needed
    pass

def dprint(*args):
    """
    Debug print function that uses warnings.warn to display messages in the
    console.

    This allows the messages to be filtered or ignored as needed, and provides
    a consistent way to output debug information without cluttering the standard
    output.
    """
    # Join the arguments into a single string message
    msg = " ".join(map(str, args))
    # Show warning
    warnings.warn(msg, DebugWarning, stacklevel=2)
