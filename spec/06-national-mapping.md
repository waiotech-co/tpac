# 06 — National mapping

This part relates TPAC to the Iranian national wastewater equipment coding instruction
(MIMS forms, "national coding" below) and defines how a plant coded under it is converted.
The mapping data is in [`catalogue/mappings/iran-mims.yaml`](../catalogue/mappings/iran-mims.yaml).

## 1. What changes

| National coding | TPAC | Reason |
|---|---|---|
| Fixed three levels: unit (8), equipment (12), device (20) | Unit, then any number of position levels | Packages, actuators, analyzer probes and building services need a level the fixed form does not have |
| Device level = group, class, type and number | Every level = kind and number | Classification describes the installed asset and changes when the asset is replaced; an address must not |
| Unit = category letters + catalogue number (`LL19`) | Unit = unit token + instance (`BS01`) | A plant can have two areas of the same type; categories become catalogue data |
| Equipment tokens listed per unit, partly named by service (`WP`, `TP`, `LP`, `UP`, `OP` for pumps) | One kind catalogue named by function class (`PU`) | One meaning per token in every unit; service is not identity |
| "تعداد مشابه" column next to the code | No count column; one row per position; populations have a quantity | The count column led to counts being written into numbers |
| No physical asset concept | Positions and assets are separate | Replacement history and spares need both |
| Structures and building services have no equipment level | Structure kinds and building services under `BD` | Every position has a parent and a kind |
| Classification text and digits recorded separately | Classification recorded once, on the asset, from the catalogue | Text and digits disagreed |

## 2. What stays

- The plant code: company code and national plant code (`KJBJ`).
- Two-letter tokens with two-digit numbers.
- The idea of group, class and type for classification. National group 01 classes, and the
  pump and compressor types, keep their national codes as `national` references.
- Operating numbers already used on site ([03](03-placement-rules.md), P9.1).

## 3. Conversion procedure

A plant coded under the national scheme is converted row by row:

1. **Clean the source.** Apply normalization ([02](02-code-grammar.md) §5) to every code.
   Record the exact source value.
2. **Split multi-item rows.** A row whose count is greater than one becomes one row per
   item, unless the items pass the population test ([03](03-placement-rules.md), P8).
   Where the equipment count and the device count disagree, the larger count is used and
   the positions are marked for counting on site. A row of a population-capable kind whose
   maintenance practice is not stated becomes a population and is marked for confirmation.
3. **Unit.** Map the national unit with the `units` table. Where the table says
   `decide: site`, the unit map of the plant decides. Where the source row's unit
   contradicts where the item is installed, the place decides (P4).
4. **Kind.** Map the national equipment token with the `equipment_tokens` table, then
   check the result against the kind definitions. The thing's function decides (P6); the
   source token is evidence, not authority.
5. **Parent.** Apply the serving test (P5). Devices of a national equipment become children
   only when they pass it; for example, a blower's motor becomes a child of the blower,
   while a basin's structure becomes the basin position itself. Where building services
   are listed without their building, the building position is created and marked as
   inferred.
6. **Number.** Use the site's operating number (P9.1). A national number that equals the
   row's count is not an operating number.
7. **Classification.** Record the asset's class and type from the catalogue. National
   group, class and type digits are evidence; where they disagree with the description,
   the physical item decides.
8. **Legacy codes.** Record every source code as a legacy code of the resulting position
   (L-9). A source code that identified several items is recorded on none of them and
   listed in the conversion report.
9. **Other sources.** Maintenance forms, drawings and nameplates of the same plant are
   sources too. Equipment named only in them is added with its source recorded.
10. **Report.** List every row that needed a site decision, every source code that could
   not be assigned, and every item found on site but missing from the source.

## 4. Known defects in the national instruction

These defects are resolved by TPAC and are listed so that converters recognize their
effects in source data:

1. The schematic calls the number fields "تعداد مشابه" (count), while the tables call them
   "شماره مشابه" (number).
2. The worked example uses unit category `WL` with 16 units numbered differently from the
   main `LL` table of 30 units.
3. About half of the units in the national list have no equipment tokens.
4. The same physical type appears under more than one group: gates under structures (09)
   and valves (10); fixed cranes under hand tools (07).
5. Blowers appear both as class 01.11 and as compressors (01.02) in practice.
6. "PdM" is used for predetermined maintenance, while common usage reads it as predictive.
   (Outside TPAC scope; noted for converters of maintenance data.)
