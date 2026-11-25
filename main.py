"""make.fun entry: Status Report Comedy Sprint.

Writes the one-line weekly status report from line.txt to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).
No network access. Deterministic: every run writes the same bytes.
After writing, the output is verified byte-for-byte against the
source line (SHA-256) so a partial or corrupted write fails loudly.
"""
import hashlib
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "line.txt"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT = Path(os.environ.get("MAKEFUN_OUTPUT", OUT_DIR / "entry.txt"))


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    # Only a trailing newline is normalised away; the line's own
    # characters (including any leading/trailing spaces) are kept intact.
    line = SRC.read_bytes().decode("utf-8").rstrip("\n")
    if not line:
        raise SystemExit("line.txt is empty")
    if len(line) > 200:
        raise SystemExit(f"status report line is {len(line)} characters, over the 200 limit")
    if "\n" in line:
        raise SystemExit("status report line must be a single line")
    data = line.encode("utf-8")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(data)
    if _sha256(OUT.read_bytes()) != _sha256(data):
        raise SystemExit("entry.txt write mismatch: output bytes differ from source")


if __name__ == "__main__":
    main()
