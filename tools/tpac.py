#!/usr/bin/env python3
"""Reference validator for the TPAC standard.

Commands:
  check                     Validate the catalogues against the catalogue rules (C-rules).
  parse CODE [CODE ...]     Normalize, validate and explain position codes and asset numbers
                            (G-, S- and A-rules).
  register FILE.csv         Validate a plant position register (G-, S- and R-rules).

Requires Python 3.9+ and PyYAML.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CATALOGUE_DIR = ROOT / "catalogue"

TOKEN_RE = re.compile(r"^[A-Z]{2}$")
CLASSIFICATION_ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")
PLANT_RE = re.compile(r"^[A-Z]{2}[A-Z][A-Z0-9]$")
SEGMENT_RE = re.compile(r"^[A-Z]{2}[0-9]{2}$")
ASSET_NUMBER_RE = re.compile(r"^[A-Z]{2}[A-Z][A-Z0-9]A[0-9]{6}$")
ASSET_NUMBER_LENGTH = 11
SEPARATORS = re.compile(r"[\s\-_.‌]+")
DIGIT_MAP = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
PLANT_TYPES = {"wastewater", "water"}
STATUSES = {"active", "provisional", "deprecated"}
PLACEMENTS = {"unit", "parent"}


# --------------------------------------------------------------------------- catalogue


@dataclass
class Catalogue:
    units: dict
    kinds: dict
    classes: dict
    types: dict
    unit_families: set
    kind_families: set
    building_services: list
    raw: dict = field(default_factory=dict)


def load_catalogue(directory: Path = CATALOGUE_DIR) -> Catalogue:
    units_doc = yaml.safe_load((directory / "units.yaml").read_text(encoding="utf-8"))
    kinds_doc = yaml.safe_load((directory / "kinds.yaml").read_text(encoding="utf-8"))
    class_doc = yaml.safe_load((directory / "classification.yaml").read_text(encoding="utf-8"))
    units = {u["token"]: u for u in units_doc["units"]}
    kinds = {k["token"]: k for k in kinds_doc["kinds"]}
    classes, types = {}, {}
    for group in class_doc["groups"]:
        for cls in group["classes"]:
            cls = dict(cls, group=group["id"])
            classes[cls["id"]] = cls
            for typ in cls.get("types") or []:
                types[f'{cls["id"]}.{typ["id"]}'] = dict(typ, cls=cls["id"])
    return Catalogue(
        units=units,
        kinds=kinds,
        classes=classes,
        types=types,
        unit_families={f["id"] for f in units_doc["families"]},
        kind_families={f["id"] for f in kinds_doc["families"]},
        building_services=kinds_doc.get("building_services", []),
        raw={"units": units_doc, "kinds": kinds_doc, "classification": class_doc, "dir": directory},
    )


def has_names(entry: dict) -> bool:
    name = entry.get("name")
    return (
        isinstance(name, dict)
        and set(name) == {"en", "fa"}
        and all(isinstance(text, str) and text.strip() for text in name.values())
    )


def sibling_groups(cat: Catalogue):
    groups = cat.raw["classification"]["groups"]
    yield "groups", [(g["id"], g) for g in groups]
    for group in groups:
        yield f"classes of group {group['id']}", [(c["id"], c) for c in group["classes"]]
        for cls in group["classes"]:
            yield f"types of class {cls['id']}", [(t["id"], t) for t in cls.get("types") or []]


def check_catalogue(cat: Catalogue) -> list[tuple[str, str]]:
    problems: list[tuple[str, str]] = []

    def bad(rule: str, msg: str) -> None:
        problems.append((rule, msg))

    unit_list = cat.raw["units"]["units"]
    kind_list = cat.raw["kinds"]["kinds"]
    all_tokens = [u["token"] for u in unit_list] + [k["token"] for k in kind_list]
    for tok in all_tokens:
        if not TOKEN_RE.match(str(tok)):
            bad("C-01", f"token {tok!r} is not two uppercase ASCII letters")
    seen: dict[str, int] = {}
    for tok in all_tokens:
        seen[tok] = seen.get(tok, 0) + 1
    for tok, n in seen.items():
        if n > 1:
            bad("C-02", f"token {tok} is used {n} times across units and kinds")

    for u in unit_list:
        if u.get("family") not in cat.unit_families:
            bad("C-03", f"unit {u['token']}: unknown family {u.get('family')!r}")
        if not u.get("plant_types") or not set(u["plant_types"]) <= PLANT_TYPES:
            bad("C-04", f"unit {u['token']}: plant_types must be a non-empty subset of {sorted(PLANT_TYPES)}")
        if u.get("status") not in STATUSES:
            bad("C-05", f"unit {u['token']}: status must be one of {sorted(STATUSES)}")
        if not has_names(u):
            bad("C-06", f"unit {u['token']}: exactly an English and a Persian name are required")
        if not u.get("covers"):
            bad("C-07", f"unit {u['token']}: `covers` is required")

    child_of: dict[str, list[str]] = {}
    for k in kind_list:
        tok = k["token"]
        if k.get("family") not in cat.kind_families:
            bad("C-03", f"kind {tok}: unknown family {k.get('family')!r}")
        if not has_names(k):
            bad("C-06", f"kind {tok}: exactly an English and a Persian name are required")
        if not k.get("definition"):
            bad("C-07", f"kind {tok}: `definition` is required")
        placement = set(k.get("placement") or [])
        if not placement or not placement <= PLACEMENTS:
            bad("C-08", f"kind {tok}: placement must be a non-empty subset of {sorted(PLACEMENTS)}")
        for c in k.get("asset_classes") or []:
            if c not in cat.classes:
                bad("C-09", f"kind {tok}: unknown asset class {c!r}")
            elif cat.classes[c]["group"] in ("civil", "mobile"):
                bad("C-09", f"kind {tok}: asset class {c!r} belongs to group {cat.classes[c]['group']}")
        for c in k.get("structure_classes") or []:
            if c not in cat.classes or cat.classes[c]["group"] != "civil":
                bad("C-10", f"kind {tok}: structure class {c!r} must be a civil class")
        if not (k.get("asset_classes") or k.get("structure_classes")):
            bad("C-11", f"kind {tok}: at least one asset class or structure class is required")
        for ch in k.get("children") or []:
            if ch not in cat.kinds:
                bad("C-12", f"kind {tok}: unknown child kind {ch!r}")
                continue
            if "parent" not in (cat.kinds[ch].get("placement") or []):
                bad("C-13", f"kind {tok}: child {ch} does not allow placement under a parent")
            child_of.setdefault(ch, []).append(tok)
    for k in kind_list:
        if "parent" in (k.get("placement") or []) and k["token"] not in child_of:
            bad("C-15", f"kind {k['token']}: placement allows a parent but no kind lists it as a child")
    if "BD" in cat.kinds and sorted(cat.kinds["BD"].get("children") or []) != sorted(cat.building_services):
        bad("C-16", "kind BD children must equal the building_services list")

    class_ids: dict[str, int] = {}
    for group in cat.raw["classification"]["groups"]:
        if not CLASSIFICATION_ID_RE.match(str(group["id"])):
            bad("C-20", f"group id {group['id']!r} must match [a-z][a-z0-9-]*")
        for cls in group["classes"]:
            if not CLASSIFICATION_ID_RE.match(str(cls["id"])):
                bad("C-20", f"class id {cls['id']!r} must match [a-z][a-z0-9-]*")
            for typ in cls.get("types") or []:
                if not CLASSIFICATION_ID_RE.match(str(typ["id"])):
                    bad("C-20", f"type id {cls['id']}.{typ['id']!r} must match [a-z][a-z0-9-]*")
            class_ids[cls["id"]] = class_ids.get(cls["id"], 0) + 1
            if not has_names(cls):
                bad("C-06", f"class {cls['id']}: exactly an English and a Persian name are required")
            type_ids = [t["id"] for t in cls.get("types") or []]
            for t in set(type_ids):
                if type_ids.count(t) > 1:
                    bad("C-17", f"class {cls['id']}: type {t!r} is defined twice")
            for t in cls.get("types") or []:
                if not has_names(t):
                    bad("C-06", f"type {cls['id']}.{t['id']}: exactly an English and a Persian name are required")
    for cid, n in class_ids.items():
        if n > 1:
            bad("C-17", f"class {cid!r} is defined {n} times")
    for scope, entries in sibling_groups(cat):
        for language in ("en", "fa"):
            seen: dict[str, str] = {}
            for entry_id, entry in entries:
                label = " ".join(str(entry["name"][language]).casefold().split())
                if label in seen:
                    bad("C-21", f"{scope}: {entry_id} and {seen[label]} have the same {language} name {entry['name'][language]!r}")
                seen[label] = entry_id
    national: dict[str, str] = {}
    for tid, t in cat.types.items():
        if t.get("national"):
            if t["national"] in national and not t["national"].count(".") == 1:
                bad("C-18", f"national code {t['national']} maps to both {national[t['national']]} and {tid}")
            national.setdefault(t["national"], tid)

    group_ids = {g["id"] for g in cat.raw["classification"]["groups"]}
    for mfile in sorted((cat.raw["dir"] / "mappings").glob("*.yaml")):
        mdoc = yaml.safe_load(mfile.read_text(encoding="utf-8"))
        for section, valid in (("units", cat.units), ("equipment_tokens", cat.kinds), ("groups", group_ids)):
            for src, entry in (mdoc.get(section) or {}).items():
                targets = entry.get("to")
                targets = targets if isinstance(targets, list) else [targets]
                for tgt in targets:
                    if tgt is not None and tgt not in valid:
                        bad("C-19", f"{mfile.name} {section}.{src}: target {tgt!r} does not exist")
    return problems


# --------------------------------------------------------------------------- codes


def normalize(raw: str) -> str:
    return SEPARATORS.sub("", str(raw).translate(DIGIT_MAP)).upper()


@dataclass
class Parsed:
    raw: str
    code: str
    plant: str = ""
    unit: str = ""
    segments: list = field(default_factory=list)
    errors: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    @property
    def parent(self) -> str | None:
        if len(self.code) <= 8:
            return None
        return self.code[:-4]

    @property
    def kind(self) -> str | None:
        return self.segments[-1][0] if self.segments else None


def parse_code(raw: str, cat: Catalogue) -> Parsed:
    code = normalize(raw)
    p = Parsed(raw=raw, code=code)
    if not re.fullmatch(r"[A-Z0-9]*", code):
        p.errors.append(("G-01", "only letters A-Z and digits 0-9 are allowed"))
        return p
    if len(code) < 8 or len(code) % 4:
        p.errors.append(("G-02", f"length {len(code)} is not 8, 12, 16, ..."))
        return p
    p.plant = code[:4]
    if not PLANT_RE.match(p.plant):
        p.errors.append(("G-03", f"plant code {p.plant!r} must be two letters, a letter, and a letter or digit"))
    unit_seg = code[4:8]
    if not SEGMENT_RE.match(unit_seg):
        p.errors.append(("G-04", f"unit segment {unit_seg!r} must be two letters and two digits"))
        return p
    utok, inst = unit_seg[:2], unit_seg[2:]
    if utok not in cat.units:
        p.errors.append(("G-04", f"unit token {utok} is not in the unit catalogue"))
    if inst == "00":
        p.errors.append(("G-05", "unit instance 00 is not allowed"))
    p.unit = unit_seg
    prev_kind = None
    for i in range(8, len(code), 4):
        seg = code[i:i + 4]
        if not SEGMENT_RE.match(seg):
            p.errors.append(("G-06", f"segment {seg!r} must be two letters and two digits"))
            return p
        ktok, idx = seg[:2], seg[2:]
        p.segments.append((ktok, idx))
        if ktok not in cat.kinds:
            p.errors.append(("G-06", f"kind token {ktok} is not in the kind catalogue"))
            prev_kind = None
            continue
        if idx == "00":
            p.errors.append(("G-07", f"index 00 in segment {seg} is not allowed"))
        kind = cat.kinds[ktok]
        if prev_kind is None and i == 8:
            if "unit" not in kind["placement"]:
                p.errors.append(("S-01", f"{ktok} ({kind['name']['en']}) cannot be placed directly under a unit"))
        elif prev_kind is not None:
            if ktok not in (cat.kinds[prev_kind].get("children") or []):
                p.errors.append(("S-02", f"{ktok} ({kind['name']['en']}) is not an allowed child of "
                                          f"{prev_kind} ({cat.kinds[prev_kind]['name']['en']})"))
        prev_kind = ktok
    return p


def parse_asset_number(raw: str) -> Parsed:
    code = normalize(raw)
    p = Parsed(raw=raw, code=code)
    if not ASSET_NUMBER_RE.match(code):
        p.errors.append(("A-01", "an asset number is a plant code, the letter A and six digits"))
        return p
    p.plant = code[:4]
    return p


def explain(p: Parsed, cat: Catalogue) -> str:
    lines = [f"{p.raw!s}  ->  {p.code}"]
    if p.plant:
        lines.append(f"  plant     {p.plant}")
    if p.unit and p.unit[:2] in cat.units:
        u = cat.units[p.unit[:2]]
        lines.append(f"  unit      {p.unit}  {u['name']['en']} {int(p.unit[2:])} / {u['name']['fa']}")
    for depth, (k, idx) in enumerate(p.segments, start=1):
        if k in cat.kinds:
            kn = cat.kinds[k]["name"]
            lines.append(f"  {'  ' * (depth - 1)}position  {k}{idx}  {kn['en']} {int(idx)} / {kn['fa']}")
    for rule, msg in p.errors:
        lines.append(f"  ERROR {rule}: {msg}")
    lines.append("  valid" if p.ok else "  invalid")
    return "\n".join(lines)


# --------------------------------------------------------------------------- register


REGISTER_COLUMNS = ["code", "name", "quantity", "structure_class", "asset_class", "legacy_codes", "status"]


def check_register(path: Path, cat: Catalogue, plant_type: str | None) -> tuple[list, int]:
    findings: list[tuple[str, str, str]] = []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        missing = [c for c in ("code", "name") if c not in (reader.fieldnames or [])]
        if missing:
            return [("R-00", "", f"missing required columns: {', '.join(missing)}")], 0
        rows = list(reader)

    codes: dict[str, int] = {}
    parsed: dict[str, Parsed] = {}
    aliases: dict[str, str] = {}
    plants: set[str] = set()
    for n, row in enumerate(rows, start=2):
        raw = (row.get("code") or "").strip()
        p = parse_code(raw, cat)
        ref = f"line {n} {p.code if len(p.code) >= 8 else raw}"
        for rule, msg in p.errors:
            findings.append((rule, ref, msg))
        if p.code in codes:
            findings.append(("R-01", ref, f"duplicate of line {codes[p.code]}"))
        codes.setdefault(p.code, n)
        parsed[p.code] = p
        if p.plant:
            plants.add(p.plant)
        if not (row.get("name") or "").strip():
            findings.append(("R-09", ref, "name is required"))
        status = (row.get("status") or "active").strip() or "active"
        if status not in ("active", "retired"):
            findings.append(("R-10", ref, f"status {status!r} must be active or retired"))

        if p.unit and p.unit[:2] in cat.units and plant_type:
            unit = cat.units[p.unit[:2]]
            if plant_type not in unit["plant_types"]:
                findings.append(("R-08", ref, f"unit {unit['token']} is not defined for {plant_type} plants"))

        kind = cat.kinds.get(p.kind) if p.kind else None
        qty_raw = (row.get("quantity") or "").strip()
        if qty_raw:
            if not qty_raw.isdigit() or int(qty_raw) < 1:
                findings.append(("R-03", ref, f"quantity {qty_raw!r} must be a whole number of at least 1"))
            elif int(qty_raw) > 1 and (kind is None or not kind.get("population")):
                findings.append(("R-03", ref, f"quantity {qty_raw} on kind {p.kind}, which does not allow populations"))

        ac = (row.get("asset_class") or "").strip()
        if ac:
            cls = ac.split(".")[0]
            if ac not in cat.classes and ac not in cat.types:
                findings.append(("R-04", ref, f"asset class {ac!r} is not in the classification"))
            elif kind is None:
                findings.append(("R-04", ref, "a unit carries no asset class"))
            elif cls not in (kind.get("asset_classes") or []):
                findings.append(("R-04", ref, f"asset class {ac!r} is not allowed for kind {p.kind} "
                                              f"(allowed: {', '.join(kind.get('asset_classes') or []) or 'none'})"))
        sc = (row.get("structure_class") or "").strip()
        if sc:
            cls = sc.split(".")[0]
            if sc not in cat.classes and sc not in cat.types:
                findings.append(("R-05", ref, f"structure class {sc!r} is not in the classification"))
            elif kind is None or cls not in (kind.get("structure_classes") or []):
                findings.append(("R-05", ref, f"structure class {sc!r} is not allowed for "
                                              f"{'a unit' if kind is None else 'kind ' + p.kind}"))

        for alias in filter(None, (a.strip() for a in (row.get("legacy_codes") or "").split(";"))):
            if alias in aliases and aliases[alias] != p.code:
                findings.append(("R-06", ref, f"legacy code {alias} is already an alias of {aliases[alias]}"))
            aliases.setdefault(alias, p.code)

    for code, p in parsed.items():
        if p.ok and p.parent and p.parent not in parsed:
            findings.append(("R-02", f"line {codes[code]} {code}",
                             f"parent {p.parent} is not in the register"))
    if len(plants) > 1:
        findings.append(("R-07", "", f"register mixes plant codes: {', '.join(sorted(plants))}"))
    return findings, len(rows)


# --------------------------------------------------------------------------- cli


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="tpac", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--catalogue", type=Path, default=CATALOGUE_DIR, help="catalogue directory")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="validate the catalogues")
    pp = sub.add_parser("parse", help="validate and explain codes")
    pp.add_argument("codes", nargs="+")
    rp = sub.add_parser("register", help="validate a position register CSV")
    rp.add_argument("file", type=Path)
    rp.add_argument("--plant-type", choices=sorted(PLANT_TYPES))
    args = ap.parse_args(argv)

    cat = load_catalogue(args.catalogue)
    if args.cmd == "check":
        problems = check_catalogue(cat)
        for rule, msg in problems:
            print(f"{rule}  {msg}")
        print(f"{len(cat.units)} units, {len(cat.kinds)} kinds, {len(cat.classes)} classes, "
              f"{len(cat.types)} types: {'OK' if not problems else f'{len(problems)} problem(s)'}")
        return 1 if problems else 0
    if args.cmd == "parse":
        failed = 0
        for raw in args.codes:
            if len(normalize(raw)) == ASSET_NUMBER_LENGTH:
                p = parse_asset_number(raw)
                print(f"{raw!s}  ->  {p.code}  (asset number)")
                for rule, msg in p.errors:
                    print(f"  ERROR {rule}: {msg}")
                print("  valid" if p.ok else "  invalid")
            else:
                p = parse_code(raw, cat)
                print(explain(p, cat))
            failed += not p.ok
        return 1 if failed else 0
    if args.cmd == "register":
        findings, n = check_register(args.file, cat, args.plant_type)
        for rule, ref, msg in findings:
            print(f"{rule}  {ref}: {msg}" if ref else f"{rule}  {msg}")
        print(f"{n} rows: {'OK' if not findings else f'{len(findings)} finding(s)'}")
        return 1 if findings else 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
