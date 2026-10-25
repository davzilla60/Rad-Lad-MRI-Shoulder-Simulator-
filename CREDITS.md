# Credits

## MRI imaging — "MRI / Shoulder / Patient 4"

**Adapted from:** one anonymised MRI study of a left shoulder from the Prometheus library (study description
"RM SPALLA SN"; Esaote 0.25 T system; feet first supine). Series used:

- 3-plane SE scout (TR 100 / TE 16, 7 mm)
- axial TSE T2 (TR 2220 / TE 90) and axial SE T1 (TR 700 / TE 26 — labelled "SE T1 SAG1" in its header, but its
  geometry is axial)
- coronal oblique GE STIR (TR 1820 / TE 25 / TI 85) and SE T1 (TR 600 / TE 26)
- sagittal oblique SE T1 (TR 700 / TE 26)

### Changes made

1. Pixel values were windowed (99.6–99.7th percentile per series) to 8-bit and saved as PNG (scouts) and JPEG (series).
2. The DICOM geometry (ImagePositionPatient, ImageOrientationPatient, PixelSpacing) is kept unchanged in
   `assets/calib.json` and drives all the planning overlays.
3. Ten anatomical landmarks (humeral head, acromion, supraspinatus footprint, greater tuberosity, axillary recess,
   glenoid, biceps groove, subscapularis, infraspinatus, scapular neck) were picked by hand on the real slices and are
   approximate (±5 mm).
4. The radiographer's oblique angles (COR −14.4°, SAG 67.4° in the axial plane) are the grading reference.
5. In the browser: the scout k-space animation is a real Fourier transform of the real scouts; the oblique previews are
   reformats of the acquired axial slices; scans show only the real slices inside the planned stack, cropped to the
   planned FOV. Arm position doesn't change the images (all were acquired in the neutral position).
6. The real axial stack stops about 30 mm above the humeral head centre, so it doesn't reach the AC joint that the
   simulator asks you to cover.
7. The 3-D room shows a generic closed-bore magnet, head first, not the real low-field system.
8. Sequences other than those listed above are for teaching only. There are no images for them.

Educational simulation. It isn't a medical device and isn't for clinical use.
