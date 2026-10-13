# 01 — Model and definitions

## 1. Overview

```text
Plant ─┬─ Unit ─┬─ Position ─┬─ Position ─ …        (position tree: where things are)
       │        │            └─ Position
       │        └─ Position
       └─ Unit …

Asset ──installed in──▶ Position                      (at most one position at a time)
Asset ──classified as──▶ Class[.Type]
Position ──has kind──▶ Kind ──allows──▶ Classes, child Kinds
```

The **position tree** describes the plant: plant, units, and positions nested under units.
**Assets** are the physical objects; each is installed in at most one position at a time.
**Kinds** define what a position is for and which assets and child positions it accepts.
**Classification** describes what an asset is.

## 2. Plant

**M-1.** A plant is one treatment plant operated as one site. It is identified by a
four-character plant code ([02](02-code-grammar.md) §3).

**M-2.** Phases or modules of a site that are operated and reported as separate plants
receive separate plant codes. Phases operated as one plant share one plant code.

## 3. Unit

**M-3.** A unit is a physical area of a plant identified by its primary function. Each unit
is an instance of a unit type from the [unit catalogue](../catalogue/units.yaml).

**M-4.** The catalogue entry's `covers` text defines what a unit of that type includes.
Each plant MUST keep a unit map that marks the boundary of every unit instance on the site
plan.

**M-5.** A unit type appears more than once in a plant only when the areas are physically
separate, for example two separate blower buildings. Instances are numbered 01, 02, …

**M-6.** Every point inside the plant fence belongs to exactly one unit. Outdoor areas that
belong to no process unit belong to the site and yard unit (`YD`).

## 4. Position

**M-7.** A position is a place in the plant where a maintainable thing is installed, or a
structure that is itself maintained. A position has:

| Attribute | Required | Meaning |
|---|---|---|
| code | yes | the position's address ([02](02-code-grammar.md)) |
| parent | yes | the unit or the position it belongs to |
| kind | yes | its role, from the [kind catalogue](../catalogue/kinds.yaml) |
| index | yes | its number among siblings of the same kind |
| name | yes | a human-readable name |
| status | yes | `active` or `retired` |
| quantity | no | for a population position, the number of identical items (default 1) |
| structure class | no | for a structure position, its civil class |
| located in | no | the structure position it is physically inside (informative) |
| legacy codes | no | codes the position had under earlier schemes |

**M-8.** A position directly under a unit is an **equipment position** (تجهیز). A position
under another position is a **component position** (جزء). The difference is only depth;
both follow the same rules.

**M-9.** A position's kind determines where it may be placed (directly under a unit, under
a parent, or both), which kinds may be its children, which asset classes may be installed
in it, and whether it may be a population.

**M-10.** A **structure position** is a position of the structure family (basin, tank,
channel, chamber, pond, bed, building). A civil structure is not an asset; its civil class
is recorded on the position. A prefabricated tank or vessel is an asset installed in a
tank position.

**M-11.** A **population position** stands for a group of identical small items that are
maintained together, such as the luminaires of one building or the diffusers of one grid.
It has a quantity and no individually installed assets. Only kinds marked `population`
may be populations.

## 5. Asset

**M-12.** An asset is an individually identified physical object whose own history matters:
it is maintained, repaired, moved or replaced as one object. An asset has:

| Attribute | Required | Meaning |
|---|---|---|
| asset number | yes | its identifier ([02](02-code-grammar.md) §7) |
| classification | yes | a class, or class and type, from the [classification](../catalogue/classification.yaml) |
| manufacturer, model, serial number | no | nameplate facts |
| status | yes | `in-service` when installed, `spare` when not installed, `under-repair` when removed from its position for repair, `disposed` when permanently withdrawn |

Software MAY derive an asset's status from its installation, repair and disposal records
instead of storing it.

**M-13.** An asset is installed in at most one position at a time. A position holds at
most one installed asset at a time. Installation is recorded with its start and end dates,
so the history of both the position and the asset is preserved.

**M-14.** The asset installed in an equipment position is the main item of that position:
the pump in a pump position, the blower in a blower position. Its driver, gearbox, drive
and local panel are installed in the component positions under it.

**M-15.** An asset's classification MUST be one of the classes allowed by the kind of the
position it is installed in.

**M-16.** Parts inside an asset (bearings, seals, impellers, filter elements) are not
assets under this standard. They are spare parts and consumables.

## 6. Kind and classification

**M-17.** A kind names the role of a position by function class: pump, blower, valve,
basin. It never names the process service: a return-sludge pump and a treated-water pump
are both of kind `PU`. The service follows from the unit, the name, and any process
relationships kept outside this standard.

**M-18.** Classification describes what an asset is, in three levels: group, class and
type. Types differ by working principle. Size, rating, voltage, material, make and
installation arrangement are attributes, never types. An asset MAY be classified to class
level when its type is unknown.

## 7. Relationships outside this standard

Process units, process streams, measurement points, maintenance plans, work orders,
failures and spare parts MAY refer to positions and assets by their identity and code.
They are not part of the position tree and never change position codes.
