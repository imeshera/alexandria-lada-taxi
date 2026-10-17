# VAZ-2107 (Lada 2107 / Riva / Nova saloon): modelling reference

Research compiled 2026-10-17 for the 1:1 CAD model of the Alexandria black-and-yellow Lada taxi.
The Alexandria taxis are mostly **Egyptian-assembled 2107s** (Alamal Group / Suzuki Egypt plant in Cairo, about 2002–2015). That makes the **late-spec car** the primary target:
- black or chrome tall grille
- plastic bumpers with black caps
- 4-spoke "LADA" steering wheel
- grey cloth seats

Early-spec details are noted wherever they differ.

Confidence ratings:
- **HIGH**: factory dimensioned drawing, or two or more independent sources agree.
- **MED**: one reputable source.
- **LOW**: measured for this project from a drawing or photo, or the sources conflict.

---

## 1. Principal dimensions

| Item | Value | Source | Confidence |
|---|---|---|---|
| Overall length | **4145 mm** | Factory drawing (`drawings/vaz-2107_factory-4view-dimensioned_…png`, `…manual-3view…jpg`); ru.wikipedia ВАЗ-2107; en.wikipedia Lada Riva; auto.ru | HIGH |
| Front overhang (bumper face to front axle) | **664 mm** | Factory drawing | HIGH |
| Wheelbase | **2424 mm** | Factory drawing; ru/en Wikipedia | HIGH |
| Rear overhang (rear axle to bumper face) | **1057 mm** | Factory drawing (664 + 2424 + 1057 = 4145) | HIGH |
| Overall width (body) | **1620 mm** | Factory drawing; auto.ru; en.wikipedia. ru.wikipedia says 1611 (outlier) | HIGH |
| Width over door mirrors | **1680 mm** | Factory drawing (rear view) | HIGH |
| Overall height (unladen) | **1446 mm** | Factory drawing; auto.ru; autospot.ru. ru.wikipedia gives 1440 and en.wikipedia gives 1435 (likely laden or a different reference) | HIGH for 1446 |
| Front track | **1365 mm** | Factory drawing (front view) | HIGH. ru.wikipedia gives 1349, probably a different wheel offset or era |
| Rear track | **1321 mm** | Factory drawing (rear view) | HIGH. ru.wikipedia gives 1305 |
| Ground clearance | **170 mm** (laden, to the lowest point, which is the rear axle housing) | auto.ru catalogue; ru.wikipedia gives 175 | MED |
| Kerb weight | **1030 kg** carburettor (2107/21074); **1060 kg** injection (21074i/2107i) | ru.wikipedia; auto.ru gives 1060 | MED |
| Gross vehicle weight | 1430 kg carburettor / 1460 kg injection | ru.wikipedia | MED |
| Doors / seats | 4-door saloon, 5 seats | all | HIGH |
| Fuel tank | 39 L, vertical tank behind the rear seat back on the right side of the boot | ru.wikipedia; cutaway image | MED |
| Tyres | **175/70 R13** (575 mm Ø nominal) or **165/80 R13** (594 mm Ø). Both are factory fitments, varying by version and year | auto.ru wheel-size catalogue; fb.ru; tirewheelguide.com | HIGH |
| Rim | **5J × 13, ET29**, steel, 4 bolts | auto.ru; fb.ru | HIGH |
| PCD / fixings | **4 × 98**, M12×1.25 wheel bolts (not studs); centre bore **58.5 mm** (often quoted as 58.6) | auto.ru; fb.ru | HIGH (PCD) / MED (CB) |
| Production | Togliatti 03-1982 to 04-2012; Izhevsk/Ukraine; **Egypt to about 2015** | ru/en Wikipedia | HIGH |

