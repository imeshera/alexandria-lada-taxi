#!/bin/zsh
# Regenerates the Lada taxi lettering SVGs (mm units) in svg/ with CoreText (text2svg.swift, macOS).
# Usage: ./make_svgs.sh <path-to-compiled-text2svg>   (swiftc -O text2svg.swift -o text2svg)
# _R = unflipped, _L = mirrored (for faces whose sketch +x is the viewer's left).
set -e
T=${1:-./text2svg}
cd "$(dirname "$0")"
PL_DIG="٨٣٤"            # plate digits (reference photo)
PL_LET="س ل م"          # plate letters; first (rightmost) letter س = Alexandria
for flip in 0 1; do
  s=$([ $flip = 0 ] && echo R || echo L)
  $T svg/plate_egypt_$s.svg  "Helvetica-Bold" 60 $flip "EGYPT"
  $T svg/plate_misr_$s.svg   "GeezaPro-Bold"  60 $flip "مصر"
  $T svg/plate_dig_$s.svg    "GeezaPro-Bold"  100 $flip "$PL_DIG"
  $T svg/plate_let_$s.svg    "GeezaPro-Bold"  100 $flip "$PL_LET"
  $T svg/door_plate_$s.svg   "GeezaPro-Bold"  60 $flip "$PL_LET  $PL_DIG"
  $T svg/door_city_$s.svg    "GeezaPro-Bold"  60 $flip "تاكسي الإسكندرية"
  $T svg/sign_ujra_$s.svg    "GeezaPro-Bold"  60 $flip "للأجرة"
  $T svg/sign_taxi_$s.svg    "Helvetica-Bold" 60 $flip "TAXI"
done
