# Alexandria taxi: livery and plates (Lada VAZ-2107)

Research notes for the CAD and texture work. Photo filenames refer to a local
`references/images/livery/` and `references/images/plates/` (not distributed with this repo).
`references/sources/<folder>/MANIFEST.csv` gives the source URL, author and licence of each image. Most are Wikimedia Commons CC BY / BY-SA, plus some PD and CC0.

Confidence levels: **H** = seen consistently in several clear photos. **M** = seen in 1–2 photos, or with variation between cars. **L** = inferred or from a single weak source.

---

## 1. Livery: panel-by-panel map

The scheme is a **two-tone split on the panel shut lines**. Front wings and rear quarters are black, and the doors, bonnet and boot are yellow. There is no horizontal beltline split on the doors and no checkered band. The black "lower body" in the reference photo is the **sill plus the black wings at either end, together with the black bumpers**. The doors are yellow almost to their bottom edge.

| Panel | Colour | Conf. | Evidence |
|---|---|---|---|
| Bonnet (hood) | Yellow | H | 3-4f_2107_roof-rack_roof-sign_2011, 3-4f_2107_market_2017, top-3-4_2107_corniche-night_2020 |
| Front wings (fenders) | **Black, full height**, including the wheel-arch lip and the area under the headlamp. Rear edge follows the front-door shut line | H | side_2107_full-side-elevation_2006, 3-4f_2107_market_2017, 2011 |
| Front panel / grille surround | Yellow. On many cars the strip between grille and bumper and the **lower valance under the bumper is yellow** | M | 2011 (yellow valance below bumper), 3-4f_2107_two-taxis_petrol_2013 |
| Front and rear doors | **Yellow, full height**, from the window-frame base down to the bottom flange | H | side_2107_full-side-elevation_2006, 2017, 2011, top-3-4 2020 |
| Door rubbing strip (moulding at the lower crease, about 1/3 up the door) | Black rubber/plastic strip with thin chrome trim. This is the only "line" low on the doors, and the paint stays yellow below it | H | side_2107_full-side-elevation_2006, side_2107_roof-rack_door-decals_2014 |
| Sills (rockers) | Black | H | 2006, 2011, relations 2020 |
| Rear quarters (rear wings) incl. C-pillar base | **Black, full height**. Front edge follows the rear-door shut line, and the black wraps around the rear corner to the tail-lamp edge | H | 2006 side, 3-4r_2105_rear-plate_2026, rear_2107_corniche-sea_2017 |
| Roof panel | **Black** | H | relations 2020 (plan), top_taxi_overhead_2020, every side view |
| A-pillars / window frames / B-pillar | **Varies: black on most cars, yellow on some.** The reference car has yellow pillars, as do 3-4f_2107_yellow-pillars_2010 and 3-4f_2107_corniche-qaitbay_2024. Black pillars appear in 2006 side, 2017 and the 2013 petrol-station photo | M | as listed |
| C-pillar (sail panel) | Black (part of the rear quarter) | H | 2006, 2105 rear |
| Boot lid (trunk) | Yellow | H | relations 2020, 3-4r_2105_rear-plate_2026, rear_2107_corniche-sea_2017 |
| Rear tail panel (between the lamps, carries the plate) | Yellow | H | 2105 rear, 2017 rear |
| Bumpers | Factory 2107 bumpers: chrome top bar over black plastic/rubber, so they read as black and chrome. Many cars are painted or replaced in plain black | H | all |
| Mirrors | Black (factory) | H | 2006, 2010 |
| Wheels | Steel, usually silver/grey with or without small hubcaps. Some cars have them painted yellow or black, and some run aftermarket alloys | M | 2006, 2011, Taxi-Alex-001 (yellow wheels), 2010 (alloys) |
| Roof rack | Tubular rack, galvanised silver or painted black/red. Common but not universal | M | 2011, 2014, 2105 rear, context_roof-rack-top_2017 |

**Model split lines:** use the existing door shut lines as the colour boundary, which avoids extra mask geometry. Front-door leading edge: everything ahead of it is black. Rear-door trailing edge: everything behind it is black, except the boot lid and tail panel. Sill: black below the door bottom flange. Roof: black above the drip rail. Pillars should be a parameter (yellow to match the reference photo).

**No checkered band** appears on any Alexandria car (H). The checker belongs to the 2009 white Cairo taxis (compare_cairo_white-new_2009).

