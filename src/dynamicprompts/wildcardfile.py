from __future__ import annotations

from pathlib import Path

from dynamicprompts.utils import is_empty_line


class WildcardFile:
    def __init__(self, path: Path, encoding="utf8"):
        self._path = path
        self._encoding = encoding
        self._cache = None

    def get_wildcards(self) -> set[str]:
        if self._cache is not None:
            return self._cache

        with self._path.open(encoding=self._encoding, errors="ignore") as f:
            lines = [line.strip() for line in f if not is_empty_line(line)]
            self._cache = set(lines)
            return self._cache
