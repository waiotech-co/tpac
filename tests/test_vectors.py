"""Run the conformance vectors in tests/vectors against the reference validator.

    python3 -m unittest discover -s tests
"""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VECTORS = Path(__file__).resolve().parent / "vectors"

_spec = importlib.util.spec_from_file_location("tpac", ROOT / "tools" / "tpac.py")
tpac = importlib.util.module_from_spec(_spec)
sys.modules["tpac"] = tpac
_spec.loader.exec_module(tpac)

CATALOGUE = tpac.load_catalogue()


def _load(name: str) -> list[dict]:
    return json.loads((VECTORS / name).read_text(encoding="utf-8"))


class CatalogueTest(unittest.TestCase):
    def test_catalogues_conform(self) -> None:
        self.assertEqual(tpac.check_catalogue(CATALOGUE), [])


class CodeVectorTest(unittest.TestCase):
    def test_position_codes(self) -> None:
        for vector in _load("codes.json"):
            with self.subTest(vector["input"]):
                parsed = tpac.parse_code(vector["input"], CATALOGUE)
                self.assertEqual(parsed.code, vector["normalized"])
                self.assertEqual({rule for rule, _ in parsed.errors}, set(vector["rules"]))

    def test_asset_numbers(self) -> None:
        for vector in _load("asset-numbers.json"):
            with self.subTest(vector["input"]):
                parsed = tpac.parse_asset_number(vector["input"])
                self.assertEqual(parsed.code, vector["normalized"])
                self.assertEqual({rule for rule, _ in parsed.errors}, set(vector["rules"]))


class RegisterVectorTest(unittest.TestCase):
    def test_registers(self) -> None:
        for vector in _load("registers.json"):
            with self.subTest(vector["file"]):
                findings, _ = tpac.check_register(
                    (VECTORS / vector["file"]).resolve(), CATALOGUE, vector["plant_type"]
                )
                self.assertEqual({rule for rule, _, _ in findings}, set(vector["rules"]))


if __name__ == "__main__":
    unittest.main()