### Door lettering and numbers
- Small hand-painted or vinyl **Arabic text in black or dark red-brown, about 3–5 cm character height**. It is placed on the **upper part of each door, just behind or below the door handle**, roughly at handle height (M). Evidence: 2006 side (two-line text on both doors), 2011 (front door), 2017 (rear door).
- The legible examples (2011, 2017) show the **plate number repeated in Arabic letters and numerals**, for example "س ر ٢٧٤٣". The 2006 car has a second short line, probably the word "الإسكندرية" or "أجرة" (L, too small to read).
- There is no large "تاكسي الإسكندرية" fleet title, no phone numbers and no big C-pillar number (H for absence, across about 15 cars).
- Optional personal decals are common: driver or owner name strips across the windscreen top, such as "Yassen" in 3-4f_2107_corniche-qaitbay_2024, door cartoons (Taxi-Alex-004), and ornament swirls (2014). These are not part of the official livery.

### Roof sign
Two types are seen (M):
1. **Small yellow dome or saddle sign** reading **"للأجرة"** ("for hire") in black Arabic script on both faces (3-4f_2107_roof-rack_roof-sign_2011). It sits centred, front of roof, just behind the windscreen header and inside the roof rack. **Estimated size: 25 cm wide × 10–12 cm tall × 12 cm deep.** This estimate is scaled against windscreen width and is ±20 %. The top is rounded and the base is a flat foot. On the reference car it looks yellow-orange. In the model, use translucent yellow plastic with an orange tint, at the sampled hex below.
2. **Rectangular yellow box sign "TAXI"** in black Latin capitals, often with Arabic on the other face (3-4r_2107_taxi-sign_2008). About 30–35 × 10–12 × 12 cm.

Many cars have no roof sign at all.

### Context: other governorates
- **Alexandria:** black and yellow, as above, unchanged from at least 2006 to 2025 (dated photos 2006, 2008, 2010, 2011, 2013–2014, 2017, 2019–2021, 2024–2025). Newer saloons (Hyundai and others) in Alexandria carry the same scheme: yellow upper, bonnet and boot with black lower/wings (context_corniche_modern-taxi_2017) (M).
- **Cairo (old):** a black body with white wings and roof (compare_cairo_black-white_2007). The 2009 replacement programme (Ministry of Finance, launched April 2009) introduced new white taxis with a black-and-white checker band (compare_cairo_white-new_2009). It offered EGP 5,000 scrap value plus a bank loan for cabs 20+ years old, and was aimed mainly at Cairo/Greater Cairo (Daily News Egypt 2009-05-20, ESMAP, Gulf News). A 2013 decree barred licence renewal for taxis over 20 years old. Even so, the Alexandria Lada fleet is still visible in 2024–2025 photos.
- **Beheira (Damanhour):** white with green (compare_damanhour_white-green_2020).
- **Port Said:** not verified. Commons has no clear photo, so this is left out of the comparison.
- Wikipedia's "Taxi livery" article states that liveries vary by governorate, naming Cairo navy/black and white and Alexandria yellow and black.
- **No source was found for a formal governorate decree fixing the Alexandria colours.** The scheme is documented here only from photographs (L for any regulatory claim).

---

## 2. Egyptian licence plate (2008+ format)

| Item | Value | Conf. / source |
|---|---|---|
| Introduced | August 2008, replacing the numeric plates. Pre-2008 taxi plates were orange over the whole plate (front_2106_old-plate) | H, Wikipedia |
| Size | **350 × 170 mm** aluminium, embossed, with a raised border and two rivet/screw holes in the top band | H, Wikipedia. One plate-recognition vendor lists 320 × 170 mm. The photo aspect ratio is about 2.0–2.1, which supports 350 × 170 |
| Layout | **Top band** about 1/3 of the height (~55–58 mm): "EGYPT" in black Latin capitals at the **left**, "مصر" in black Arabic at the **right**. **Main field** (~110 mm): white, split by a thin vertical grey/black divider near the centre. **Numbers on the LEFT** (Eastern Arabic-Indic digits ٠-٩), **letters on the RIGHT** (Arabic, separated by spaces) | H, every plate photo plus diagrams |
| Band colours | **Taxi = orange**. Private = light blue. Trucks/transport = red. Bus/government = grey. Limousine/tourism = beige. Diplomatic = green. Customs/temporary = yellow. Police = dark blue | H, Wikipedia; matches photos |
| Character count | Alexandria: **3 letters + 3–4 digits**. Cairo: 3 letters + 3 digits. Giza: 2 letters + 4 digits | H, Wikipedia |
| Governorate letter | First (rightmost) letter **س = Alexandria**. The reference car's "٨٣٤ س ل م" therefore fits Alexandria. It reads right-to-left as س ل م, with the digits ٨٣٤ in the left box | H |
| Latin transliteration line | Early 2008 plates had small embossed Latin letters and Western digits under the Arabic (plates/photo_private_blue_latin-line*). This was **dropped early**, so most current plates have none | H |
| Fonts | Since 2022: Calibri-like Latin for "EGYPT" and a Square-Kufic-style Arabic. Older plates use a rounded naskh-like embossed Arabic | M, Wikipedia |
| Weathering | The orange band fades toward red-orange or amber/ochre (photo_taxi_red-orange_weathered, photo_taxi_amber_faded). Black paint wears off the embossed characters, and plates collect dents and dirt | H |

