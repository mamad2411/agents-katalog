---
name: inorganic-chemistry
description: "Coordination chemistry, crystal field theory, ligand field theory, organometallics, bioinorganic chemistry, and main group elements"
category: chemistry
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/chemistry/inorganic-chemistry/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Inorganic Chemistry

## Scope
Inorganic chemistry examines the synthesis, structure, and bonding of non-carbon and metallo-organic compounds. This skill provides structural, magnetic, and electronic evaluation of coordination complexes and main group solids.

## Coordination Chemistry & Bonding Models

### 1. Crystal Field Theory (CFT)
- $d$-Orbital Splitting in Octahedral Fields ($O_h$):
  - Lower energy: $t_{2g}$ ($d_{xy}, d_{yz}, d_{xz}$), energy $-0.4 \Delta_o$.
  - Higher energy: $e_g$ ($d_{z^2}, d_{x^2-y^2}$), energy $+0.6 \Delta_o$.
- **Spectrochemical Series**:
  $$I^- < Br^- < S^{2-} < SCN^- < Cl^- < F^- < OH^- < H_2O < NH_3 < en < NO_2^- < CN^- < CO$$
- **High-Spin vs. Low-Spin**:
  - High-spin occurs when $\Delta_o < P$ (pairing energy) $\to$ weak-field ligands.
  - Low-spin occurs when $\Delta_o > P$ $\to$ strong-field ligands ($CN^-, CO$).
- **Tetrahedral Fields ($T_d$)**: $\Delta_t = \frac{4}{9} \Delta_o$; always high-spin due to small splitting.

### 2. Ligand Field Theory (LFT) & Molecular Orbitals
- Treats ligand-metal interaction with covalent $\sigma$- and $\pi$-bonding considerations.
- **$\pi$-Donor Ligands** ($Cl^-, I^-$): Destabilize $t_{2g}$, decreasing $\Delta_o$.
- **$\pi$-Acceptor Ligands** ($CO, CN^-$): Synergistic back-bonding stabilizes $t_{2g}$, drastically increasing $\Delta_o$.

### 3. Organometallic 18-Electron Rule
- Total valence electron count ($N_{\text{val}}$) for stable transition metal organometallics equals 18:
  $$N_{\text{val}} = n_d + \sum e_{\text{ligands}} - q_{\text{complex}}$$
- Neutral ligand counting method:
  - $CO, PR_3, NR_3$: $2e^-$ donors
  - Halides, alkyls ($R^-$), hydride ($H^-$): $1e^-$ donors
  - Cyclopentadienyl ($\eta^5-Cp$): $5e^-$ donor
  - Benzene ($\eta^6-C_6H_6$): $6e^-$ donor

### 4. Magnetism & Tanabe-Sugano Diagrams
- **Effective Magnetic Moment**: $\mu_{\text{eff}} = \sqrt{n(n+2)}\mu_B$ (spin-only formula, where $n$ is unpaired electrons).
- **Tanabe-Sugano Diagrams**: Predict electronic absorption spectra (UV-Vis) across weak-to-strong ligand fields.

## Standards & References
- **Standards**: IUPAC Red Book (Nomenclature of Inorganic Chemistry).
- **Software**: VESTA (crystal structures), Mercury (CSD), CrystalMaker.
- **Canonical References**: Miessler, Fischer & Tarr — *Inorganic Chemistry*; Cotton, Wilkinson & Gaus — *Basic Inorganic Chemistry*.