Sources:
- https://ru.wikipedia.org/wiki/ВАЗ-2107
- https://en.wikipedia.org/wiki/Lada_Riva
- https://auto.ru/catalog/cars/vaz/2107/2307270/2307271/specifications/
- https://auto.ru/catalog/cars/vaz/2107/specifications/razmer-koles/
- https://autospot.ru/brands/vaz/2647/technical-parameters/
- https://fb.ru/article/524720/2023-vaz-razmer-kolesa---harakteristiki-i-opisanie
- https://tirewheelguide.com/sizes/vaz/2107/2011/
- https://drawingdatabase.com/lada-2107/
- https://carblueprints.info/eng/prints/lada/lada-2107-1982

The tyre diameter in the table is nominal: 175/70R13 gives 330.2 + 2 × 122.5 = 575 mm, and 165/80R13 gives 594 mm. For the model, use **Ø ≈ 580 mm**, which fits the drawing's static ground line.

### Heights and lengths measured from the factory side view (LOW–MED)
Measured on `vaz-2107_factory-4view-dimensioned_carblueprints_1109x717.png`, side view:
- Vertical scale ≈ 6.89 mm/px: roof at y = 75, ground at y = 285, 1446 mm.
- Horizontal scale ≈ 6.73 mm/px: bumper faces at x = 85 and x = 701, 4145 mm.

Expect ±15–25 mm error on each value.

| Feature | Approx. value |
|---|---|
| Roof top | 1446 mm (reference) |
| Windscreen top / drip rail | ≈ 1360 mm |
| **Beltline** (side-glass bottom, front door) | **≈ 920–950 mm** |
| Windscreen base / scuttle | ≈ 1000 mm, about 1010 mm aft of the front bumper face |
| Bonnet front edge / top of headlamp surround | ≈ 850 mm |
| Front-wing top at front axle | ≈ 940 mm |
| Door handle (pull-type, horizontal) | ≈ 790 mm |
| Side moulding / rubbing strip | ≈ 450 mm |
| **Sill bottom** (black sill trim) | **≈ 250 mm** (black band ≈ 310–250 mm) |
| Front wheel-arch top | ≈ 640 mm |
| Rear bumper | ≈ 360–490 mm (top ≈ 490) |
| Boot-lid rear edge (top of tail-lamp panel) | ≈ 780–800 mm |
| Bonnet length (plan) | ≈ 910 mm. Front edge to scuttle ≈ 1010 mm |
| Boot lid length (plan) | ≈ 740 mm, rear-window base to tail panel |
| Cabin widths (top view of the-blueprints 83611 drawing) | **1200 mm** and **1400 mm** annotations, probably rear-cushion width and elbow width |

### Windscreen, lamps, grille and bumpers
- **Windscreen:** no catalogue dimension was found for the glass. It is the same glass as the 2105/2104, a laminated flat-curved screen. Take it from the drawing: it spans about 1250 mm across the A-pillars at the base. Its slope runs from roughly scuttle 1000 mm to header 1360 mm over about 700 mm of plan length (LOW).
- **Headlamps:** large rectangular units, one per side. The amber indicator sits as a separate unit **below the headlamp in the bumper** on export cars, and at the outer end of the headlamp unit on Soviet-market cars. From the front-view drawing each unit is about 300 × 120 mm, and the grille is about 470 mm wide × 145 mm tall (LOW, scaled).
- **Grille:** tall, upright, with a raised and peaked bonnet centre that "follows" the grille.
  - Early cars: chrome grille with closely spaced vertical bars and the VAZ boat badge.
  - Late cars: black grille with a chrome surround.
- **Bumpers:** plastic (first Soviet car with plastic bumpers).
  - Early cars: a chrome top strip.
  - Late cars: all black, with separate black end caps wrapping onto the wings.
  - A plate recess is in the rear bumper.
- **Tail lamps:** horizontal two-tier units.
  - Upper tier: red stop/tail.
  - Lower tier: amber indicator and white reverse.
  - The 2105's vertical stop-lamp segments were dropped.
  - The rear panel between the lamps carries the plate recess.
- **Other body cues:**
  - C-pillar extraction vent: a louvred trim on the rear pillar.
  - Side repeater on the front wing.
  - Black sill strip.
  - Bright window surrounds on early cars, black on late.
  - Door mirrors: a single round-cornered mirror on the driver side, or both sides on late cars.

