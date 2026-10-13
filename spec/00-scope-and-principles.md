# 00 — Scope and principles

**TPAC — Treatment Plant Asset Coding**
استاندارد کدگذاری دارایی‌های تصفیه‌خانه

Status: draft 0.3.0

## 1. Purpose

TPAC defines how to identify, place and classify the physical assets of water and
wastewater treatment plants, so that every maintainable thing in a plant has exactly one
correct code, and two people applying the standard to the same plant arrive at the same
codes.

## 2. Scope

TPAC covers:

- plant identification;
- units: the areas a plant is divided into;
- positions: the places where maintainable things are installed, and how they nest;
- physical assets and their installation in positions;
- equipment kinds and asset classification, with their catalogues;
- the code grammar;
- what does and does not receive a code;
- creation, replacement, relocation, retirement and correction;
- legacy codes and their conversion.

TPAC does not cover:

- maintenance strategy, maintenance tasks, failure coding, priority or criticality;
- process modelling: process units, streams, measurement points;
- inventory, spare parts and consumables;
- work management and any software's internal design;
- pipes, cables and assets outside the plant fence (networks, remote lift stations).

Other standards and systems may reference TPAC positions and assets. They do not change
TPAC codes.

## 3. Plant types

TPAC applies to wastewater and water treatment plants. The model, the grammar, the
placement rules and the lifecycle rules are the same for both. Catalogue entries state the
plant types they apply to. Entries for water treatment are marked `provisional` in this
version.

## 4. Normative language

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as
described in RFC 2119. Text marked *Example* or *Note* is informative.

## 5. Principles

**5.1 Position and asset are separate.** A position is a place in the plant. An asset is a
physical object. A pump position keeps its code when the pump installed in it is replaced.

**5.2 A code is an address, not a description.** A position code says where something is
and what role the position has. It never contains classification, make, rating, process
service, criticality, condition or status. Those are recorded as data.

**5.3 One meaning per segment.** Every part of a code has exactly one meaning, defined in
[02 — Code grammar](02-code-grammar.md).

**5.4 Codes are derived, not composed by hand.** A code results from choices made from
the catalogues: unit, parent, kind and index. Software SHOULD generate codes and SHOULD
NOT accept hand-typed codes without validation.

**5.5 Every question has one answer.** Placement rules are written as decision procedures
with explicit tie-breakers ([03 — Placement rules](03-placement-rules.md)). Where a rule
leaves a choice open, the standard says so and says who decides.

**5.6 Codes are stable.** A code, once issued, never changes meaning and is never reused,
even after the position is retired.

**5.7 The catalogue is data.** The unit, kind and classification catalogues are
maintained as machine-readable files ([`catalogue/`](../catalogue)). They are the single
source of truth for documentation and tools.

## 6. Relationship to other standards

- **ISO 14224** — TPAC kinds and classes follow the ISO 14224 idea of equipment classes
  with defined boundaries. TPAC's parent–child rule ([03](03-placement-rules.md), P5)
  plays the role of the ISO 14224 equipment boundary.
- **IEC 81346** — TPAC follows the reference designation principle of separating where a
  thing is, what role it has, and what product is installed.
- **Iranian national MIMS coding** — TPAC succeeds the national wastewater equipment
  coding instruction. Differences and conversion rules are in
  [06 — National mapping](06-national-mapping.md).

## 7. Parts

| Part | Content |
|---|---|
| [00](00-scope-and-principles.md) | Scope and principles |
| [01](01-model.md) | Model and definitions |
| [02](02-code-grammar.md) | Code grammar |
| [03](03-placement-rules.md) | Placement rules |
| [04](04-catalogues.md) | Catalogues |
| [05](05-lifecycle.md) | Lifecycle |
| [06](06-national-mapping.md) | National mapping |
| [07](07-conformance.md) | Conformance |
| [Glossary](glossary.md) | Terms in English and Persian |

## 8. Versioning

The standard and each catalogue carry a version `MAJOR.MINOR.PATCH`.

- **MAJOR** changes the meaning of an existing rule, token or class.
- **MINOR** adds rules, tokens, classes or types without changing existing meaning.
- **PATCH** corrects wording without changing meaning.

Versions below 1.0.0 are drafts; any part may change between drafts.
