# 03 — Placement rules

This part decides, for any physical thing in a plant, whether it gets a position, which
unit it belongs to, what its parent is, what kind it is, whether it is individual or a
population, and what number it gets. The rules are applied in order, P1 to P10.

## Decision procedure

```text
P1  Does it get a position at all?        no  → not coded (inventory, tools, furniture)
P2  Is it mobile or portable?             yes → asset only, with a home unit
P3  Is it a spare, not installed?         yes → asset only, not installed
P4  Which unit?                           the unit whose area contains it
P5  Which parent?                         the position it serves, or else the unit
P6  Which kind?                           by function class
P7  Structure?                            record the civil class on the position
P8  Individual or population?             by the population test
P9  Which number?                         established number, or else the ordering rule
P10 Which name?                           by the naming rule
```

## P1 — Coding threshold

**P1.1** A thing gets a position when it is installed at a fixed place in the plant and at
least one of the following is true:

1. it needs maintenance, inspection, testing or calibration that is recorded;
2. its failure affects treatment, safety, compliance or the supply of power, air or water;
3. it is a civil structure (basin, tank, channel, chamber, pond, bed, building).

**P1.2** The following never get positions:

- spare parts, consumables, chemicals and lubricants (inventory);
- hand tools and workshop hand equipment;
- furniture, shelving, cabinets, benches and fittings;
- laboratory glassware and small lab ware;
- pipes, pipe fittings and cables;
- computer peripherals (monitors, keyboards, printers) and video displays; they are parts
  of the workstation or recorder they serve;
- software and licences.

*Example.* A laboratory spectrophotometer is calibrated and repaired: it gets a position.
A set of pipettes does not.

## P2 — Mobile and portable equipment

**P2.1** Equipment that is moved between places in normal use is registered as an asset
with a home unit and gets no position: vehicles, portable pumps and generators, portable
meters and gas detectors, breathing apparatus, condition monitoring instruments.

**P2.2** Equipment that is installed and connected at a fixed place is not portable, even
if it could be moved.

## P3 — Spares and uninstalled assets

An asset that is not installed — a spare motor, a pump at the workshop — keeps its asset
number and classification and has no current installation. It does not get a position.

## P4 — Unit

**P4.1** A position belongs to the unit whose area, as defined by the catalogue `covers`
text and the plant's unit map, contains the place where it is installed.

**P4.2** When the catalogue text and the place disagree, the place decides. *Example.* The
`GR` text includes air supply installed at the grit chambers; blowers housed in a separate
blower building belong to that building's `BS` unit.

**P4.3** A component position always belongs to the unit of its parent, even when it is
mounted elsewhere (P5.4).

**P4.4** Equipment that extends over two units belongs to the unit that contains its drive
or, if it has no drive, its fixed anchorage.

**P4.5** Equipment that serves several units belongs to the unit where it is installed. The
units it serves are recorded as relationships, not in the code.

**P4.6** A building belongs to exactly one unit, given by the unit map. Everything installed
in a building belongs to that building's unit. A catalogue `covers` text never moves an item
out of the building it stands in. *Example.* Thickening machines installed in the dewatering
building belong to the dewatering unit.

## P5 — Parent

**P5.1 The serving test.** A thing X is a child of a position Y when both hold:

1. X exists only to make Y work: it drives, powers, controls, protects, monitors, supports
   or services Y, and serves nothing else; and
2. Y's kind lists X's kind as an allowed child.

Otherwise X is placed directly under its unit.

**P5.2** A thing that serves several positions is placed under the unit. *Example.* A
common discharge header valve of three pumps is a unit-level valve; each pump's own check
valve is a child of that pump.

**P5.3** A thing that acts on the process, rather than on another position, is placed
under the unit, even when it is installed inside a structure. Mixers, aerators, diffuser
grids, gates and sludge collectors in a basin are unit-level positions. The basin they are
in MAY be recorded as the position's `located in` attribute.

P5.3 does not apply to a valve or gate that isolates one machine. Such a valve or gate
exists only to make that machine work and is the machine's child under P5.1.

**P5.4** A dedicated driver, gearbox, drive or starter, and local control panel are
children of the machine they serve, wherever they are mounted. *Example.* A variable
frequency drive in the motor control centre, dedicated to blower 5, is a child of blower 5;
the motor control centre itself is a unit-level switchboard.

**P5.5 Building services.** Lighting, distribution boards, HVAC, ventilation fans, powered
doors, elevators, earthing, fire extinguishers, hydrants, fire suppression, fire alarm,
emergency showers and first aid stations that serve one building are children of that
building's `BD` position. The same things outdoors are unit-level positions.

**P5.6 Packages.** Everything supplied and mounted on a package is a child of the package
position (`PK`), even if it could be maintained on its own.

