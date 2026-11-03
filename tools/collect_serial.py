"""Collect labelled REAL windows from the node (set RAW_DUMP 1 in config.h).
  python collect_serial.py --port /dev/ttyUSB0 --machine rig1 --label imbalance --count 60 --out ../data
Then: python ml/train.py --real data/    (windows are split by machine, so use >=3 machines/sessions)"""
import argparse, os, serial

ap = argparse.ArgumentParser()
ap.add_argument("--port", required=True); ap.add_argument("--machine", required=True); ap.add_argument("--label", required=True)
ap.add_argument("--count", type=int, default=60); ap.add_argument("--out", default="data"); ap.add_argument("--baud", type=int, default=115200)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
ser = serial.Serial(a.port, a.baud, timeout=5)
n, buf, meta = 0, None, ""
while n < a.count:
    line = ser.readline().decode(errors="ignore").strip()
    if line.startswith("BEGIN"):
        meta, buf = line[6:], []
    elif line == "END" and buf is not None and len(buf) == 1024:
        with open(os.path.join(a.out, f"{a.machine}_{a.label}_{n:04d}.csv"), "w") as f:
            f.write("# " + meta + "\n" + "\n".join(buf) + "\n")
        n += 1; print("saved", n, meta); buf = None
    elif buf is not None and line.count(",") == 2:
        buf.append(line)
