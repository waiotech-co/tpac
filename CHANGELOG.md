# Changelog

## 0.3.0

Changes from adopting the standard in software (Waiotech).

### Conformance

- New part 07 §6 and `tests/vectors/`: machine-readable cases for the code, asset-number and
  register rules, run by `tests/test_vectors.py` against the reference validator.
- Rule A-01 for asset numbers; the validator parses them (`tpac.py parse`).
- Rule C-20: classification ids match `[a-z][a-z0-9-]*` (part 04 §5.0).
- Rule C-21 and a stricter C-06: names are exactly an English and a Persian text, and siblings
  have distinct names. Eight English names that an unquoted comma had truncated are fixed
  (for example `Circular, centre drive`).
- Register rules renumbered without a gap: R-03 to R-10 (was R-04 to R-11).
- G-04 and G-06 state the segment shape (two letters and two digits) they always checked.
- I-09 records the TPAC version, not a catalogue version.

### Code grammar

- Unit instance numbers are never reused within a plant (§4.3).

### Model

- M-12: asset status is defined by installation, repair and disposal, and software may derive
  it. The asset-number reference points to 02 §7.

### Lifecycle

- L-8: correcting a position recodes its descendants in the same action, because their codes
  contain the parent's code. L-6: children are retired or corrected under another parent.

## 0.2.0

Changes from the first conversion of a real plant against the standard.

### Code grammar

- Codes have one written form, without separators. The hyphenated display form is removed.

### Catalogue

- Kind `HS` (Hardstanding) for paved pads, plant roads and platforms, with civil class `pad`.
- Kind `WM` (Workshop machine) with class `workshop-machine`.
- `PU` may have `PU` and `GA` children; `BW` and `CO` may have `PU` children.
- `SW` is one switchboard line-up; cubicles and feeders are parts.
- Types `conveyor.screw-feeder`, `lab-instrument.shaker`, `lab-instrument.heating-mantle`,
  `lab-instrument.air-pump`.
- Laboratory meter types are named by what they measure; bench or portable is an attribute.
- Rule C-14 retired: a kind may list itself as a child.

### Placement rules

- P1.2: computer peripherals and video displays are not positions.
- P4.6: a building belongs to one unit; everything in it belongs to that unit.
- P5.3: does not apply to a valve or gate isolating one machine.
- P5.7: instrument displays are parts of the instrument.
- P5.8: auxiliary machines are children of the machine they serve.

### Conversion

- Count disagreements, population defaults, inferred buildings and other plant sources
  are covered in part 06.

## 0.1.0

First draft.
