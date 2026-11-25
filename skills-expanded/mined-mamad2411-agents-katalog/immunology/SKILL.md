---

## name: immunology
description: >
  Expert immunology assistant for academic researchers. Use this skill whenever the user needs:
  analysis of immune system components and functions, antibody response optimization, T-cell and B-cell 
  biology research, immune signaling pathway analysis, vaccine development support, flow cytometry 
  interpretation, immunological disorder research, or any rigorous academic treatment of immunology.
  Trigger for any immunology, immunology-related disease, or immune response question where academic 
  depth, correct terminology, and scientific rigor are expected.
license: MIT
 compatibility: opencode
metadata:
  audience: researchers
  category: biology

# Immunology — Academic Research Assistant

Covers: **Innate Immunity · Adaptive Immunity · Antibody Biology · T-cell Immunology · Cytokines & Signaling · Autoimmunity · Immunodeficiency · Vaccine Immunology · Flow Cytometry**

---

## Immune System Components

### Innate Immunity (Non-specific)

The innate immune system provides the first line of defense and responds rapidly (minutes to hours) to pathogens without prior sensitization.

|Component|Function|Key Markers/Features|
|---------|--------|-------------------|
|**Physical barriers**|Skin, mucous membranes, epithelial tight junctions|Desquamation, antimicrobial peptides|
|**Phagocytes**|Macrophages, neutrophils, dendritic cells|NK cells: CD16+, CD56+; Macrophages: CD14+, CD68+|
|**Complement system**|Opsonization, lysis, inflammation|C3a, C5a, membrane attack complex|
|**Dendritic cells**|Antigen presentation, bridge to adaptive|CD11c+, HLA-DR+, CD141+ (cDC1), CD1c+ (cDC2)|
|**Natural killer cells**| cytotoxic killing of infected/tumor cells|CD16+, CD56dim/bright|
|**Pattern recognition receptors**|TLRs, NLRs, RLRs|TLR4 (LPS), TLR3 (viral dsRNA)|

### Adaptive Immunity (Antigen-specific)

The adaptive immune system develops over days and provides long-lasting protection through immunological memory.

|Component|Function|Key Markers|
|---------|--------|------------|
|**B cells**|Antibody production, antigen presentation|CD19+, CD20+, CD21+, surface Ig+|
|**T helper cells (CD4+)**|Helper functions, cytokine production|CD3+, CD4+|
|**T cytotoxic cells (CD8+)**|Direct killing of infected cells|CD3+, CD8+|
|**Regulatory T cells**|Immune tolerance|CD4+, CD25+, FOXP3+|
|**Memory B cells**|Long-term antibody production|CD27+, IgD-|
|**Memory T cells**|Rapid secondary response|CD45RO+, CD27+|

---

## Antibody Biology

### Antibody Structure

Immunoglobulins (Ig) are Y-shaped proteins composed of two heavy chains and two light chains.

```
       ┌──────────────────────────────────────┐
       │           Variable Region            │
       │         (VH - Heavy Chain)           │
       │         (VL - Light Chain)           │
       └──────────────────┬───────────────────┘
                        ╱ ╲
       ┌────────────────┴───┴────────────────┐
       │            Hinge Region              │
       └──────────────────┬───────────────────┘
       ┌──────────────────┴───────────────────┐
       │         Constant Region (CH)        │
       └──────────────────────────────────────┘
              ┌──────────────┐
              │   Light      │
              │   Chain      │
              │   (CL)       │
              └──────────────┘
```

### Antibody Classes (Isotypes)

|Isotype|Structure|Primary Location|Key Functions|
|-------|---------|-----------------|---------------|
|**IgG**|Monomer (γ heavy chain)|Blood, extracellular fluid|Secondary response, opsonization, complement activation, placental transfer|
|**IgA**|Dimer (α heavy chain)|Mucous membranes, secretions|Mucosal immunity, dimeric with secretory component|
|**IgM**|Pentamer (μ heavy chain)|Blood, B cell surface|Primary response, complement activation, B cell receptor|
|**IgE**|Monomer (ε heavy chain)|Basophils, mast cells|Allergy, parasite defense, bound to FcεRI|
|**IgD**|Monomer (δ heavy chain)|B cell surface, blood|Coadministration with IgM, B cell activation|

### Antibody Naming Conventions

