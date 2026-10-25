# MR-I Ready — MRI Shoulder

An embeddable, single-file teaching simulator for the Rad-Lad website. It uses the same engine and layout as the
MR-I Ready elbow simulator, but every image comes from **one real, anonymised left-shoulder MRI** and is shown with its
true scanner geometry. **It's a demonstration only.**

Marker: **Shoulder the Burden** — axial first, both obliques angled to the supraspinatus, key anatomy covered, and the
arm in the standard position.

## Flow

1. **Patient set-up.** The patient lies supine, head first, slid toward the right of the table so the left shoulder is
   near isocentre, with a dedicated shoulder coil on. Choose how the left arm lies (the 3-D room changes pose):
   - by the side, **thumb up** (neutral / slight external rotation) — the standard position;
   - hand on the abdomen (internal rotation) — foreshortens the supraspinatus tendon;
   - ABER (hand behind the head) — an MR-arthrogram add-on, not the routine set-up.
2. **Scout.** The real 3-plane spin-echo scout is "acquired" line by line: each image is rebuilt from its own k-space
   with an inverse FFT as the phase-encode lines fill.
3. **Axial first.** The coronal and sagittal obliques are locked until the axial has been scanned.
4. **Drag the axial in.** Completed series sit in a tray in the rail. Drag (or tap) the axial onto the **AXIAL** panel;
   only then does the rotate handle ⟳ appear for the obliques. Scroll the panel (wheel or ▲ ▼) to the slice where the
   supraspinatus tendon runs out to the greater tuberosity.
5. **Angle the obliques on the axial.**
   - **Coronal oblique:** slices **parallel** to the supraspinatus tendon.
   - **Sagittal oblique:** slices **perpendicular** to it.
   - The angle is graded against the radiographer's own planes in the DICOM (COR −14.4°, SAG perpendicular to the COR
     reference, ±10°). SCAN stays locked until the angle is right.
   - The preview panel reformats the planned centre slice from the axial slices you actually acquired, so you can see
     the tendon line up as you rotate.
6. **Scan → images.** Each scan shows only the real slices that fall inside your stack, cropped to your FOV.
7. **Debrief.** Coverage and angle for each plane, the position note, hero images (the axial shows your planes and the
   radiographer's dashed), a sequences-to-consider table, and the marker.

Boxes are projected onto each panel using its real IPP / IOP, so they line up on the scouts, the axial series and the
double-oblique coronal alike. Drag the box to move it, drag its edges to change coverage or FOV, or use the steppers /
CLI (`slices`, `thick`, `gap`, `fov`, `angle`, `use <series>`, `restore <plane>`, `help`).

## Files

- `shoulder.embed.html` is the self-contained deliverable (~2.1 MB, every image inlined). `index.html` is an
  identical copy for one-drop hosting.
- `shoulder.html` is the source. It loads `./assets/`, `assets/calib.js` and `room3d.js`. Run `python inline.py` to
  rebuild both deliverables.
- `room3d.js` is the procedural three.js MRI room (three.js from jsDelivr): magnet, three arm poses and the shoulder
  coil. Not mirrored (the scanned left arm faces the camera). If you change it, bump `?v=N` in `shoulder.html` **and**
  `inline.py` together.
- `assets/` holds the real scouts (`loc_ax/cor/sag.png`), the series slices (`ax_t2`, `ax_t1`, `cor_t1`, `cor_stir`,
  `sag_t1`), `calib.json` / `calib.js` (true geometry of every image + hand-picked landmarks) and the logos.
- `tools/gen_assets.py <study folder>` rebuilds `assets/` from the DICOM study.

Debug hooks: `window.__mrs` (`parse(cmd)`, `gotoPlan(q)`, `useSeries(id)`, `setAngle(q, deg)`, `angErr(q)`,
`autoPlan()`, `analyse(q)`, `planOK(q)`, `S()`) and `window.__room()` (`setPose`, `cam`, `snap`).
