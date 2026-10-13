# TPAC — Treatment Plant Asset Coding

استاندارد کدگذاری دارایی‌های تصفیه‌خانه

TPAC is an open standard for identifying, placing and classifying the physical assets of
water and wastewater treatment plants. It gives every maintainable thing in a plant exactly
one correct code, the same way in every plant, and it is precise enough to be checked by
software.

**Status:** draft 0.3.0 ([changelog](CHANGELOG.md)). Wastewater catalogue entries are `active`; water treatment entries
are `provisional`.

## In one picture

```text
KJBJBS01BW05MO01
│    │    │    └── motor 1 of …
│    │    └─────── blower 5 in …
│    └──────────── blower station 1 of …
└───────────────── plant KJBJ
```

- A **position** is a place in the plant; its code is an address and never describes what
  is installed there.
- An **asset** is the physical object installed in a position; replacing the blower does
  not change `KJBJBS01BW05`.
- Every segment is two letters and two digits; the tree is as deep as the plant needs.
- Kinds, units and classification come from machine-readable catalogues.

## Contents

| Path | Content |
|---|---|
| [`spec/`](spec) | The standard, parts 00 to 07, and the glossary |
| [`catalogue/units.yaml`](catalogue/units.yaml) | Unit catalogue |
| [`catalogue/kinds.yaml`](catalogue/kinds.yaml) | Position kind catalogue |
| [`catalogue/classification.yaml`](catalogue/classification.yaml) | Asset classification |
| [`catalogue/mappings/iran-mims.yaml`](catalogue/mappings/iran-mims.yaml) | Mapping from the Iranian national coding |
| [`tools/tpac.py`](tools/tpac.py) | Reference validator |
| [`tests/vectors/`](tests/vectors) | Conformance vectors for codes, asset numbers and registers |
| [`examples/`](examples) | Example position register |

Start with [00 — Scope and principles](spec/00-scope-and-principles.md), then
[03 — Placement rules](spec/03-placement-rules.md).

## Validator

Requires Python 3.9 or later and PyYAML (`pip install pyyaml`).

```sh
python3 tools/tpac.py check                               # check the catalogues
python3 tools/tpac.py parse KJBJBS01BW05MO01 KJBJA000123   # explain and validate codes and asset numbers
python3 tools/tpac.py register examples/example-plant.csv --plant-type wastewater
python3 tests/test_vectors.py                             # run the conformance vectors
```

## Licence

Specification and catalogues: CC BY 4.0. Tools: MIT.