**P5.7 Instruments.** An instrument that monitors a machine (bearing temperature, a pump's
discharge pressure gauge, a screen's differential level) is a child of that machine. An
instrument that measures the process (basin oxygen, channel flow, tank level) is a
unit-level position. The probes of an analyzer are children of the analyzer. Local and
remote displays are parts of the instrument they display and get no position.

**P5.8 Auxiliary machines.** A pump, fan or compressor that exists only to serve one
machine — lubrication, seal water, cooling, cleaning, belt tracking — is a child of that
machine.

### Determinations

| Thing | Parent |
|---|---|
| Motor, gearbox, drive, starter, local panel of a machine | the machine |
| Isolation and check valves dedicated to one pump or blower | the pump or blower |
| Gate isolating one pump (for example in front of a screw lift pump) | the pump |
| Grease or lubrication pump of one machine | the machine |
| Header, line and distribution valves | unit |
| Actuator of a valve or gate | the valve or gate |
| Valve or gate isolating a basin, channel or filter | unit (filter cell valves: the filter) |
| Pump carried on a sludge collector bridge | the collector |
| Mixer, aerator, diffuser grid, gate or collector in a basin | unit |
| Analyzer probe | the analyzer |
| Basin dissolved oxygen, pH, ORP, MLSS analyzer | unit |
| Pressure gauge on one pump's discharge | the pump |
| Pressure gauge on a common header | unit |
| Lighting, HVAC, extinguisher in a building | the building |
| Yard lighting, lighting tower, outdoor extinguisher | unit |
| Crane in a building | unit |
| Motor control centre, main distribution board | unit |
| Distribution or lighting board serving only one building | the building |
| Pump, mixer, tank, valve mounted on a dosing skid | the package |
| Day tank and fuel pump of a generator set | the generator set |

## P6 — Kind

**P6.1** The kind is the catalogue kind whose definition matches the thing's function
class. The process service never decides the kind.

**P6.2** A kind is chosen once for a position. If the thing installed there later turns out
to be classified differently, the asset's classification is corrected; the kind changes
only if the function changes ([05](05-lifecycle.md), L-5).

### Determinations

| Thing | Kind |
|---|---|
| Any pump, including screw lift, airlift, dosing and submersible pumps | `PU` |
| A dosing skid with pumps, tank and instruments | `PK` |
| Polymer preparation unit | `PK` |
| Flocculator | `MX` |
| Grit chamber air blowers | `BW` |
| Sludge scraper bridge, rotating scraper, chain-and-flight | `SM` |
| Separate scum skimmer | `SK` |
| Grit classifier, hydrocyclone, grit washer | `GC` |
| Screenings washer-compactor, screw press for screenings | `CP` |
| Belt press, centrifuge, sludge screw press, belt or drum thickener | `SX` |
| Penstock, slide gate, weir gate, stop log | `GA` |
| Motorized butterfly valve | `VA` with child `AT` |
| Parshall flume with ultrasonic level transmitter | `CH` for the flume, `FM` for the measurement |
| Chlorine storage cylinder rack | not a position (cylinders are consumables) |
| Gas chlorinator, hypochlorite generator | `DZ` |
| Split air conditioner | `HV` |
| Exhaust fan in a building | `FN` (child of the building) |
| Diesel standby generator | `GE` |
| Integral geared motor | `MO` (no separate `GB`) |
| MV switchgear of ten cubicles in one line-up | one `SW` |
| Bench grinder, drill press, lathe | `WM` |
| Paved sludge storage pad, plant road | `HS` |
| Server, operator workstation | `IT` |
| Multi-parameter analyzer with three probes | `QM` with three `SE` children |

## P7 — Structures

**P7.1** Basins, concrete tanks, channels, chambers, ponds, beds, hardstandings and
buildings are structure positions of kinds `BA`, `TK`, `CH`, `CM`, `PD`, `BE`, `HS` and `BD`.
Their civil class is recorded on the position.

**P7.2** Civil work on a structure — concrete repair, coating, roof repair — targets the
structure position.

**P7.3** Each building in a unit is a `BD` position, including a building that houses the
whole unit.

**P7.4** A prefabricated steel, GRP or polyethylene tank or pressure vessel is an asset
installed in a `TK` position.

## P8 — Individual or population

**P8.1** Items of one kind under one parent are a single population position when all of
these hold:

1. the kind is marked `population` in the catalogue;
2. the items are identical in classification and duty;
3. they are maintained, inspected and replaced as a group, with no record kept per item;
4. none of them is safety-critical on its own.

Otherwise each item gets its own position.

**P8.2** Fire extinguishers, gas detectors, hydrants and emergency showers are always
individual. Luminaires and diffusers are normally populations.

**P8.3** A population position records its quantity. Changing the quantity does not change
the code.

## P9 — Numbering

**P9.1** When a thing already has an established operating number on site — painted on the
equipment, used in SCADA, on the P&ID or in operating instructions — that number MUST be
used as the index, provided it is between 01 and 99 and unique among siblings of the same
kind.

**P9.2** Otherwise numbers are assigned in this order:

1. in process flow order;
2. among parallel items, from left to right as seen looking downstream;
3. for items not on a flow path, clockwise from the main entrance of the building or area;
4. for items on several floors, from the lowest floor upward.

**P9.3** Unit instances are numbered in order of commissioning; where that is unknown, in
process flow order.

**P9.4** Equipment in parallel trains SHOULD be numbered train by train, so that the
numbers of one train are consecutive. *Example.* Two mixers in each of four anoxic basins
are `MX01`–`MX02` in basin 1, `MX03`–`MX04` in basin 2, and so on.

## P10 — Naming

**P10.1** Every position has a name. The default name is the kind's name followed by the
number: "Blower 5", "Motor 1".

**P10.2** A position MAY have a more specific name that identifies it on site: "Anoxic
basin 2 mixer 1", "Blower 5 drive motor". A name never replaces the code and need not be
unique.

**P10.3** A full name is formed by joining the names along the path: "Blower station 1 ›
Blower 5 › Motor 1".

## Worked examples

### Blower station

```text
KJBJBS01                  Blower station 1
├─ KJBJBS01BD01          Building 1                   structure class building.steel-frame
│  ├─ KJBJBS01BD01LI01     Lighting (quantity 8)
│  ├─ KJBJBS01BD01SW01     Lighting board
│  ├─ KJBJBS01BD01HV01     Split air conditioner
│  ├─ KJBJBS01BD01FE01     Fire extinguisher 1
│  └─ KJBJBS01BD01FE02     Fire extinguisher 2
├─ KJBJBS01BW05          Blower 5                     asset: blower.rotary-lobe
│  ├─ KJBJBS01BW05MO01     Motor                        asset: motor.induction-cage-3ph
│  ├─ KJBJBS01BW05VF01     Drive (in the MCC)           asset: drive.vfd
│  ├─ KJBJBS01BW05VA01     Discharge valve              asset: valve.butterfly
│  │  └─ KJBJBS01BW05VA01AT01  Actuator                     asset: actuator.electric-quarter-turn
│  ├─ KJBJBS01BW05VA02     Safety valve                 asset: valve.pressure-relief
│  └─ KJBJBS01BW05PM01     Discharge pressure gauge     asset: pressure-instrument.gauge
├─ KJBJBS01VA01          Air header isolation valve
├─ KJBJBS01FM01          Air header flow measurement  asset: flow-instrument.thermal-mass
├─ KJBJBS01SW01          Motor control centre         asset: switchboard.motor-control-centre
└─ KJBJBS01CR01          Overhead crane               asset: lifting.overhead-travelling-crane
```

### Screening

```text
KJBJSR01                  Screening 1
├─ KJBJSR01CH01          Coarse screen channel 1      structure class channel.open-concrete
├─ KJBJSR01CH02          Coarse screen channel 2
├─ KJBJSR01GA01          Channel 1 inlet gate         asset: gate.penstock
│  └─ KJBJSR01GA01AT01     Actuator
├─ KJBJSR01GA02          Channel 2 inlet gate
├─ KJBJSR01SN01          Manual coarse screen         asset: screen.manual-bar
├─ KJBJSR01SN02          Mechanical coarse screen     asset: screen.multi-rake-bar
│  ├─ KJBJSR01SN02MO01     Motor
│  ├─ KJBJSR01SN02GB01     Gearbox
│  ├─ KJBJSR01SN02LP01     Local control panel
│  └─ KJBJSR01SN02LM01     Differential level           asset: level-instrument.ultrasonic
├─ KJBJSR01CV01          Screenings belt conveyor
│  └─ KJBJSR01CV01MO01     Motor (geared)               asset: motor.geared-motor
└─ KJBJSR01CP01          Washer compactor
```

### Anoxic zone

```text
KJBJAN01                  Anoxic zone 1
├─ KJBJAN01BA01 … BA04   Anoxic basins 1–4            structure class civil-basin.rectangular-concrete
├─ KJBJAN01MX01          Basin 1 mixer 1              located in BA01
│  └─ KJBJAN01MX01MO01     Motor
├─ KJBJAN01MX02          Basin 1 mixer 2              located in BA01
├─ KJBJAN01MX03          Basin 2 mixer 1              located in BA02
├─ …
├─ KJBJAN01GA01 … GA04   Basin inlet gates
└─ KJBJAN01QM01          ORP analyzer, basin 1        asset: analyzer.orp
   └─ KJBJAN01QM01SE01     ORP probe
```

### Chlorine dosing package

```text
KJBJDI01PK01             Hypochlorite dosing package  asset: package.chemical-dosing
├─ KJBJDI01PK01TK01        Day tank                     asset: vessel.polyethylene-tank
├─ KJBJDI01PK01PU01        Dosing pump 1                asset: pump.diaphragm
├─ KJBJDI01PK01PU02        Dosing pump 2
├─ KJBJDI01PK01PM01        Discharge pressure gauge
├─ KJBJDI01PK01FM01        Dosing flow meter            asset: flow-instrument.electromagnetic
└─ KJBJDI01PK01LP01        Package control panel
```
