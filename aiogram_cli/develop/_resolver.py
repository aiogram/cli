import importlib
import logging
from typing import Any

logger = logging.getLogger(__name__)


class LoadError(Exception):
    pass


def resolve_import(*, target: str, possible_names: set[str] | None = None) -> Any:
    module_name, _, target_name = target.partition(":")
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        msg = f"Can't import module: {module_name!r} ({type(e).__name__}: {e})"
        raise LoadError(msg) from e
    if not target_name:
        for name in possible_names:
            if hasattr(module, name):
                target_name = name
                break
        else:
            msg = f"Can't find target name in module: {module_name!r} (checked names: {possible_names})"
            raise LoadError(msg)

    try:
        return getattr(module, target_name, None)
    except AttributeError as e:
        msg = f"Can't find target name in module: {module_name!r} by name: {target_name!r}"
        raise LoadError(msg) from e
