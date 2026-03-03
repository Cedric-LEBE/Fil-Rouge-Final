from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SRC_MODEL = ROOT / "model_store" / "latest"
SRC_DATA_INTERIM = ROOT / "data" / "interim"

DST = ROOT / "app" / "bundle"
DST_MODEL = DST / "model_store" / "latest"
DST_DATA = DST / "data" / "interim"


def copytree(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)

    if not SRC_MODEL.exists():
        raise FileNotFoundError(f"Missing: {SRC_MODEL}")
    if not SRC_DATA_INTERIM.exists():
        raise FileNotFoundError(f"Missing: {SRC_DATA_INTERIM}")

    copytree(SRC_MODEL, DST_MODEL)
    copytree(SRC_DATA_INTERIM, DST_DATA)

    print(f"✅ Bundle exporté dans: {DST}")


if __name__ == "__main__":
    main()