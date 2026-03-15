"""Deterministic SHA-256 hashing of skill folder contents."""

from __future__ import annotations

import hashlib
from pathlib import Path


def hash_directory(path: Path) -> str:
    """Compute a deterministic SHA-256 hash of a directory's contents.

    Files are sorted by relative path to ensure determinism across platforms.
    Both file paths and contents are hashed.
    """
    hasher = hashlib.sha256()

    all_files = sorted(f for f in path.rglob("*") if f.is_file() and not f.name.startswith("."))

    for file_path in all_files:
        rel = file_path.relative_to(path)
        hasher.update(str(rel).encode())
        hasher.update(file_path.read_bytes())

    return hasher.hexdigest()
