from ._version import __version__


def get_version() -> str:
    """Get the package version."""
    return __version__


__all__ = ["get_version"]