**Plate positions on the Lada 2107:**
- **Front:** bolted to the centre of the front bumper below the grille, on the factory plate bracket. The Egyptian plate is taller than the Euro strip the bracket was designed for, so it hangs below the bumper line. On some cars it is offset left or right of centre (2011 right, 2017 left). Model it centred, with the top edge just under the chrome bar.
- **Rear:** centred on the yellow tail panel between the two tail-lamp clusters, above the rear bumper. The 2107 plate-lamp housing sits in the bumper beneath it. Evidence: 3-4r_2105_rear-plate_2026 and rear_2107_corniche-sea_2017.

---

## 3. Recommended colours (sRGB, sampled with PIL)

Sampling method: an HSV mask over panel boxes, taking the median of the 40–60th luminance percentile ("mid") and the 70–90th ("lit"). The most neutral photos, 2006 side and 2010, were used for the base values. Graded or filtered photos were excluded.

| Use | sRGB hex | Notes |
|---|---|---|
| **Taxi yellow, fresh (base colour)** | **#F0C400** | 2006 mid #F1C500, lit #F4DC21. Close to RAL 1023 Traffic Yellow. Warm, slightly orange-leaning lemon |
| Yellow, sun-faded / chalky | #E2C24A | Lower saturation. The 2011 car fades greenish (#BDBC42), and the 2105 fades toward #E2B742 |
| Yellow, shadow side (sanity check only) | #C9A000 | |
| **Gloss black** | **#0C0D0E** | 2006/2011/2017 mid #050507–#0B0D0C |
| Black, faded / oxidised (quarters, sills) | #2A2B2D | Chalky grey-black, visible in the 2105 rear and 2014 photos |
| **Plate band orange** | **#F47725** | Diagram value. Clean real plate: #FE8244. Weathered: #D4332B (red-orange) to #885817 (amber) |
| Plate field white | #F2F2EE | Off-white aluminium |
| Plate characters / border | #111111 | |
| Private-plate blue (reference only) | #0377B4 | |
| Roof sign | #F5C000 body, characters #111111 | Translucent yellow-orange plastic |
| Chrome (bumper bar, trim) | #C8CCD0 base, metallic | Pitted, see below |

---

## 4. Weathering cues (seen in photos)

- **Faded yellow**, especially on the bonnet and roof-adjacent surfaces. Faded panels go paler and slightly greenish or chalky. Repainted panels can mismatch, with a brighter yellow on one door (Taxi-Alex-001).
- **Black paint chalking/oxidising** to a grey-black on the rear quarters and sills. Brush-painted black shows streaks.
- **Rust:** bubbling along the sills, rear wheel-arch lips, door bottoms and around the tail-lamp corners. There are also rust trails from the rack feet and drip rails.
- **Dents and scrapes** on the front wings, bumper corners and rear quarters. Misaligned bumpers (Taxi-Alex-001, 2105 rear).
- **Chrome pitting and dulling** on the bumper bars, grille and window trim. The chrome bumper strip is sometimes missing.
- **Steel wheels** are dusty and grey. Hubcaps are often missing, and some wheels are hand-painted yellow.
- **Stickers and decals:** name strips on the windscreen, cartoons and religious stickers, and a fuel-type sticker on the front wing (2010).
- **Plates** are dented, with the band faded orange to red/amber and dirt in the embossing.

---

## Sources
- Wikipedia, *Vehicle registration plates of Egypt*: https://en.wikipedia.org/wiki/Vehicle_registration_plates_of_Egypt (size, band colours, letter codes, fonts, transliteration)
- Wikipedia, *Taxi livery*: https://en.wikipedia.org/wiki/Taxi_livery (liveries by governorate)
- Daily News Egypt, "New taxis gain speed on Cairo's streets" (2009-05-20): https://www.dailynewsegypt.com/2009/05/20/new-taxis-gain-speed-on-cairos-streets/
- ESMAP, Egypt taxi scrapping programme: https://esmap.org/node/659
- Gulf News, "Egypt's taxis modernised": https://gulfnews.com/amp/story/business%2Fegypts-taxis-modernised-1.828436
- Ahram Online, 20-year taxi licence decree: https://english.ahram.org.eg/News/88286.aspx
- Wikimedia Commons categories *Taxis in Alexandria*, *Taxis in Cairo*, *Taxis in Damanhour*, *License plates of Egypt* (images, see MANIFEST.csv files)
