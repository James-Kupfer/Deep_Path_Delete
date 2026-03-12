# Deep_Path_Delete

A focused Python utility for force-deleting stubborn directory trees on Windows.

`Deep_Path_Delete` is built for **path-length and depth edge cases** where Windows Explorer, `rmdir`, or other tools refuse to delete a folder because:

- The directory structure is extremely deep (many nested levels).
- File and folder names are so long that they exceed the traditional `MAX_PATH` limit.
- The combined path length makes the tree effectively "undeletable" by normal methods.

By applying the Windows `\\?\` long-path prefix and using a stack-based walk, this tool can successfully remove files and directories that standard deletion methods cannot touch.

> **WARNING: This tool permanently and irrecoverably deletes all files and folders under the target path. There is no undo, no Recycle Bin, and no recovery. Double-check `TARGET_PATH` before running.**

---

## Features

- Handles very long paths via the Windows `\\?\` prefix.
- Reliably deletes deeply nested directory trees that break Explorer.
- Often succeeds where `rmdir` / Explorer fail due to name length or depth.
- Explicit stack-based traversal (no recursion-limit issues).
- Two-phase delete: files first, then directories deepest-first.
- Prints a clear summary of deleted files, directories, and errors.

---

## Requirements

- Windows
- Python 3.7+ (standard library only)

---

## How to Use

### 1. Clone or download the repo

```bash
git clone https://github.com/<your-username>/Deep_Path_Delete.git
cd Deep_Path_Delete
```

### 2. Set the target path

Open `Deep_Path_Delete.py` and update `TARGET_PATH` near the top of the file:

```python
# Target directory to delete. Update this value before running the script.
TARGET_PATH = r"C:\FolderTreeToDelete"
```

Change this to the folder you want to delete. This is the **only line you need to edit**.

> **WARNING: Once run, all files and folders under `TARGET_PATH` will be permanently and irrecoverably deleted. Verify this path carefully before proceeding.**

### 3. Run the script

```cmd
python Deep_Path_Delete.py
```

You should see output similar to:

```text
Deleting: C:\FolderTreeToDelete

Done: 123 files, 45 dirs deleted, 0 errors.
```

- `files` -- number of files successfully deleted.
- `dirs` -- number of directories successfully deleted.
- `errors` -- operations that failed (e.g., locked files); printed as `ERR ...` lines.

---

## Using it from other scripts

```python
from Deep_Path_Delete import delete_tree

delete_tree(r"C:\some\very\deep\structure")
```

This gives you the same long-path and deep-tree handling inside other tools or scheduled jobs.
