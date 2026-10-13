# 02 — Code grammar

## 1. Structure

A position code is a plant code followed by a unit segment and zero or more position
segments. Every segment is four characters: two letters and two digits.

```text
KJBJ  BS01  BW05  MO01
│     │     │     └── position segment: kind MO (motor), index 01
│     │     └──────── position segment: kind BW (blower), index 05
│     └────────────── unit segment: unit type BS (blower station), instance 01
└──────────────────── plant code
```

Formal grammar (ABNF, RFC 5234):

```abnf
unit-code        = plant-code unit-segment
position-code    = unit-code 1*position-segment
plant-code       = 2UPALPHA UPALPHA (UPALPHA / DIGIT)
unit-segment     = unit-token number
position-segment = kind-token number
unit-token       = 2UPALPHA          ; a token from the unit catalogue
kind-token       = 2UPALPHA          ; a token from the kind catalogue
number           = 2DIGIT            ; 01 to 99; 00 is never used
UPALPHA          = %x41-5A           ; A-Z
DIGIT            = %x30-39           ; 0-9
```

A code's length is always 8 (unit), 12, 16, 20, … characters. The kind of every segment and
the parent of every position can be read from the code without any other information: the
parent of a position is its code without the last four characters.

## 2. Validity

A code is valid when:

- **G-01** it contains only the characters A–Z and 0–9 after normalization (§5);
- **G-02** its length is 8 + 4n;
- **G-03** its plant code matches the grammar;
- **G-04** its unit segment is two letters and two digits, and its unit token is in the unit
  catalogue;
- **G-05** its unit instance is between 01 and 99;
- **G-06** every position segment is two letters and two digits, and its kind token is in
  the kind catalogue;
- **G-07** every index is between 01 and 99;
- **S-01** the first position segment has a kind that may be placed directly under a unit;
- **S-02** every further segment has a kind listed as an allowed child of the previous
  segment's kind.

Rules S-01 and S-02 make the structure of a code checkable from the code alone.

## 3. Plant code

The plant code is four characters: two uppercase letters, one uppercase letter, and one
uppercase letter or digit. Plant codes are assigned by the register that the plant belongs
to and MUST be unique within it.

*Note.* For Iranian water and wastewater companies, the plant code is the company code
followed by the plant code from the national register, for example `KJBJ`. Where the
national register contains duplicates, the register owner resolves them before codes are
issued.

## 4. Numbers

**4.1** The unit instance numbers the instances of one unit type within a plant. The
position index numbers the positions of one kind under one parent. Both run from 01.

**4.2** Numbers are identifiers, never counts. `BW05` is blower number 5, not five blowers.

**4.3** A number, once issued under a parent, is never reused for another position under
that parent, even after retirement. Gaps are allowed. The same holds for unit instances,
whose parent is the plant: an instance number issued for a unit type is never reused in that
plant.

**4.4** A parent has at most 99 children of one kind. Groups of identical small items are
populations ([03](03-placement-rules.md), P8). Where more than 99 individual positions of
one kind are needed, the unit is divided into instances.

**4.5** The order in which numbers are assigned is defined in
[03](03-placement-rules.md), P9.

## 5. Normalization

Software accepting a code from a person or a file MUST normalize it as follows before
validation, and MUST NOT apply any other correction:

1. convert Persian and Arabic-Indic digits to ASCII digits;
2. remove spaces, hyphens, underscores, dots and zero-width non-joiners;
3. convert letters to uppercase.

Anything that is still invalid after normalization is an error for a person to resolve.

## 6. Written form

A code has one written form: the characters of the code with no separators, for example
`KJBJBS01BW05MO01`. Labels, drawings, documents, files and software MUST write codes in this
form. Segments are recognized by their fixed widths, so no separator is needed to read
them: plant (4), unit (4), then 4 characters per position segment.

Normalization (§5) lets software accept a code typed with spaces or hyphens; it never
writes one back that way.

## 7. Asset number

An asset number identifies a physical asset:

```abnf
asset-number = plant-code "A" 6DIGIT
```

Example: `KJBJA000123`. The plant code is the plant that first
registered the asset; it does not change when the asset moves. Asset numbers are issued in
sequence, carry no meaning, and are never reused. An asset number cannot be mistaken for a
position code: its length is 11, and a position code's length is a multiple of 4.

## 8. What a code never contains

A position code MUST NOT encode classification, make, model, rating, process service,
train, criticality, condition, status, quantity or dates. A code that would change when any
of these changes is not a valid TPAC code.