---

## 2. 2105 vs 2107: what to model differently

| Area | 2105 | 2107 |
|---|---|---|
| Grille | low, flat, black | **tall chrome (late: black) grille**, with a bonnet raised in the centre to suit it |
| Headlamps | rectangular | rectangular, larger units; indicator separate |
| Bumpers | aluminium with rubber | **plastic bumpers with chrome strip (early) or black (late), wrap-around end caps** |
| Tail lamps | with vertical stop segments | **two-tier horizontal, no vertical segments** |
| Front seats | separate headrests | **anatomic seats with integrated headrests** |
| Dashboard | low panel, no rev counter | **tall panel with separate instrument binnacle (tachometer + speedometer to 180 km/h) and full centre console; 4 face vents** (side vents use outside air) |
| Headliner | perforated vinyl, with dome lamps on the B-pillars | **moulded headliner with central roof lamp**; no B-pillar lamps |
| Steering wheel | 2-spoke | **early/1980s cars: 2-spoke with VAZ boat badge (confirmed in zr.ru photos). Late (2000s): 4-spoke wheel with a concave "LADA" hub** |
| Gauges | — | econometer replaced the oil-pressure gauge from 1988 |
| Glovebox badge | "Жигули" | "LADA" |

**Taxi recommendation:** model the late interior, because Egypt-assembled taxis are 2002–2015 cars:
- 4-spoke LADA wheel
- black dash
- grey or black cloth seats

Check this against Alexandria taxi photos. Many taxis have aftermarket seat covers and wheel covers.

---

## 3. Interior description for modelling

- **Dashboard:** a one-piece moulded black upper panel, tall and with a flat top.
  - **Driver binnacle:** a rectangular hooded pod, about 400 mm wide.
    - Left: tachometer, round, about 100 mm.
    - Between the dials: a vertical column of warning lamps.
    - Right: speedometer, round, 0–180 km/h with odometer.
    - Flanking pairs of small round gauges: fuel, coolant temperature, econometer/vacuum and voltmeter (or oil pressure on early cars).
  - **Vents:** two rectangular louvred face vents at the outer ends, and two central vents above the console (top of the centre stack).
  - **Centre console:** runs down to the transmission tunnel and holds:
    - analogue clock (round)
    - rocker switches
    - heater slide controls
    - radio slot
    - ashtray
  - **Passenger side:** glovebox, flush lid with key lock and "LADA" script.
  - **Stalks:** indicator/lights and wiper stalks on the column. Ignition on the right of the column.
- **Steering wheel:** about 380–390 mm Ø (LOW).
  - Early: 2-spoke wheel, spokes dropping to the lower third, and a large flat-rectangular hub with the VAZ boat badge.
  - Late: 4-spoke wheel with a round concave hub and LADA badge.
- **Gear lever and pedals:**
  - Gear lever: long floor lever with a rubber boot and round knob; 4- or 5-speed.
  - Handbrake: lever between the seats.
  - Pedals: three pendant pedals with rectangular rubber pads.
  - Floor: ribbed rubber mats, with carpet on the tunnel.
- **Front seats:** separate buckets with **integrated headrests** (one-piece tall backrest with an opening/recess at the top), moderate side bolsters, and reclining. Upholstery:
  - Early export cars: velour, often red, brown or blue.
  - Late cars: grey or black patterned cloth.
- **Rear seat:** flat 3-seat bench with a fold-down centre armrest (higher trims). The backrest is fixed, with the fuel tank behind it.
- **Door cards:**
  - Upholstered panel with horizontal pleated or welded seams.
  - Separate pull handle / armrest bar: chrome-trimmed on early cars, black on late.
  - Small chrome interior opener lever and window winder crank.
  - Lock buttons at the top rear of the door, by the window.
  - Map pocket at the bottom of the front doors on some versions.
