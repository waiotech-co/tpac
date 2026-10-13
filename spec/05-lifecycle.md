# 05 — Lifecycle

## L-1 Creating a position

A position is created by choosing its unit, parent, kind and number through the placement
rules ([03](03-placement-rules.md)). Its code follows from those choices. Its parent MUST
exist and be active.

## L-2 Installing an asset

Installing an asset in a position records the asset, the position and the start date. The
asset's classification MUST be allowed by the position's kind. A position holds at most one
installed asset; installing a new asset ends the previous installation.

## L-3 Replacing an asset

Replacing the asset in a position — like for like, or by a different make, model or type
that does the same job — does not change the position or its code. The outgoing asset's
installation ends; the incoming asset's installation starts. Both assets keep their own
history.

## L-4 Moving an asset

Moving an asset from one position to another ends one installation and starts another. Both
positions keep their codes. The asset keeps its asset number.

## L-5 Changing a position's function

When a position's function changes so that its kind no longer fits, the old position is
retired and a new position is created with its own code.

*Example.* Replacing a manual screen with a mechanical screen keeps the kind `SN` and the
position; only the installed asset changes. Replacing the screen with a channel grinder
changes the kind to `MC`: the screen position is retired and a grinder position is created.

## L-6 Retiring a position

A retired position keeps its code, history and installations. Its code and number are never
issued again. A position with active children cannot be retired until the children are
retired or corrected under another parent (L-8).

## L-7 Temporarily removing an asset

Removing an asset for repair leaves the position active and empty. It does not retire the
position.

## L-8 Correcting a code

A code that was issued in breach of the placement rules — wrong unit, wrong parent, wrong
kind — MAY be corrected. A correction gives the position a new code, keeps the same
position identity and history, and records the old code as a legacy code. A position's code
contains its parent's code, so a correction gives every descendant a new code as well, in the
same action, and records each old code as a legacy code of that descendant. The new codes
MUST satisfy the rules of [02](02-code-grammar.md), including the limit of 99 children of one
kind under a parent. Correction is a deliberate, recorded action; software MUST NOT recode
automatically.

## L-9 Legacy codes

Codes from earlier schemes are recorded as legacy codes of the position they identify.

- A legacy code identifies at most one position.
- A position MAY have several legacy codes.
- A legacy code MUST NOT be presented as a TPAC code.

Converting a plant from an earlier scheme is described in
[06 — National mapping](06-national-mapping.md).

## L-10 Catalogue changes

A new catalogue version does not change existing codes or classifications. Where a new
class or type would describe an asset better, reclassifying it is a deliberate, recorded
action.

## L-11 Plant code changes

A plant code changes only when the plant register changes it. All codes of the plant then
change, and every old code is recorded as a legacy code. Asset numbers do not change.

## L-12 History

Software implementing TPAC MUST keep, for every position and asset, the history of codes,
names, installations, classifications and status changes, with the date and the person
responsible for each change.
