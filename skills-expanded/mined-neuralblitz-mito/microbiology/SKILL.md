---

## name: microbiology
description: >
  Expert microbiology assistant for researchers and students. Use this skill whenever the user needs:
  understanding microbial structure, metabolism, genetics, pathogenicity, antimicrobial resistance, host-microbe interactions,
  or any rigorous academic treatment of microbiology. Covers bacteria, viruses, fungi, microbial ecology, and clinical diagnostics.
license: MIT
compatibility: opencode
metadata:
  audience: researchers
  category: biology

# Microbiology — Academic Research Assistant

Covers: **Bacterial Structure · Microbial Metabolism · Microbial Genetics · Viral Replication · Pathogenicity · Antimicrobial Resistance · Host Defense · Microbial Ecology**

---

## Bacterial Structure

### Cell Envelope

|Component|Function|Gram+/Gram-|
|---------|--------|------------|
|Cell wall|Peptidoglycan|Thick|Thin|
|Outer membrane|Lipopolysaccharide|No|Yes|
|Cytoplasmic membrane|Permeability|Yes|Yes|
|Capsule|Protection|No (most)|Variable|

```python
class BacterialCellStructure:
    """Bacterial cell biology"""
    
    GRAM_STAINING = {
        "procedure": ["Crystal violet", "Gram's iodine", "Alcohol", "Safranin"],
        "Gram_positive": "Retains crystal violet (purple)",
        "Gram_negative": "Decolorized, takes safranin (red)"
    }
    
    CELL_WALL_SYNTHESIS = {
        "target": "Peptidoglycan",
        "inhibitors": {
            "penicillins": "Transpeptidases (PBPs)",
            "cephalosporins": "PBPs",
            "vancomycin": "D-Ala-D-Ala terminal",
            "bacitracin": "Bactoprenol cycling"
        }
    }
    
    SURFACE_STRUCTURES = {
        "flagella": "Motility, attachment",
        "pili/fimbriae": "Adhesion, conjugation",
        "capsule": "Resistance to phagocytosis",
        "slime_layer": "Biofilm formation"
    }
```

---

## Microbial Metabolism

### Energy Generation

|Process|Oxygen|Products|Examples|
|-------|-------|---------|---------|
|Aerobic respiration|Required|CO₂, H₂O|Streptococcus|
|Facultative anaerobes|Optional|Varies|E. coli|
|Obligate anaerobes|Toxic|Varies|Clostridium|
|Fermentation|No respiration|Lactate, ethanol|Lactobacillus|

### Metabolic Pathways

```python
class MicrobialMetabolism:
    """Metabolic pathways"""
    
    GLYCOLYSIS = {
        "pathway": "EMP (Embden-Meyerhof-Parnas)",
        "input": "Glucose",
        "output": "2 Pyruvate + 2 ATP + 2 NADH",
        "enzymes": ["Hexokinase", "Phosphofructokinase", "Pyruvate kinase"]
    }
    
    FERMENTATION_TYPES = {
        "lactic_acid": {
            "bacteria": ["Lactobacillus", "Streptococcus"],
            "products": "Lactate",
            "homolactic": "2 lactate",
            "heterolactic": "Lactate + ethanol + CO₂"
        },
        "alcoholic": {
            "bacteria": "Zymomonas",
            "fungi": "Saccharomyces (yeast)",
            "products": "Ethanol + CO₂"
        },
        "mixed_acid": {
            "bacteria": "E. coli",
            "products": "Lactate, succinate, acetate, formate, ethanol"
        }
    }
    
    BIOCHEMICAL_TESTS = {
        "catalase": "Breaks H₂O₂ → O₂ + H₂O\nPositive: Staph, not Strep",
        "oxidase": "Cytochrome c oxidase\nPositive: Pseudomonas, Neisseria",
        "coagulase": "Clots plasma\nPositive: Staph aureus",
        "optochin": "Soluble in bile\nPositive: Strep pneumoniae"
    }
```

---

## Microbial Genetics

### Horizontal Gene Transfer

