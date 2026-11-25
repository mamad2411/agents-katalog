---
name: amber-parameterize
description: AmberTools small-molecule parameterization from SMILES. Use when
  parameterizing a ligand or custom molecule, generating GAFF/GAFF2 force field
  parameters, running antechamber, parmchk2, or tleap, or converting AMBER
  topology to GROMACS format with acpype.
---

# AmberTools Small-Molecule Parameterization

## Workflow Overview

```
SMILES → obabel (3D mol2) → antechamber (GAFF2 + AM1-BCC) → parmchk2 (frcmod) → tleap (AMBER topology) → acpype (GROMACS files)
```

---

## Environment Setup

Activate the Amber conda environment before running any commands:

```bash
conda activate amber    # adjust name to your actual env
which obabel antechamber parmchk2 tleap acpype  # verify all tools in PATH
```

If any tool is missing:
- `obabel`: `conda install -c conda-forge openbabel`
- `antechamber`, `parmchk2`, `tleap`: part of AmberTools (`conda install -c conda-forge ambertools`)
- `acpype`: `conda install -c conda-forge acpype`

---

## Directory Layout

```
MOLECULE/
├── smiles.txt          # record of input SMILES string
├── mol2/               # raw and parameterized mol2 files
│   ├── MOL.mol2        # initial 3D structure from obabel
│   └── MOL_gaff2.mol2  # antechamber output with GAFF2 types + charges
├── amber/              # AMBER topology files
│   ├── tleap.in        # tleap input script
│   ├── MOL.frcmod      # missing parameters from parmchk2
│   ├── MOL.prmtop      # AMBER topology
│   └── MOL.inpcrd      # AMBER coordinates
└── gromacs/            # GROMACS-format files from acpype
    ├── MOL_GMX.itp     # atom types + bonded/nonbonded parameters
    ├── MOL_GMX.gro     # coordinates
    └── MOL_GMX.top     # standalone topology (includes itp)
```

Create directories before starting:

```bash
mkdir -p MOLECULE/{mol2,amber,gromacs}
echo "SMILES_STRING" > MOLECULE/smiles.txt
```

---

## Step 1 — SMILES → 3D mol2 (Open Babel)

```bash
obabel -:"SMILES_STRING" -o mol2 -O MOLECULE/mol2/MOL.mol2 --gen3d
```

- `-:"SMILES"` — SMILES as literal string (note the colon prefix, no input file)
- `--gen3d` — generates 3D coordinates (required; without it coordinates are all zeros)
- For charged molecules, ensure the SMILES encodes the correct protonation state

**Verify:**
```bash
# Check that coordinates are non-zero
grep -v "^@" MOLECULE/mol2/MOL.mol2 | awk 'NF==9 {print $3,$4,$5}' | head -5
# Should show non-zero x,y,z values
```

**Alternative if obabel geometry is poor:** use RDKit:
```python
from rdkit import Chem
from rdkit.Chem import AllChem
mol = Chem.MolFromSmiles("SMILES_STRING")
mol = Chem.AddHs(mol)
AllChem.EmbedMolecule(mol, AllChem.ETKDG())
AllChem.MMFFOptimizeMolecule(mol)
Chem.MolToMolFile(mol, "MOLECULE/mol2/MOL.sdf")
obabel MOLECULE/mol2/MOL.sdf -o mol2 -O MOLECULE/mol2/MOL.mol2
```

---

## Step 2 — Antechamber (GAFF2 atom types + AM1-BCC charges)

```bash
antechamber \
    -i MOLECULE/mol2/MOL.mol2 -fi mol2 \
    -o MOLECULE/mol2/MOL_gaff2.mol2 -fo mol2 \
    -at gaff2 \
    -c bcc \
    -s 2 \
    -nc CHARGE
```

| Flag | Meaning |
|---|---|
| `-at gaff2` | GAFF2 atom types (preferred; use `gaff` only for compatibility with older params) |
| `-c bcc` | AM1-BCC charges — fast, accurate enough for most MD applications |
| `-s 2` | verbosity level (shows progress) |
| `-nc CHARGE` | net formal charge as integer (e.g. `0`, `1`, `-1`) — **critical to set correctly** |

**Verify:**
```bash
# Check CHARGE column (col 9) in output mol2
grep -A 100 "@<TRIPOS>ATOM" MOLECULE/mol2/MOL_gaff2.mol2 | grep -B 100 "@<TRIPOS>BOND" | \
    awk '{print $1, $2, $9}' | head -20
# Charges should be non-zero and sum approximately to net charge
```