- **Headliner:** moulded fibreboard and cloth, with a central rectangular dome lamp. Sun visors are vinyl.
- **Colours:**
  - Late cars: black plastics with grey cloth.
  - Early cars: black plastics with red, brown or blue velour.

---

## 4. Blueprints (downloaded to `references/images/drawings/`)

| File | Source | Author / licence | Pixels | Views | Dimension scale? |
|---|---|---|---|---|---|
| `vaz-2107_factory-4view-dimensioned_carblueprints_1109x717.png` | https://carblueprints.info/eng/prints/lada/lada-2107-1982 | AvtoVAZ factory/owner-manual drawing; licence unknown (reference only) | 1109×717 | side, front, rear, top | **Yes**: 4145/664/2424/1057, 1446, 1620, 1680, 1365/1321. **Primary canvas** |
| `vaz-2107_manual-3view-dimensioned-shaded_drawingdatabase_930x880.jpg` | https://drawingdatabase.com/lada-2107/ (identical on carblueprints vaz-2107-2) | Repair-manual illustration; licence unknown | 930×880 | side, front, rear (shaded) | **Yes**: same numbers |
| `lada-2107_4view_the-blueprints-26796_1045x571.gif` | https://the-blueprints.com/blueprints/cars/lada/26796/view/lada_2107_2008 | uploader Dr Dan Saranga; site terms, personal use | 1045×571 | side (passenger side), front, rear, top | No |
| `lada-vaz-2107_side-top-interior-widths_the-blueprints-83611_923x701.png` | https://the-blueprints.com/blueprints/cars/lada/83611/view/lada_vaz-2107_zhiguli | uploader Dr Dan Saranga; personal use | 923×701 | side, top | Interior widths only (1200/1400) |
| `vaz-2107-riva_front-side_carblueprints_1055x269.gif` | https://carblueprints.info/eng/prints/lada/lada-vaz-2107-riva | brochure art; unknown | 1055×269 | front, side | No |

Not downloaded: getoutlines.com sells "1982 Lada 2107 Sedan" vectors (AI/DWG/DXF, about US$23). It is the only vector option if higher precision is ever needed: https://getoutlines.com/vector-drawings/15702/1982-lada-2107-drawings. No 2107 entries were found on smcars.net or outlines.ru.

**Recommended canvas setup:**
1. Use the factory 4-view. Place the side view so the front axle is at x = 0. The front bumper is then at −664 and the rear bumper at +3481.
2. Calibrate horizontal and vertical scale separately; there is about 2% anisotropy in the scan.
3. Cross-check against the shaded manual drawing, and against the near-orthographic photo `exterior/side_green_moscow-2025.jpg` (CC0).

---

## 5. Free 3D / CAD models (metadata only; nothing downloaded)

All are Sketchfab models. Check each page before use. CC-BY requires attribution, and none is engineering-accurate.