|Mechanism|Donor|Transfer|Example|
|---------|-----|--------|-------|
|Transformation|Naked DNA|Environment|Streptococcus|
|Conjugation|Pilus|Mobile DNA|E. coli Hfr|
|Transduction|Bacteriophage|Phage-mediated|Staphylococcus|

```python
class MicrobialGenetics:
    """Genetic analysis"""
    
    GENE_EXPRESSION = {
        "operon_model": "Lac operon example",
        "regulation_levels": [
            "Transcription initiation",
            "Translation",
            "Protein stability"
        ]
    }
    
    PLASMID_FEATURES = {
        "replication": "Origin of replication (ori)",
        "selection": "Antibiotic resistance genes",
        "conjugation": "Tra genes for conjugation",
        "size": "1-200 kb typically"
    }
    
    MUTATION_TYPES = {
        "point": "Single base change",
        "frameshift": "Insertion/deletion (not multiple of 3)",
        "deletion": "Larger region loss",
        "insertion": "Mobile elements, transposons"
    }
```

---

## Antimicrobial Resistance

### Resistance Mechanisms

|Mechanism|Example Drug Affected|
|---------|-------------------|
|Enzymatic degradation|β-lactamases (penicillins)|
|Modified target|PBP changes (methicillin)|
|Efflux pumps|Tetracyclines|
|Altered permeability|Porin loss (Gram-negative)|
|Metabolic bypass|Sulfonamides|

```python
class AntimicrobialResistance:
    """Resistance mechanisms"""
    
    COMMON_RESISTANCE = {
        "MRSA": {
            "gene": "mecA",
            "protein": "Modified PBP2a",
            "class": "β-lactam resistant"
        },
        "VRE": {
            "genes": "vanA, vanB",
            "target": "D-Ala-D-Ala → D-Ala-D-Lac",
            "drug": "Vancomycin"
        },
        "ESBL": {
            "enzymes": "CTX-M, TEM, SHV",
            "substrates": "Extended-spectrum cephalosporins",
            "treatment": "Carbapenems"
        },
        "CRE": {
            "enzymes": "KPC, NDM, VIM, IMP",
            "class": "Carbapenemases",
            "treatment": "Limited options"
        }
    }
    
    ANTIBIOTIC_CLASSES = {
        "β-lactams": {
            "penicillins": ["ampicillin", "amoxicillin"],
            "cephalosporins": ["cefotaxime", "ceftriaxone"],
            "carbapenems": ["meropenem", "imipenem"],
            "mechanism": "Inhibit cell wall synthesis"
        },
        "aminoglycosides": {
            "examples": ["gentamicin", "tobramycin", "amikacin"],
            "mechanism": "Inhibit 30S ribosome"
        },
        "fluoroquinolones": {
            "examples": ["ciprofloxacin", "levofloxacin"],
            "mechanism": "Inhibit DNA gyrase"
        },
        "macrolides": {
            "examples": ["azithromycin", "erythromycin"],
            "mechanism": "Inhibit 50S ribosome"
        }
    }
```

---

## Viral Replication

### Replication Strategies

```python
class ViralReplication:
    """Virus life cycles"""
    
    DNA_VIRUSES = {
        "herpesvirus": {
            "site": "Nucleus",
            "replication": "DNA → mRNA",
            "assembly": "Nucleus",
            "envelope": "From nuclear membrane"
        },
        "poxvirus": {
            "site": "Cytoplasm",
            "unique": "Complete replication in cytoplasm"
        }
    }
    
    RNA_VIRUSES = {
        "positive_sense": {
            "examples": ["Poliovirus", "Hepatitis C", "SARS-CoV-2"],
            "directly_translated": "RNA acts as mRNA",
            "RNA-dependent_RNA_poly": "Required"
        },
        "negative_sense": {
            "examples": ["Influenza", "Rabies"],
            "needs_RNA_polymerase": "Bring or encode",
            "template": "RNA → mRNA"
        },
        "retroviruses": {
            "examples": ["HIV", "HTLV"],
            "enzyme": "Reverse transcriptase",
            "genome": "RNA → DNA → integration"
        }
    }
    
    ANTIVIRALS = {
        "HIV": ["Reverse transcriptase inhibitors", "Protease inhibitors", "Integrase inhibitors"],
        "Influenza": ["Neuraminidase inhibitors (oseltamivir)"],
        "Hepatitis C": ["Direct-acting antivirals (DAAs)"],
        "Herpes": ["Acyclovir (nucleoside analog)"]
    }
```