- **Polyclonal antibodies**: Multiple epitopes, heterogeneous preparation
- **Monoclonal antibodies**: Single epitope, homogeneous, produced by hybridomas
- **Nomenclature**: Prefix + target + -mab (e.g., pembrolizumab, rituximab)
- **Humanized antibodies**: Murine variable regions grafted to human framework

---

## T-Cell Immunology

### T-Cell Receptor (TCR) Biology

The TCR is a heterodimer (αβ or γδ) that recognizes antigens presented on MHC molecules.

```
TCR Complex:
┌─────────────────────────────────────────┐
│         αβ Heterodimer (TCR)            │
├─────────────────────────────────────────┤
│         CD3 Complex (Signal Transduction)│
│         ζ-chain (homodimer)            │
├─────────────────────────────────────────┤
│         CD4 or CD8 Coreceptor            │
└─────────────────────────────────────────┘
```

### Major Histocompatibility Complex (MHC)

|MHC Class|Presents To|Cell Types| Gene Location|
|---------|-----------|----------|--------------|
|**MHC Class I**|CD8+ T cells|All nucleated cells|HLA-A, -B, -C|
|**MHC Class II**|CD4+ T cells|Professional APCs (DC, macrophages, B cells)|HLA-DP, -DQ, -DR|

### T-Cell Differentiation States

|Subset|Master Transcription Factor|Cytokines Produced|Function|
|------|---------------------------|------------------|--------|
|**Th1**|T-bet|IFN-γ, IL-2|Cellular immunity, viral defense|
|**Th2**|GATA3|IL-4, IL-5, IL-13|Humoral immunity, allergy|
|**Th17**|RORγt|IL-17, IL-22|Mucosal defense, autoimmunity|
|**Tfh**|BCL6|IL-21|B cell help in germinal centers|
|**Treg**|FOXP3|IL-10, TGF-β|Immune tolerance|

---

## Cytokines & Immune Signaling

### Key Cytokines

|Cytokine|Source|Primary Target|Function|
|--------|------|---------------|--------|
|**IL-1β**|Macrophages, DCs|Wide range|Inflammation, fever, leukocyte recruitment|
|**IL-6**|Macrophages, T cells|Liver, immune cells|Acute phase response, B cell differentiation|
|**IFN-α/β**|Various cells|Various cells|Antiviral state, MHC I upregulation|
|**IFN-γ**|Th1, NK cells|Macrophages, various cells|Macrophage activation, Th1 differentiation|
|**TNF-α**|Macrophages, T cells|Wide range|Inflammation, apoptosis, cachexia|
|**IL-10**|Treg, Th2, macrophages|Wide range|Anti-inflammatory, inhibits APCs|
|**IL-12**|DCs, macrophages|NK, Th1|Th1 differentiation, NK activation|
|**IL-17A/F**|Th17|Epithelial cells, fibroblasts|Pro-inflammatory, neutrophil recruitment|

### Signaling Pathways

```python
# Cytokine signaling conceptual model
class CytokineSignaling:
    """Simplified cytokine signaling pathway model"""
    
    JAK_STAT_PATHWAY = {
        "Type I (e.g., IL-6)": {
            "receptor": "gp130 family",
            "JAKs": "JAK1, JAK2, TYK2",
            "STATs": "STAT1, STAT3",
            "outcome": "Acute phase response, B cell differentiation"
        },
        "Type II (e.g., IFN-γ)": {
            "receptor": "IFNAR family", 
            "JAKs": "JAK1, JAK2",
            "STATs": "STAT1, STAT2",
            "outcome": "MHC upregulation, antiviral response"
        }
    }
    
    NFκB_PATHWAY = {
        "canonical": {
            "activators": ["TNF-α", "IL-1β", "LPS", "TLRs"],
            "IKK_complex": "IKKα, IKKβ, IKKγ",
            "inhibitor": "IκBα",
            "transcription_factor": "p65/p50"
        }
    }
```

---

## Flow Cytometry Analysis

### Sample Preparation

1. **Cell count and viability**: Aim for >90% viability, 1×10⁶ cells/mL
2. **Staining**: Surface markers (4°C, 30 min) → intracellular (fix/perm)
3. **Controls**:
   - Unstained control (autofluorescence)
   - Fluorescence minus one (FMO)
   - Isotype controls
   - Viability dye

### Common Fluorophores

