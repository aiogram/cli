from importlib.metadata import entry_points


def iter_entry_points(group: str):
    return entry_points(group=group).select()