| Model | Author | Licence | Downloadable | Faces | URL | Note |
|---|---|---|---|---|---|---|
| **Vaz 2107 scan** | rsc.jes | Sketchfab Free Standard | yes | 717k | https://sketchfab.com/3d-models/0c67b0f1a4ce4628a6010171038ee86f | **Photogrammetry scan (2025)**. Potentially the best dimensional cross-check of the real body |
| VAZ-2107 Car Wreck | Abandoned Scans | Editorial | no | 550k | https://sketchfab.com/3d-models/3af1a5ea9d594dc0b78708607a8c59e7 | scan; viewer only |
| Lada 2107 | Elchinbek Qodirov | CC BY | yes | 215k | https://sketchfab.com/3d-models/b201429d07084738a83bb69748d3434d | tuned version, C4D |
| LADA 2107 | tiunov.se | CC BY | yes | 105k | https://sketchfab.com/3d-models/31201f80892b404a8e49c272490a664c | |
| Lada_2107 | Lisecot | CC BY | yes | 107k | https://sketchfab.com/3d-models/8b3916563b6743d5bb8271584a789cc9 | |
| Lada 2107 | Aslan | CC BY | yes | 107k | https://sketchfab.com/3d-models/55bd23c141284e758e4eacc01df14037 | |
| Lada 2107 (Variation) | OWRING | CC BY | yes | 57k | https://sketchfab.com/3d-models/71066ccf169a484cb39c7d8362dc9e89 | |
| Vaz 2107 | zairiq zairiq | CC BY | yes | 64k | https://sketchfab.com/3d-models/8ed2d32933864613be555e1c4f7a0d9a | |
| VAZ 2107 | Alex | CC BY | yes | 42k | https://sketchfab.com/3d-models/c408bafeadd94e10bbd984a45d86d5d5 | |
| Lada 2107 | davidmarton1987 | CC BY | yes | 41k | https://sketchfab.com/3d-models/dbe677c06c72447b93a053348f46c4da | |
| Old Car – VAZ 2107 | Arkady Gribachev | CC BY | yes | 20k | https://sketchfab.com/3d-models/91270dab9d1a47c7ba7ffaaf8c8b0beb | popular, about 18.6k downloads |
| Lada Riva | 87-Motors | CC BY | yes | 94k | https://sketchfab.com/3d-models/351a10ee679f4142aff3b370df922846 | |
| **LADA Taxi** | abbmo | CC BY | yes | 6.6k | https://sketchfab.com/3d-models/e75073fa0888469b89cb5c9bae48a4ba | **Low-poly Alexandria Lada taxi**; livery reference |
| Lada Zhiguli (Riva) | rtrule | CC BY-NC | yes | 153k | https://sketchfab.com/3d-models/1058625a0f8940c9871e3f252140422e | non-commercial |
| 1995 Lada/VAZ 2107 | Renafox | CC BY-NC | yes | 2k | https://sketchfab.com/3d-models/c94daeb210b244729d634975c9ed0c5b | low-poly |
| VAZ 2107 | ICantModel123 | CC BY-SA | yes | 7.8k | https://sketchfab.com/3d-models/62af1ba8df884766bac86cf3353a2764 | |
| VAZ Zhiguli 2105 | Nieve5677 | CC BY | yes | 808k | https://sketchfab.com/3d-models/bfc82572ac3a4653807b7753cba135a3 | sister car, high detail; shares the body shell aft of the A-pillar |
| Lada 2107 / Lada 2107 Police | codexito | Standard (paid) | no | 26k | https://sketchfab.com/3d-models/49c2aedd5c974323bec7d39eead8580d | |

Paid or editorial models elsewhere:
- TurboSquid 625042 / 584176 (editorial)
- RenderHub "Vaz Lada 2107 1982" (editorial)
- CGTrader
- Unity Asset Store "PBR Classic Car VAZ 2107" (US$4.99)

GrabCAD returned nothing because its API was blocked from here and web search found no hits. No Printables or Thingiverse 2107 models turned up in web search.

---

## 6. Photo sets
- `exterior/`: 36 images. 29 are from Wikimedia Commons with known CC0, PD or CC-BY(-SA) licences, including 3 Alexandria taxis. 7 are Za Rulem press or editorial photos, reference only. See `MANIFEST.csv`.
- `interior/`: 17 images. Wikimedia Commons has **no** standard VAZ-2107 interior photos. Checked:
  - the VAZ-2107 and related categories
  - multilingual searches
  - Openverse
  - Flickr, which is blocked from this network
  - Unsplash, which had only a Samara

  So 15 interior images come from zr.ru (© Za Rulem, private reference only, do not redistribute). They cover:
  - early 2-spoke and late 4-spoke dashboards
  - the instrument cluster
  - the centre console
  - front and rear seats
  - door cards
  - the headliner and dome lamp
  - pedals and gear lever

  2 are public-domain Commons images: a roof-cut convertible showing the cabin from above, and a car with all doors open.

Gaps:
- No close-ups of door handles or mirrors were found on Commons; zoom into the 2592–3000 px Kraków and press shots instead.
- No exact windscreen glass dimensions were found.
- No rear-seat or headliner dimensions were found.