|Fluorophore|Excitation (nm)|Emission (nm)|Channels|
|-----------|---------------|--------------|--------|
|FITC|488|519|Green|
|PE|488|578|Yellow-orange|
|APC|633|660|Red|
|PerCP-Cy5.5|488|710|Deep red|
|Pacific Blue|405|450|Blue|
|BV421|405|421|Blue|

### Gating Strategy Example

```
Raw Data
    ↓ (FS/SS gate) → Lymphocyte gate
    ↓ (Single cells) → Live/Dead exclusion
    ↓ (CD45+) → Leukocyte population
    ↓ (CD3+) → T cells
    ↓ (CD4/CD8) → Helper vs Cytotoxic
    ↓ (CD45RA/CCR7) → Naive vs Memory
```

---

## Autoimmunity & Immunodeficiency

### Autoimmune Disease Classification

|Category|Examples|Autoantibodies|Mechanism|
|--------|--------|---------------|----------|
|**Systemic**|SLE, RA, Sjögren|Anti-dsDNA, RF|Anti-nuclear antibodies|
|**Organ-specific**|Type 1 Diabetes, Graves'|Anti-insulin, Anti-TSHR|Tissue-specific autoimmunity|
|**Cell-mediated**|Multiple sclerosis|T cells reactive to myelin|Delayed-type hypersensitivity|

### Primary Immunodeficiencies

|Disorder|Defect|Clinical Features|Treatment|
|---------|------|------------------|----------|
|**SCID**|Adaptive immunity absent|Severe infections, failure to thrive|BMT, gene therapy|
|**X-linked agammaglobulinemia**|B cell development|Bacterial infections|IVIG|
|**Chronic granulomatous disease**|NADPH oxidase|Recurrent catalase+ infections|IFN-γ, prophylaxis|
|**Hyper-IgM syndrome**|Class-switching defect|Opportunistic infections|IVIG, prophylaxis|

---

## Vaccine Immunology

### Vaccine Types

|Type|Example|Mechanism|
|----|-------|----------|
|**Live attenuated**|MMR, Varicella|Replication-competent, mimics natural infection|
|**Inactivated**|Polio (IPV), Rabies|Killed pathogen, cannot replicate|
|**Subunit**|Hepatitis B, HPV|Protein/polysaccharide antigens only|
|**Toxoid**|Tetanus, Diphtheria|Inactivated toxins|
|**mRNA**|COVID-19 mRNA vaccines|In vivo protein production|
|**Viral vector**|Ebola, some COVID-19|Recombinant viral expression|

### Vaccine Response Evaluation

```python
# Serological response interpretation
class VaccineResponse:
    """Interpret vaccine-induced immune responses"""
    
    def calculate_seroconversion(self, pre_titer, post_titer, threshold=4):
        """4-fold rise = seroconversion"""
        if pre_titer < threshold:
            return post_titer >= threshold
        return post_titer / pre_titer >= 4
    
    def interpret_protective_titer(self, antibody_level, protective_level=10):
        """Assess if titer exceeds protective threshold"""
        return antibody_level >= protective_level
    
    # Memory B cell response (flow cytometry)
    def memory_bcell_response(self, antigen_specific_bcells, total_bcells):
        """Calculate percentage of antigen-specific memory B cells"""
        if total_bcells == 0:
            return 0
        return (antigen_specific_bcells / total_bcells) * 100
```

---

## Immunological Techniques

### ELISA (Enzyme-Linked Immunosorbent Assay)

|Type|Detection|Use Cases|
|----|---------|----------|
|Direct ELISA|Antigen detection|Infection diagnosis|
|Indirect ELISA|Antibody detection|Vaccine response|
|Sandwich ELISA|Antigen detection in complexes|Disease biomarkers|
|Competitive ELISA|Low molecular weight analytes|Hormones, drugs|

### Western Blot

- **Purpose**: Detect specific proteins in a mixture
- **Detection**: Primary antibody + enzyme-conjugated secondary antibody
- **Substrate**: Chemiluminescent (ECL), colorimetric, fluorescent

### Common Errors to Avoid

1. **Ignoring Fc receptor binding** — use Fc block for phagocyte staining
2. **Not accounting for dead cells** — always include viability dye
3. **Insufficient controls** — FMO is essential for proper gating
4. **Citing antibody clone without validation** — verify specificity
5. **Assuming isotype controls match primary** — they should match fluorophore
6. **Over-gating rare populations** — report parent population percentages
7. **Confusing correlation with causation** — functional assays validate phenotypic findings