**Common issue:** antechamber calls `sqm` for AM1-BCC; if it fails check that `sqm` is in PATH (part of AmberTools).

---

## Step 3 — parmchk2 (supplemental force field parameters)

```bash
parmchk2 \
    -i MOLECULE/mol2/MOL_gaff2.mol2 \
    -f mol2 \
    -o MOLECULE/amber/MOL.frcmod
```

**Verify:**
```bash
cat MOLECULE/amber/MOL.frcmod
# A minimal or blank frcmod means GAFF2 covers all parameters — this is fine
# Non-blank entries are supplemental parameters; check for "ATTN, need revision" warnings
```

---

## Step 4 — tleap (AMBER topology and coordinates)

Create the tleap input file (or copy from `templates/tleap.in` and substitute placeholders):

```bash
cat > MOLECULE/amber/tleap.in << 'EOF'
source leaprc.gaff2
MOL = loadmol2 MOLECULE/mol2/MOL_gaff2.mol2
check MOL
loadamberparams MOLECULE/amber/MOL.frcmod
saveamberparm MOL MOLECULE/amber/MOL.prmtop MOLECULE/amber/MOL.inpcrd
quit
EOF
```

Run tleap:

```bash
tleap -f MOLECULE/amber/tleap.in
```

**Verify:**
```bash
ls -lh MOLECULE/amber/MOL.prmtop MOLECULE/amber/MOL.inpcrd
# Both files must exist and be non-empty
# Check tleap output for FATAL errors (warnings are usually OK)
```

**Common tleap errors:**

| Error | Fix |
|---|---|
| `FATAL: Could not open file` | Check paths in tleap.in are correct; run tleap from project root |
| `Could not find bond parameter` | parmchk2 frcmod incomplete; check for "ATTN" lines |
| `Added missing heavy atom` | Molecule has unresolved valence; fix mol2 or SMILES |

---

## Step 5 — acpype (convert to GROMACS format)

```bash
acpype \
    -p MOLECULE/amber/MOL.prmtop \
    -x MOLECULE/amber/MOL.inpcrd \
    -b MOL

mv MOL.acpype/MOL_GMX.* MOLECULE/gromacs/
rm -r MOL.acpype
```

**Verify:**
```bash
# Check key sections exist in the itp file
grep -c "\[ atomtypes \]\|\[ atoms \]\|\[ bonds \]" MOLECULE/gromacs/MOL_GMX.itp
# Should be 3 (one match per section)
```

Output files:
- `MOL_GMX.itp` — force field parameters (include this in system topology)
- `MOL_GMX.gro` — coordinates
- `MOL_GMX.top` — standalone topology (useful for testing in isolation)

---

## Python Automation Script

Save as `parameterize.py` and run with:
```bash
python parameterize.py 'SMILES_STRING' OUTDIR MOLNAME CHARGE
```

