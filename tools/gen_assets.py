"""Build ../assets from the shoulder MRI study (Prometheus "MRI/Shoulder/Patient 4").

    python -I tools/gen_assets.py "D:/Prometheus/MRI/Shoulder/Patient 4/48213468_20020101"

Writes loc_ax/cor/sag.png (the real 3-plane scout), <series>_NN.jpg slices, and calib.json / calib.js holding the
true DICOM geometry (IPP / IOP / pixel spacing) of every image plus the hand-picked anatomical landmarks.
All coordinates are DICOM patient (LPS) millimetres.
"""
import sys, os, json
import numpy as np, pydicom, cv2

ROOT = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

base = os.path.join(ROOT, "48213468", "DICOM")
for _ in range(2):
    base = os.path.join(base, [x for x in os.listdir(base) if not x.startswith(".")][0])

def series(pref):
    sd = os.path.join(base, [x for x in os.listdir(base) if x.startswith(pref)][0])
    ds = [pydicom.dcmread(os.path.join(sd, f)) for f in os.listdir(sd) if not f.startswith(".")]
    return sorted(ds, key=lambda d: int(d.InstanceNumber))

def to8(a, hi):
    return np.clip(a.astype(np.float32) / hi * 255, 0, 255).astype(np.uint8)

def geo(d):
    iop = [round(float(x), 5) for x in d.ImageOrientationPatient]
    return {"ipp": [round(float(x), 3) for x in d.ImagePositionPatient], "row": iop[:3], "col": iop[3:],
            "ps": round(float(d.PixelSpacing[0]), 6), "cols": int(d.Columns), "rows": int(d.Rows)}

calib = {"loc": {"n": 256}, "ser": {}}

# ---- scout: instance 1 axial, 2 sagittal, 3 coronal ----
for d, p in zip(series("Series 001"), ("ax", "sag", "cor")):
    a = d.pixel_array
    cv2.imwrite(os.path.join(OUT, "loc_" + p + ".png"), to8(a, np.percentile(a, 99.6)))
    calib["loc"][p] = geo(d)

# ---- diagnostic series ----
# (prefix, id, plane, label, params, est. seconds per acquisition, max slices per TR)
SERIES = [
    ("Series 002", "ax_t2",    "ax",  "TSE T2",  "TR 2220 · TE 90",          250, 30),
    ("Series 004", "ax_t1",    "ax",  "SE T1",   "TR 700 · TE 26",           190, 14),
    ("Series 006", "cor_t1",   "cor", "SE T1",   "TR 600 · TE 26",           170, 12),
    ("Series 005", "cor_stir", "cor", "GE STIR", "TR 1820 · TE 25 · TI 85",  280, 16),
    ("Series 003", "sag_t1",   "sag", "SE T1",   "TR 700 · TE 26",           190, 14),
]
for pref, sid, plane, label, params, secs, maxsl in SERIES:
    ds = series(pref)
    hi = np.percentile(np.stack([d.pixel_array for d in ds]), 99.7)
    for k, d in enumerate(ds):
        cv2.imwrite(os.path.join(OUT, "%s_%02d.jpg" % (sid, k)), to8(d.pixel_array, hi), [cv2.IMWRITE_JPEG_QUALITY, 88])
    g = geo(ds[0])
    ipps = [[round(float(x), 3) for x in d.ImagePositionPatient] for d in ds]
    step = np.subtract(ipps[1], ipps[0])
    g.update({"plane": plane, "seq": label, "params": params, "n": len(ds), "ipp": ipps,
              "nrm": [round(float(x), 5) for x in step / np.linalg.norm(step)], "sp": round(float(np.linalg.norm(step)), 3),
              "thk": float(ds[0].SliceThickness), "secs": secs, "maxsl": maxsl})
    calib["ser"][sid] = g

# ---- anatomical landmarks (picked on the real slices: series, instance, column, row) ----
def P(sid, inst, i, j):
    s = calib["ser"][sid]
    return list(np.round(np.add(s["ipp"][inst - 1], np.add(np.multiply(s["row"], i * s["ps"]), np.multiply(s["col"], j * s["ps"]))), 1))
LM = {
    "hh":   P("cor_t1", 6, 300, 270),   # humeral head centre
    "acro": P("cor_t1", 6, 195, 150),   # acromion / AC joint
    "ssp":  P("cor_t1", 6, 335, 215),   # supraspinatus tendon at the greater tuberosity
    "gt":   P("cor_t1", 6, 358, 250),   # greater tuberosity, lateral cortex
    "axr":  P("cor_t1", 6, 285, 360),   # inferior glenoid / axillary recess
    "glen": P("ax_t2", 5, 226, 255),    # glenoid face (mid)
    "bic":  P("ax_t2", 5, 322, 190),    # long head of biceps in the groove
    "subs": P("ax_t2", 5, 232, 212),    # subscapularis, anterior to the glenoid
    "isp":  P("ax_t2", 5, 290, 296),    # infraspinatus / teres minor, behind the head
}
LM["sneck"] = list(np.round(np.add(LM["glen"], [-10, 3, 0]), 1))   # scapular neck, medial to the glenoid
calib["lm"] = LM
# the radiographer's own oblique angles (in-plane direction on the axial, degrees from +x toward +y)
calib["real"] = {"cor": -14.4, "sag": 67.4}

json.dump(calib, open(os.path.join(OUT, "calib.json"), "w"), indent=1)
open(os.path.join(OUT, "calib.js"), "w").write("window.MRS_CALIB=" + json.dumps(calib, separators=(",", ":")) + ";\n")
print("ok", {k: v["n"] for k, v in calib["ser"].items()})
