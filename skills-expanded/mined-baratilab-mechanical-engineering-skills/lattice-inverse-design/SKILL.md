---
name: lattice-inverse-design
description: Design 3D-printable lattice unit cells for a target stiffness — TPMS and hybrid-TPMS implicit cells, printability checks (one connected solid, no sealed cavities, periodic), voxel homogenisation of the full 6x6 stiffness (checked against exact solutions), parametric inverse search, a GLU3D-style stiffness-conditioned 3D diffusion model with surrogate guidance, and watertight tiled STL export. Based on GLU3D (Barati Farimani Lab). Use when someone needs a lightweight infill, core, or architected material with given E/G (isotropic or anisotropic), wants to compare TPMS against strut lattices, or wants to train a generative lattice model on their own cells.
---

# Lattice inverse design (GLU3D)

GLU3D (Jadhav et al., *Adv. Funct. Mater.* 34 (2024) 2404165) works like this:
- It builds a dataset of unit cells from implicit equations: 22 TPMS families, plus hybrids that
  blend 2–4 families (Eqs. 3–7).
- It homogenises each cell to its 6 × 6 stiffness matrix.
- It trains a 3D conditional DDPM that turns a target stiffness into a new cell's implicit field.
  A tanh scaling (Eq. 9) keeps the surface at level set 0, which raised mesh yield from 33–51% to
  100%.
- Printed PLA cells followed the requested modulus.

`scripts/glu3d.py` covers the whole loop. Everything except the neural models runs on numpy and
scipy; scikit-image and trimesh are needed for meshes, pyamg is optional for speed, and PyTorch is
needed for the models. Paper numbers and the interpretation choices are in
`references/paper-notes.md`.

Stiffness is **relative to the solid** (E/Es) unless you pass `--Es`. The cell is one period of
side 1; choose its printed size at export.

## Workflow
1. **Pin down the target.**
   - Ask for E (or E1, E2, E3), optionally G, and either a density budget or "as light as possible".
   - Ask for the process and its minimum wall or strut thickness, and the cell size. Convert walls to
     the cell scale: 0.5 mm walls in a 10 mm cell is 0.05 of the cell.
   - Express targets relative to the solid: printed PLA ≈ 3.5 GPa, Ti-6Al-4V LPBF ≈ 110 GPa.
2. **Try a known cell first** (seconds):
   ```bash
   python scripts/glu3d.py families
   python scripts/glu3d.py cell --families gyroid --h 0.25 --png g.png
   python scripts/glu3d.py cell --families gyroid,primitive --mode H2 --t 0.3 --h 0.2
   python scripts/glu3d.py cell --families gyroid --h 0.25 --freq 2,2,1   # anisotropic: E3 ≈ 2.8 E1
   python scripts/glu3d.py compare --cells '[["gyroid sheet", {"families":["gyroid"]}]]' --png cmp.png
   ```
   - `cell` reports the printability checks, the periodicity error, the full C^H, E1–E3, G, ν, the
     Zener anisotropy ratio and the weakest and strongest directional modulus.
   - `compare` sweeps the thickness against simple-cubic and BCC strut lattices.
3. **Inverse design without a GPU:** `search --target E=0.08,G=0.03 [--data ds.npz] [--density-weight 0.2]`.
   - It ranks dataset cells (or random ones) by mean |log error| against the target.
   - It then refines the thickness `h` and bias `a` of the best three by re-homogenising.
   - This is the dependable route for one-off designs.
4. **Generative route (paper):**
   ```bash
   python scripts/glu3d.py dataset --n 3000 --res 65 --hres 32 --out ds.npz     # paper: 3723 cells, 64^3
   python scripts/glu3d.py train-surrogate --data ds.npz --out sur.pt
   python scripts/glu3d.py train --data ds.npz --out glu3d.pt --size 64 --chans 1,4,8,16,32,64 --surrogate sur.pt --device cuda
   python scripts/glu3d.py generate --model glu3d.pt --target E=0.1,G=0.04 --vfrac 0.3 --n 8 --steps 100
   python scripts/glu3d.py evaluate --gen generated.npz --data ds.npz          # success, periodicity, Dice/Chamfer/Hausdorff, FEM error
   ```
   - The defaults match the paper: cosine schedule, T = 500, Huber loss, 20% unconditional
     training, stiffness entries standardised to mean 50, φ̂min = 0.75, and an ancestral DDPM
     sampler with 500 steps (`--steps 100 --eta 0` for fast DDIM).
   - The networks train on the periodic grid with circular padding, so **generated cells are
     exactly periodic**. Other small-data fixes are listed in `references/paper-notes.md`.
   - Generation also conditions on volume fraction by default, because the paper names its absence
     as the reason high-modulus targets failed. Use `--paper-cond` for the paper's stiffness-only
     setting.
   - `--guidance > 1` turns on classifier-free guidance.
   - **Always re-homogenise the generated cells** (`evaluate` does this) and keep only those that
     hit the target. The surrogate is for guidance, not for acceptance.
5. **Export:** `stl --npz generated.npz --index 2 --cell-mm 10 --tiles 4,4,4 --out part.stl`, or
   `cell --spec '<spec JSON from search>' --stl part.stl --cell-mm 10 --tiles 4,4,4`.
   - The mesh is watertight and capped at the boundary, with volume ≈ vfrac × box (tested).
   - Check printability in the slicer: minimum wall, and whether trapped powder or resin can drain.
     The `dfm-review` or `agentscad-fdm-dfam` skills can help.

## Judgement calls
- **Elastic only.** C^H is the small-strain stiffness. The paper's claims about energy absorption and
  peak load came from compression tests. For crash or impact use, test coupons or run nonlinear
  FEA.
- **Hand over the directional modulus, not just E1.** A simple-cubic lattice has a high axial E, but
  it is very weak in shear and off-axis (see `compare`).
- **Resolution.** The node grid is what you print. The voxel grid used for homogenisation needs at
  least 3–4 voxels through each wall. `cell_stiffness` falls back to full resolution if
  coarsening loses material. 24³ is within about 1% of 32³ for a gyroid at vf 0.25.
- **Printability filters**, used for the dataset and for search:
  - the solid must be one periodic piece that reaches every face;
  - every void region must open to the faces, so there are no sealed cavities;
  - 0.05 < vf < 0.95;
  - Dice > 0.75 against an accepted cell counts as a duplicate.
- **Cost and data.** A 32³ homogenisation takes about 5–10 s on a laptop CPU, and a 24³ one about
  3 s. The paper's 64³ DDPM took 16 h on 4 GPUs with 3723 cells.
  - A CPU rehearsal with 300 cells at 16³ produces periodic but unusable cells: stiffness error of
    about 200%.
  - Use `search` for real designs until you have paper-scale data and a GPU.

Cite: Jadhav, Berthel, Hu, Panat, Beuth, Barati Farimani, *Generative Lattice Units with 3D
Diffusion for Inverse Design: GLU3D*, Adv. Funct. Mater. 34 (2024) 2404165.