```python
#!/usr/bin/env python3
"""
AmberTools small-molecule parameterization pipeline.
Usage: python parameterize.py 'SMILES' [output_dir] [mol_name] [net_charge]
"""
import sys
import subprocess
from pathlib import Path


def run(cmd, **kwargs):
    print(f"  $ {cmd}")
    subprocess.run(cmd, shell=True, check=True, **kwargs)


def parameterize(smiles, output_dir="molecule", mol_name="MOL", charge=0):
    base = Path(output_dir)
    mol2_dir = base / "mol2"
    amber_dir = base / "amber"
    gmx_dir = base / "gromacs"

    for d in (mol2_dir, amber_dir, gmx_dir):
        d.mkdir(parents=True, exist_ok=True)

    # Record SMILES
    (base / "smiles.txt").write_text(smiles + "\n")

    mol2_raw = mol2_dir / f"{mol_name}.mol2"
    mol2_gaff = mol2_dir / f"{mol_name}_gaff2.mol2"
    frcmod = amber_dir / f"{mol_name}.frcmod"
    prmtop = amber_dir / f"{mol_name}.prmtop"
    inpcrd = amber_dir / f"{mol_name}.inpcrd"
    tleap_in = amber_dir / "tleap.in"

    # Step 1: SMILES → 3D mol2
    print("\n[1/5] Generating 3D structure with Open Babel...")
    run(f"obabel -:'{smiles}' -o mol2 -O {mol2_raw} --gen3d")

    # Step 2: Antechamber (GAFF2 + AM1-BCC)
    print("\n[2/5] Running antechamber (GAFF2, AM1-BCC charges)...")
    run(
        f"antechamber "
        f"-i {mol2_raw} -fi mol2 "
        f"-o {mol2_gaff} -fo mol2 "
        f"-at gaff2 -c bcc -s 2 -nc {charge}"
    )

    # Step 3: parmchk2
    print("\n[3/5] Running parmchk2...")
    run(f"parmchk2 -i {mol2_gaff} -f mol2 -o {frcmod}")

    # Step 4: tleap
    print("\n[4/5] Running tleap...")
    tleap_in.write_text(
        f"source leaprc.gaff2\n"
        f"{mol_name} = loadmol2 {mol2_gaff}\n"
        f"check {mol_name}\n"
        f"loadamberparams {frcmod}\n"
        f"saveamberparm {mol_name} {prmtop} {inpcrd}\n"
        f"quit\n"
    )
    run(f"tleap -f {tleap_in}")

    # Step 5: acpype → GROMACS
    print("\n[5/5] Converting to GROMACS format with acpype...")
    run(f"acpype -p {prmtop} -x {inpcrd} -b {mol_name}")
    run(f"mv {mol_name}.acpype/{mol_name}_GMX.* {gmx_dir}/")
    run(f"rm -r {mol_name}.acpype")

    print(f"""
Parameterization complete. Files in {output_dir}/:

  GROMACS itp:  {gmx_dir}/{mol_name}_GMX.itp
  GROMACS gro:  {gmx_dir}/{mol_name}_GMX.gro
  AMBER prmtop: {prmtop}
  AMBER inpcrd: {inpcrd}

To include in a GROMACS simulation topology (topol.top):
  Add before [ system ]:   #include "{gmx_dir}/{mol_name}_GMX.itp"
  Add in [ molecules ]:    {mol_name}    1
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parameterize.py 'SMILES' [outdir] [molname] [charge]")
        sys.exit(1)
    parameterize(
        smiles=sys.argv[1],
        output_dir=sys.argv[2] if len(sys.argv) > 2 else "molecule",
        mol_name=sys.argv[3] if len(sys.argv) > 3 else "MOL",
        charge=int(sys.argv[4]) if len(sys.argv) > 4 else 0,
    )
```

---

## Key Parameter Choices

| Parameter | Default | Alternative | When to change |
|---|---|---|---|
| Force field | `gaff2` | `gaff` | Use GAFF only for compatibility with older parameterizations |
| Charge method | `bcc` (AM1-BCC) | `resp` | RESP for higher accuracy; requires Gaussian (`-c resp -gn gaussian`) |
| Net charge | `0` | any integer | Always set to actual formal charge of the molecule |
| 3D builder | `obabel --gen3d` | RDKit ETKDG, Avogadro | If obabel produces bad geometry (clashes, wrong ring conformations) |
| leaprc | `leaprc.gaff2` | `leaprc.gaff` | Match the `-at` flag used in antechamber |

---

## Common Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `obabel: command not found` | openbabel not in PATH | `conda install -c conda-forge openbabel`; check conda env is active |
| `Error: cannot run 'sqm'` (antechamber) | AmberTools incomplete / sqm not in PATH | Reinstall ambertools: `conda install -c conda-forge ambertools` |
| `Error: Total charge (X) != net charge (Y)` | `-nc` value wrong | Recalculate formal charge from SMILES; set `-nc` accordingly |
| `FATAL: Could not open file` (tleap) | Wrong path in tleap.in | Use absolute paths or run tleap from the directory containing the files |
| `acpype: FileNotFoundError` | prmtop/inpcrd not created | Check tleap log for FATAL errors; fix and re-run tleap |
| `Warning: missing frcmod parameters` | GAFF2 incomplete for exotic atoms | Add manual parameters to .frcmod; or use RESP + higher-level QM |

---

## Integration with GROMACS Protein Simulations

After parameterization, to combine ligand with a protein system:

```bash
# 1. Combine coordinates
gmx insert-molecules \
    -f prep/protein_processed.gro \
    -ci MOLECULE/gromacs/MOL_GMX.gro \
    -nmol 1 -o prep/complex.gro -radius 0.3

# 2. Edit topol.top — add before [ system ]:
#    #include "MOLECULE/gromacs/MOL_GMX.itp"
# 3. In [ molecules ] section add:
#    MOL   1

# 4. Continue with solvate → genion → EM → NVT → NPT → production
```

See the `gromacs-prep` skill for the full downstream workflow.
