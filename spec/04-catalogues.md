# 04 — Catalogues

## 1. Files

The catalogues are YAML files in [`catalogue/`](../catalogue). They are normative: the
tokens, definitions and relationships in them are part of the standard.

| File | Content |
|---|---|
| [`units.yaml`](../catalogue/units.yaml) | unit types, their families, plant types and scope |
| [`kinds.yaml`](../catalogue/kinds.yaml) | position kinds, their placement, children and allowed classes |
| [`classification.yaml`](../catalogue/classification.yaml) | asset classification: groups, classes, types |
| [`mappings/iran-mims.yaml`](../catalogue/mappings/iran-mims.yaml) | mapping from the Iranian national coding |

## 2. Tokens

**C-01** Unit and kind tokens are two uppercase ASCII letters.

**C-02** A token is unique across the unit and kind catalogues together. A token means one
thing everywhere.

A token, once published, is never reused for a different meaning, even after it is
deprecated.

## 3. Unit entries

| Field | Meaning |
|---|---|
| `token` | the unit token |
| `name` | English and Persian names |
| `family` | liquid, solids, biogas, chemical, energy, utility or support |
| `plant_types` | `wastewater`, `water` or both |
| `status` | `active`, `provisional` or `deprecated` |
| `covers` | the physical scope of a unit of this type |

## 4. Kind entries

| Field | Meaning |
|---|---|
| `token` | the kind token |
| `name` | English and Persian names |
| `family` | the kind family |
| `placement` | `unit`, `parent` or both: where positions of this kind may appear |
| `children` | kinds allowed as children of this kind |
| `population` | whether a position of this kind may stand for a group of identical items |
| `asset_classes` | classification classes allowed for the installed asset |
| `structure_classes` | civil classes recorded on the position |
| `definition` | what positions of this kind are |

A kind's `children` list is its equipment boundary: it is the complete list of child kinds
that the serving test ([03](03-placement-rules.md), P5) can produce under it.

## 5. Classification entries

Classification has three levels. A classification reference is `<class>` or
`<class>.<type>`, for example `pump` or `pump.radial-flow`.

| Level | Field | Meaning |
|---|---|---|
| group | `id`, `name` | a broad technical family |
| class | `id`, `name`, `national` | an equipment family; class ids are unique across groups |
| type | `id`, `name`, `national` | a working principle within a class |

**5.0** A group, class or type `id` is lowercase ASCII: it matches `[a-z][a-z0-9-]*`. A
class id is unique across groups; a type id is unique within its class. A reference is
written exactly as `<class>` or `<class>.<type>`; a group is referenced by its `id` alone.
Ids are permanent: they appear in stored data, and an id once published is never reused for
another meaning.

**5.1** Types differ by working principle. Size, rating, voltage, material, make and
installation arrangement are asset attributes and never create a type.

**5.2** Each physical type has exactly one classification path. *Example.* Penstocks are
`gate.penstock`; there is no penstock type under valves and none under structures.

**5.3** Civil classes (group `civil`) are recorded on structure positions, not on assets.
Mobile classes (group `mobile`) are used for assets that have no position.

**5.4** `national` holds the equivalent Iranian MIMS code where the meaning is identical.

## 6. Status of entries

- `active` — normal use.
- `provisional` — defined but not yet tested on a real plant; MAY change in a minor version.
- `deprecated` — not used for new positions; existing positions keep their codes. A
  deprecated entry names its replacement.

## 7. Changing the catalogues

**7.1** Adding a unit, kind, class or type is a minor change.

**7.2** Changing the meaning of an existing token, class or type, or removing one, is a
major change.

**7.3** A proposed entry MUST include its names in English and Persian, its definition or
scope, and at least one real example from a plant.

**7.4** A catalogue change never recodes existing positions or reclassifies existing assets
automatically.

## 8. Catalogue checks

The catalogue rules (C-01 to C-18) are listed in [07 — Conformance](07-conformance.md) and
are checked by `tools/tpac.py check`.
