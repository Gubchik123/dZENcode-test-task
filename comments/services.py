def _are_ordering_parameters_valid(order_by: str, order_dir: str) -> bool:
    """Checks if the given order_by and order_dir are valid."""
    if (order_dir not in ("asc", "desc")) or (order_by not in ("u", "e", "c")):
        return False
    return True


def _get_order_symbol_by_(order_dir: str) -> str:
    """Returns the Django order symbol (dash or empty string)."""
    return "-" if order_dir == "desc" else ""


def _get_correct_(order_by: str) -> str:
    """Returns the correct field name by the given (one-letter) order_by."""
    fields = {"u": "author__username", "e": "author__email", "c": "created"}
    return fields[order_by]


def get_ordering_string(order_by: str, order_dir: str) -> str | None:
    """
    Returns ordering string or None after checking the given GET parameters.
    """
    if _are_ordering_parameters_valid(order_by, order_dir):
        return _get_order_symbol_by_(order_dir) + _get_correct_(order_by)
    return None
