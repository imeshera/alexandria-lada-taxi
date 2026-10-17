# Alexandria Lada taxi (VAZ-2107): dimension sheet

This is the sheet the Fusion parameters are built from. Every value below is a user parameter in the
**Alexandria Lada Taxi** document, with the same source and confidence in its comment.
Detailed research is in [`vaz2107-specs.md`](vaz2107-specs.md) (car) and [`livery-and-plates.md`](livery-and-plates.md)
(livery, roof sign, plates).

**Frame:** X runs from the front bumper face rearwards, Y is up from the ground, Z is lateral (+Z = the car's right).
**Confidence:**
- **HIGH**: factory data, or two independent sources agree.
- **MED**: read off the factory dimensioned drawing (±15–25 mm) or a calibrated photo.
- **LOW**: estimated, or the sources conflict.

## Sources
| Tag | Source |
|---|---|
| FAC | AvtoVAZ factory dimensioned 4-view (owner/repair manual). `images/drawings/vaz-2107_factory-4view-dimensioned_carblueprints_1109x717.png`. Side view 6.73 mm/px horizontal, 6.89 mm/px vertical; bumper face at x = 84 px, ground at y = 285 px. Licence unknown, reference only |
| SPEC | ru/en Wikipedia ВАЗ-2107 / Lada Riva, auto.ru catalogue, autospot.ru (see vaz2107-specs.md) |
| P06 | `images/livery/side_2107_full-side-elevation_2006.jpg` (Commons): near-orthographic Alexandria taxi, wheelbase-scaled 2.646 mm/px. Lengths are good to ~2 %. The camera sits above the car, so heights read 5–8 % high; used for lengths only |
| LIV | ~15 dated Alexandria taxi photos (images/livery, MANIFEST.csv) |
| PL | Wikipedia "Vehicle registration plates of Egypt" + plate photos (images/plates) |

## Principal dimensions
| Parameter | Value (mm) | Source | Conf. |
|---|---|---|---|
| len_overall | 4145 | FAC, SPEC | HIGH |
| axle_f_x (front overhang) | 664 | FAC | HIGH |
| wheelbase | 2424 | FAC, SPEC | HIGH |
| rear overhang | 1057 (derived) | FAC | HIGH |
| width_body | 1620 (1680 over mirrors) | FAC, SPEC | HIGH |
| roof_h | 1446 unladen | FAC, auto.ru (ru.wiki 1440, en.wiki 1435) | HIGH |
| track_f / track_r | 1365 / 1321 | FAC (ru.wiki 1349/1305) | HIGH |
| ground clearance | 170 | auto.ru | MED |
| tyres | 175/70 R13 (Ø 575); alt. 165/80 R13 (Ø 594) | SPEC | HIGH |
| rim | 5J×13 ET29, 4×98, CB 58.5 | SPEC | HIGH |
| wheel_cy | 287 (static radius) | derived | MED |

## Side-profile stations (x from the front bumper face)
| Parameter | Value | Source | Conf. |
|---|---|---|---|
| body_front_x | 60 | P06 | MED |
| ws_base_x | 1080 | FAC centreline ~1000, P06 A-pillar foot ~1200. Flat-glass compromise | LOW |
| ws_top_x | 1420 | FAC (P06 1440) | MED |
| door_f_x0 | 1184 | FAC (P06 1148) | MED |
| b_pillar_x | 2120 | FAC (P06 2080) | MED |
| door_r_x1 | 3001 | FAC (P06 2948) | MED |
| rdw_x1 (rear door glass end) | 2890 | FAC + P06 | MED |
| rs_top_x | 3015 | FAC (P06 3010) | MED |
| rs_base_x | 3338 | FAC (P06 3300) | MED |
| body_rear_x | 4100 | FAC | MED |

## Heights
| Parameter | Value | Source | Conf. |
|---|---|---|---|
| bonnet_front_h | 830 | FAC 812–850 | MED |
| cowl_h (scuttle) | 985 | FAC | MED |
| belt_h (side-glass base) | 947 | FAC 920–950 | MED |
| deck_h / rear_top_h | 950 / 792 | FAC | MED |
| sill_h | 300 | FAC (black sill band ~250–310) | MED |
| door_bot_h | 370 | FAC | MED |
| handle_y | 805 | FAC 790–826 | MED |
| rub_y (rubbing strip) | 462 | FAC ~450, P06 | MED |
| front bumper | 380–510 | FAC | MED |
| rear bumper | 360–490 | FAC | MED |
| headlamps | 575–715, \|z\| 275–645 | FAC front view | MED |
| grille | 535–805, half width 255 | FAC front view (~470 wide) | MED |
| tail lamps | 585–770 | FAC rear view | MED |
| roof_crown | 25 | estimate | LOW |
| belt_hw / roof_hw (tumblehome) | 765 / 655 | photos; FAC front view | LOW |

## Livery (LIV)
The two-tone split follows the **panel shut lines**:
- **Black:** front wings, rear quarters including the C-pillars, sills and roof.
- **Yellow:** doors, bonnet, boot lid, tail panel and front valance.
- **Varies by car:** pillars and door frames are black on most cars and yellow on the reference car. The model uses parameter `pillars_yellow` (1 = yellow).
- **Lettering and fittings:** the plate number is repeated in small Arabic on the doors, and the car carries a tubular roof rack and a small yellow roof light. Details are in livery-and-plates.md.

## Plate (PL)
- **Size:** 350 × 170 mm.
- **Top band:** orange (taxi), with "EGYPT" on the left and "مصر" on the right.
- **Main field:** digits on the left, letters on the right. The plate reads "٨٣٤ س ل م"; its first letter, س, codes Alexandria.

## Underlays (Fusion canvases, component "Underlays")
| Canvas | File (images/derived) | Plane | Calibration |
|---|---|---|---|
| Factory side view | factory_side_iso.png: FAC side view, crop (40,40)–(720,300), heights ×1.02318 (isotropic), ×2 | z = −1500 | 3.365 mm/px, origin px (88, 501.4) |
| Side photo 2006 | side2006_flipped.jpg (P06 mirrored) | z = −1600 | 2.646 mm/px, origin px (177.1, 946) |

## Biggest open uncertainties
1. **Windscreen base and A-pillar.** The real screen is curved and wraps round. The model uses one flat plane between the drawing's centreline base (~1000) and the pillar foot (~1200).
2. **Tumblehome and plan-view corner radii.** These come from photos only; the factory front and rear views are low resolution.
3. **Interior package** (seat H-points, dash depth, wheel position). This is estimated from interior photos; no dimensioned interior drawing was found.
4. **Exhaust exit side, fuel-filler position and rack geometry.** These vary between taxis.
