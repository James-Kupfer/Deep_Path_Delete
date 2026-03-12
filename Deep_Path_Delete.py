"""deep_path_deleter.py

Force-delete stubborn directory trees on Windows, including extremely
long or deeply nested paths that normal tools struggle with.
"""

import os

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Target main directory to delete. Update this value before running the script.
TARGET_PATH = r"C:\FolderTreeToDelete"

# ---------------------------------------------------------------------------

def _unc(path: str) -> str:
    """Return *path* with a Windows `\\?\` long-path prefix applied."""
    if path.startswith("\\\\?\\"):
        return path
    return "\\\\?\\" + os.path.abspath(path)


def delete_tree(root: str) -> None:
    """Recursively delete all files and directories under *root*."""
    root = _unc(root)
    deleted_files = deleted_dirs = errors = 0

    # Phase 1: walk with explicit stack using os.scandir + \?\ prefix
    all_dirs = []
    stack = [root]
    while stack:
        current = stack.pop()
        all_dirs.append(current)
        try:
            with os.scandir(current) as it:
                for entry in it:
                    try:
                        if entry.is_dir(follow_symlinks=False):
                            stack.append(entry.path)
                        else:
                            try:
                                os.remove(entry.path)
                                deleted_files += 1
                            except OSError as e:
                                print(f" ERR file: {e}")
                                errors += 1
                    except OSError as e:
                        print(f" ERR entry stat: {e}")
                        errors += 1
        except OSError as e:
            print(f" ERR scandir: {e}")
            errors += 1

    # Phase 2: remove dirs deepest-first
    for d in reversed(all_dirs):
        try:
            os.rmdir(d)
            deleted_dirs += 1
        except OSError as e:
            print(f" ERR rmdir: {e}")
            errors += 1

    print(
        f"\nDone: {deleted_files} files, {deleted_dirs} dirs deleted, {errors} errors."
    )


if __name__ == "__main__":
    print(f"Deleting: {TARGET_PATH}")
    delete_tree(TARGET_PATH)