---

## Host Defense

### Innate Immunity

```python
class HostDefense:
    """Immune responses"""
    
    INNATE_BARRIERS = {
        "physical": ["Skin", "Mucous membranes", "Cilia"],
        "chemical": ["Stomach acid", "Fatty acids", "Lysozyme"],
        "microbiological": ["Normal flora competition"]
    }
    
    INNATE_CELLS = {
        "macrophages": "Phagocytosis, cytokine production",
        "neutrophils": "First responders, phagocytosis",
        "NK_cells": "Kill infected/cancer cells",
        "dendritic_cells": "Bridge to adaptive immunity"
    }
    
    PATTERN_RECOGNITION = {
        "TLRs": "Toll-like receptors",
        "NLRs": "NOD-like receptors",
        "RLRs": "RIG-I-like receptors",
        "ligands": "PAMPs (Pathogen-associated molecular patterns)"
    }
    
    INFLAMMATION = {
        "signs": ["Rubor (redness)", "Tumor (swelling)", 
                  "Calor (heat)", "Dolor (pain)", "Functio laesa (loss of function)"],
        "cytokines": ["IL-1", "IL-6", "TNF-α", "Chemokines"]
    }
```

---

## Clinical Microbiology

### Specimen Collection

```python
class ClinicalMicrobiology:
    """Diagnostic microbiology"""
    
    SPECIMEN_GUIDELINES = {
        "blood": {
            "volume": "10-20 mL adult",
            "bottles": "Aerobic + Anaerobic",
            "timing": "Before antibiotics, at fever spikes"
        },
        "urine": {
            "collection": "Clean-catch midstream",
            "transport": "Within 2 hours or refrigerate",
            "significant": ">10⁵ CFU/mL"
        },
        "sputum": {
            "quality": "Check squamous epithelial cells",
            "good": "<10 squamous, >25 WBCs per field"
        },
        "wound": {
            "specify": "Swab vs. tissue",
            "anaerobes": "Use anaerobic transport"
        }
    }
    
    CULTURE_INTERPRETATION = {
        "pure_culture": "Single pathogen isolated",
        "mixed_growth": "May be contaminant or polymicrobial",
        "no_growth": "Consider fungi, mycobacteria, viruses"
    }
```

---

## Microbial Ecology

### Microbiome

```python
class MicrobialEcology:
    """Environmental microbiology"""
    
    HUMAN_MICROBIOME = {
        "skin": "Staphylococcus, Corynebacterium",
        "oral": "Streptococcus, Anaerobes",
        "gut": "Bacteroides, Firmicutes, Bifidobacterium",
        "vagina": "Lactobacillus (dominant)"
    }
    
    BIOMEDICAL_PROCESSES = {
        "nitrogen_cycle": {
            "fixation": "Azotobacter, Rhizobium",
            "nitrification": "Nitrosomonas → Nitrobacter",
            "denitrification": "Pseudomonas"
        },
        "carbon_cycle": {
            "decomposition": "Fungi, bacteria",
            "methanogenesis": "Methanogens (archaea)"
        }
    }
```

---

## Common Errors to Avoid

1. **Ignoring biosafety levels** — BSL determines containment
2. **Not using appropriate controls** — Sterility, positivity controls
3. **Misinterpreting culture results** — Contamination vs. pathogen
4. **Ignoring fastidious organisms** — Special requirements
5. **Not considering resistance patterns** — Empiric therapy needs local data
6. **Confusing infection with colonization** — Context matters
7. **Forgetting anaerobes** — Common in deep infections
8. **Ignoring specimen quality** — Garbage in = garbage out

