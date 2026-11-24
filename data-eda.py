#!/usr/bin/env python3
"""data-eda — EDA ringkas 1 file dataset, output ≤40 baris (hemat token).
Pakai: ~/.agents/test-venv/bin/python3 data-eda.py <file> [--rows N]"""
import os
import sys


def load(path):
    import pandas as pd
    ext = os.path.splitext(path)[1].lower()
    if ext == ".jsonl":
        return pd.read_json(path, lines=True)
    if ext in (".xls", ".xlsx", ".xlsm"):
        return pd.read_excel(path)
    if ext == ".arff":
        # parser ARFF minimal: lewatkan header @, ambil section @data
        import io
        rows, indata, attrs = [], False, []
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("%"):
                    continue
                low = line.lower()
                if low.startswith("@data"):
                    indata = True
                    continue
                if line.startswith("@"):
                    if low.startswith("@attribute"):
                        parts = line.split(None, 2)
                        attrs.append(parts[1].strip("'\"") if len(parts) > 1 else "")
                    continue
                if indata:
                    rows.append(line)
        df = pd.read_csv(io.StringIO("\n".join(rows)), header=None)
        if len(attrs) == df.shape[1]:
            df.columns = attrs
        else:
            df.columns = [f"attr{i}" for i in range(df.shape[1])]
        return df
    if ext in (".dat", ".data", ".txt"):
        # coba whitespace dulu, fallback koma/titik-koma
        for sep in (None, ",", ";", "\t"):
            try:
                df = pd.read_csv(path, sep=sep, header=None if sep is None else "infer")
                if df.shape[1] > 1:
                    return df
            except Exception:
                continue
        return pd.read_csv(path, sep=None, engine="python")
    return pd.read_csv(path)


def main():
    path = sys.argv[1]
    if not os.path.exists(path):
        sys.exit(f"file tidak ada: {path}")
    import pandas as pd
    df = load(path)
    print(f"file : {os.path.basename(path)}")
    print(f"shape: {df.shape[0]} baris x {df.shape[1]} kolom")
    print("\n-- dtypes --")
    print(df.dtypes.value_counts().to_string())
    miss = df.isna().sum()
    miss = miss[miss > 0]
    print(f"\n-- missing ({len(miss)} kolom) --")
    print(miss.head(10).to_string() if len(miss) else "tidak ada")
    num = df.select_dtypes("number")
    if len(num.columns):
        d = num.describe().T[["mean", "std", "min", "25%", "50%", "75%", "max"]]
        d = d.round(3)
        print(f"\n-- statistik numerik ({len(num.columns)} kolom, tampil 12) --")
        print(d.head(12).to_string())
    print("\n-- 3 baris pertama --")
    print(df.head(3).to_string(max_cols=12))
    # tebakan target: nama mengandung kata kunci, else kolom numerik terakhir
    kw = ("class", "label", "target", "result", "strength", "mpg", "price",
          "sales", "output", "yield", "status")
    guess = [c for c in df.columns if any(k in str(c).lower() for k in kw)]
    if not guess and len(num.columns):
        guess = [num.columns[-1]]
    if guess:
        g = df[guess[0]]
        vc = g.value_counts().head(6)
        print(f"\n-- kandidat target '{guess[0]}' ({g.nunique()} unik) --")
        print(vc.to_string())


if __name__ == "__main__":
    main()
