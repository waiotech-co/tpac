# 07 — Conformance

## 1. Conformance targets

| Target | Conforms when |
|---|---|
| A code | it satisfies the G- and S-rules (a position code) or the A-rule (an asset number) |
| A position register | every code conforms and it satisfies the R-rules |
| A catalogue | it satisfies the C-rules |
| Software | it satisfies the I-rules |

The reference validator [`tools/tpac.py`](../tools/tpac.py) checks the C-, G-, S-, A- and
R-rules.

## 2. Code rules

| Rule | Requirement | Source |
|---|---|---|
| G-01 | Only A–Z and 0–9 after normalization | 02 §2, §5 |
| G-02 | Length is 8 + 4n | 02 §2 |
| G-03 | Plant code matches the grammar | 02 §3 |
| G-04 | Unit segment is two letters and two digits; unit token is in the unit catalogue | 02 §2 |
| G-05 | Unit instance is 01–99 | 02 §4 |
| G-06 | Every position segment is two letters and two digits; kind token is in the kind catalogue | 02 §2 |
| G-07 | Every index is 01–99 | 02 §4 |
| S-01 | First position kind may be placed under a unit | 02 §2, 01 M-9 |
| S-02 | Every further kind is an allowed child of the previous kind | 02 §2, 01 M-9 |
| A-01 | An asset number is a plant code, `A`, and six digits | 02 §7 |

## 3. Register rules

A position register is a list of positions of one plant. The CSV form has the columns
`code`, `name`, `quantity`, `structure_class`, `asset_class`, `legacy_codes` (separated by
`;`) and `status`. Unit rows (8-character codes) are included.

| Rule | Requirement | Source |
|---|---|---|
| R-01 | Every code appears once | 02 §4.3 |
| R-02 | Every position's parent is in the register | 01 M-7 |
| R-03 | Quantity above 1 only on population kinds | 03 P8 |
| R-04 | Asset class is allowed by the position's kind | 01 M-15 |
| R-05 | Structure class is allowed by the position's kind | 01 M-10 |
| R-06 | A legacy code identifies at most one position | 05 L-9 |
| R-07 | One plant code per register | 01 M-1 |
| R-08 | Units are defined for the plant's type | 00 §3 |
| R-09 | Every position has a name | 03 P10 |
| R-10 | Status is `active` or `retired` | 01 M-7 |

## 4. Catalogue rules

| Rule | Requirement |
|---|---|
| C-01 | Tokens are two uppercase ASCII letters |
| C-02 | Tokens are unique across units and kinds |
| C-03 | Families exist |
| C-04 | Unit plant types are `wastewater` and/or `water` |
| C-05 | Status is `active`, `provisional` or `deprecated` |
| C-06 | Every entry has English and Persian names |
| C-07 | Units have `covers`; kinds have `definition` |
| C-08 | Placement is `unit` and/or `parent` |
| C-09 | Asset classes exist and are not civil or mobile |
| C-10 | Structure classes are civil classes |
| C-11 | Every kind allows at least one asset or structure class |
| C-12 | Child kinds exist |
| C-13 | A child kind allows placement under a parent |
| C-14 | Retired in 0.2.0: a kind may list itself as a child (an auxiliary pump of a pump) |
| C-15 | Every kind placeable under a parent is some kind's child |
| C-16 | Building children equal the building services list |
| C-17 | Class ids and type ids within a class are unique |
| C-18 | A national type code maps to one TPAC type |
| C-19 | Every mapping target exists in the catalogues |
| C-20 | Group, class and type ids match `[a-z][a-z0-9-]*` |
| C-21 | Groups, classes within a group, and types within a class have distinct names in each language |

## 5. Implementation rules

Software that stores TPAC data conforms when it:

| Rule | Requirement |
|---|---|
| I-01 | keeps an immutable identity for every position and asset, separate from its code |
| I-02 | generates codes from unit, parent, kind and number, and validates any code it accepts |
| I-03 | never issues a retired code or number again |
| I-04 | never changes a code automatically |
| I-05 | keeps installation history with start and end dates |
| I-06 | keeps code, name, classification and status history with date and actor |
| I-07 | stores legacy codes and finds positions by them |
| I-08 | exports a position register in the CSV form of §3 |
| I-09 | records the TPAC version (`MAJOR.MINOR.PATCH`) each code was issued under |

## 6. Conformance vectors

[`tests/vectors/`](../tests/vectors) holds machine-readable cases for the code rules (G-, S-,
A-) and the register rules (R-). Each case states its input and the rules it violates, or that
it is valid. The reference validator passes every vector; software that claims conformance
SHOULD pass them too, so that independent implementations agree with the validator.
