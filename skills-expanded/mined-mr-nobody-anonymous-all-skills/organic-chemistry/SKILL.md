---
name: organic-chemistry
description: "Nomenclature, stereochemistry, reaction mechanisms (SN1/SN2, E1/E2, additions), synthesis planning, and functional group interconversions"
category: chemistry
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/chemistry/organic-chemistry/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Organic Chemistry

## Scope
Organic chemistry focuses on the structure, properties, composition, reactions, and synthesis of carbon-containing compounds. This skill covers functional group transformations, mechanistic electron pushing, stereochemical assignments, and retrosynthetic analysis.

## Mechanistic Frameworks

### 1. Stereochemistry & Isomerism
- **Cahn-Ingold-Prelog (CIP) Rules**:
  - Assign priorities by atomic number ($Z$).
  - For ties, proceed along the chain until the first point of difference.
  - View with priority 4 pointing away: clockwise = $(R)$, counter-clockwise = $(S)$.
- **Enantiomers vs. Diastereomers**:
  - Enantiomers: Non-superimposable mirror images; identical physical properties except optical rotation ($[\alpha]$).
  - Diastereomers: Non-mirror image stereoisomers; differing melting points, NMR spectra, and chromatographic retention times.

### 2. Nucleophilic Substitution & Elimination
| Mechanism | Rate Law | Stereochemistry | Solvent Preference | Substrate Preference |
|---|---|---|---|---|
| **$S_N1$** | $\text{Rate} = k[\text{Substrate}]$ | Racemization (carbocation intermediate) | Polar protic ($H_2O$, $MeOH$) | $3^\circ > 2^\circ \gg 1^\circ$ |
| **$S_N2$** | $\text{Rate} = k[\text{Substrate}][\text{Nu}]$ | Inversion of configuration (Walden) | Polar aprotic (DMF, DMSO, MeCN) | $\text{Me} > 1^\circ > 2^\circ \gg 3^\circ$ |
| **$E1$** | $\text{Rate} = k[\text{Substrate}]$ | Zaitsev product favored (more substituted alkene) | Polar protic | $3^\circ > 2^\circ$ |
| **$E2$** | $\text{Rate} = k[\text{Substrate}][\text{Base}]$ | Anti-periplanar geometry required ($H-C-C-X = 180^\circ$) | Non-polar or aprotic | $3^\circ > 2^\circ > 1^\circ$ |

### 3. Carbonyl Chemistry & Enolates
- **Nucleophilic Addition to Carbonyls**: Grignard reagents ($RMgX$), hydrides ($NaBH_4, LiAlH_4$), organolithiums.
- **Nucleophilic Acyl Substitution**: Carboxylic acid derivatives reactivity: Acyl chloride > Anhydride > Ester $\approx$ Carboxylic acid > Amide.
- **Aldol Condensation**: Enolate generation via base ($LDA$ or $NaOH$), nucleophilic addition to aldehyde/ketone, dehydration ($lpha,\beta$-unsaturated carbonyl).

### 4. Retrosynthetic Analysis
- Break complex targets into commercial synthons using strategic disconnections ($\Rightarrow$).
- **Core disconnections**:
  - C-C bond formation via Grignard, Wittig, Diels-Alder, Heck, Suzuki-Miyaura coupling.
  - Functional group interconversions (FGI): Alcohol oxidation (DMP, Swern, PCC), reduction, halogenation.

## Toolchains & Standards
- **Computational / Cheminformatics**: RDKit, ChemBioDraw, Gaussian, Spartan, ORCA.
- **Databases**: Reaxys, SciFinder, PubChem, Cambridge Structural Database (CSD).
- **Canonical References**: March's *Advanced Organic Chemistry*; Clayden, Greeves & Warren — *Organic Chemistry*; Carey & Sundberg.
