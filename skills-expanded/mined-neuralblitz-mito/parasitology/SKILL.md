---

## name: parasitology
description: >
  Expert parasitology assistant for researchers and medical professionals. Use this skill whenever the user needs:
  understanding parasitic organisms, host-parasite relationships, disease transmission, treatment strategies, or any rigorous 
  academic treatment of parasitology. Covers protozoa, helminths, arthropod vectors, and tropical diseases.
license: MIT
compatibility: opencode
metadata:
  audience: researchers
  category: biology

# Parasitology — Academic Research Assistant

Covers: **Parasitic Protozoa · Helminths · Arthropod Vectors · Malaria · Disease Transmission · Host Immunity · Treatment Strategies**

---

## Parasite Classification

### Major Groups

|Group|Examples|Location|Transmission|
|------|--------|--------|-------------|
|Protozoa|Plasmodium, Giardia|Various|Fecal-oral, vector|
|Trematodes|Schistosoma, Fasciola|Blood, liver|Water, snail|
|Cestodes|Taenia, Echinococcus|Intestine|Food-borne|
|Nematodes|Ascaris, Hookworm|Intestine, tissue|Fecal-oral, skin|

```python
class ParasiteClassification:
    """Parasite taxonomy"""
    
    PROTOZOA = {
        "Amoebozoa": {
            "examples": ["Entamoeba histolytica", "Acanthamoeba"],
            "disease": ["Amoebiasis", "Amoebic keratitis"],
            "transmission": "Fecal-oral, water"
        },
        "Apicomplexa": {
            "examples": ["Plasmodium spp.", "Toxoplasma gondii", "Cryptosporidium"],
            "disease": ["Malaria", "Toxoplasmosis", "Cryptosporidiosis"],
            "transmission": "Vector (mosquito), food, cat feces"
        },
        "Kinetoplastea": {
            "examples": ["Trypanosoma brucei", "Leishmania"],
            "disease": ["African sleeping sickness", "Leishmaniasis"],
            "transmission": "Tsetse fly, sandfly"
        },
        "Ciliophora": {
            "examples": ["Balantidium coli"],
            "disease": ["Balantidiasis"],
            "transmission": "Fecal-oral (pigs)"
        }
    }
    
    HELMINTHS = {
        "Nematoda": {
            "soil_transmitted": ["Ascaris lumbricoides", "Trichuris trichiura", 
                                "Necator americanus", "Strongyloides stercoralis"],
            "tissue_nematodes": ["Wuchereria bancrofti", "Onchocerca volvulus",
                                "Dracunculus medinensis"]
        },
        "Trematoda": {
            "blood_flukes": ["Schistosoma mansoni", "S. japonicum", "S. haematobium"],
            "liver_flukes": ["Fasciola hepatica", "Opisthorchis"],
            "intestinal_flukes": ["Fasciolopsis buski"]
        },
        "Cestoda": {
            "intestinal": ["Taenia saginata", "Taenia solium", "Hymenolepis nana"],
            "tissue": ["Echinococcus granulosus", "Taenia solium (cysticercosis)"]
        }
    }
```

---

## Malaria (Plasmodium)

### Life Cycle

```
Human → Mosquito → Human
        ↓
1. Sporozoites injected → Liver (schizogony)
2. Merozoites released → Blood (erythrocytic cycle)
3. Gametocytes form → Mosquito takes up
4. Mosquito: Fertilization → Oocyst → Sporozoites
```

### Species Comparison

|Species|Mortality|Relapse|Fever Cycle|Geographic|
|-------|---------|--------|------------|-----------|
|P. falciparum|High|No|Irropical|Tropics|
|P. vivax|Moderate|Yes|48 hours|Wide|
|P. ovale|Moderate|Yes|48 hours|Africa|
|P. malariae|Low|No|72 hours|Wide|
|P. knowlesi|Day|None|24 hours|Southeast Asia|

```python
class MalariaParasitology:
    """Malaria calculations and info"""
    
    # Treatment guidelines
    UNCOMPLICATED_P_FALCIPARUM = {
        "ACT": ["Artemether-lumefantrine", "Artesunate-amodiaquine"],
        "alternative": ["Artesunate + sulfadoxine-pyrimethamine"],
        "primaquine": "G6PD testing required"
    }
    
    SEVERE_P_FALCIPARUM = {
        "IV_treatment": "IV Artesunate",
        "duration": "At least 24 hours",
        "follow_oral": "Complete 3-day ACT course"
    }
    
    # Diagnostic thresholds
    PARASITE_THRESHOLDS = {
        "light_microscopy": ">10 parasites/μL detectable",
        "RDT": "40-100 parasites/μL depending on test",
        "PCR": "<1 parasites/μL (research)"
    }
    
    def calculate_parasite_density(self, parasites_per_200_WBC, WBC_count):
        """
        Parasites/μL = (parasites/WBC) × WBC count
        """
        return (parasites_per_200_WBC / 200) * WBC_count
```

---

## Helminth Infections

### Soil-Transmitted Helminths (STH)

|Parasite|Infection Route|Egg/Larvae|Key Features|
|--------|---------------|-----------|------------|
|Ascaris lumbricoides|Fecal-oral|Egg|Intestinal, large|
|Trichuris trichiura|Fecal-oral|Egg|Whipworm|
|Necator americanus|Skin|Larvae|Hookworm, anemia|
|Strongyloides stercoralis|Skin|Larvae|Auto-infection|

```python
class Helminthology:
    """Helminth treatment"""
    
    STH_TREATMENT = {
        "albendazole": {
            "ascaris": "400 mg single dose",
            "trichuris": "400 mg × 3 days",
            "hookworm": "400 mg single dose",
            "efficacy": "~95% cure for Ascaris"
        },
        "mebendazole": {
            "ascaris": "100 mg × 3 days",
            "trichuris": "100 mg × 3 days",
            "hookworm": "100 mg × 3 days"
        },
        "ivermectin": {
            "strongyloides": "200 μg/kg × 2 days"
        }
    }
    
    SCHISTOSOMIASIS = {
        "praziquantel": {
            "adults": "40 mg/kg single dose",
            "children": "40 mg/kg single dose",
            "efficacy": "S. mansoni, S. haematobium: good",
            "limitation": "S. japonicum: less effective"
        }
    }
```

### Echinococcosis

|Treatment|Indication|
|----------|----------|
|Albendazole|Pre- and post-surgery|
|Praziquantel|Potential benefit|
|Surgery|Prefan cyst removal|
|PAIR|Percutaneous aspiration|

---

## Vector-Borne Diseases

### Arthropod Vectors

|Vector|Pathogen|Disease|Geographic Distribution|
|------|--------|-------|----------------------|
|Anopheles mosquito|Protozoa|Malaria|Tropical, subtropical|
|Culex mosquito|Filarioidea|Filariasis|Worldwide|
|Aedes mosquito|Virus|Dengue, Zika, Yellow fever|Tropical|
|Phlebotomine sandfly|Leishmania|Leishmaniasis|Tropical, Mediterranean|
|Tsetse fly|Trypanosoma|African sleeping sickness|Africa|
|tsetse fly||||

```python
class VectorBorneDiseases:
    """Vector control methods"""
    
    PERSONAL_PROTECTION = {
        "bed_nets": {
            "type": "Long-lasting insecticidal nets (LLIN)",
            "efficacy": "Reduces child mortality by ~20%"
        },
        "repellents": {
            "DEET": "20-30% concentration",
            "Picaridin": "20% concentration",
            "IR3535": "20% concentration"
        },
        "clothing": {
            "treatment": "Permethrin treatment",
            "color": "Light colors preferred"
        }
    }
    
    LARVICIDING = {
        "larvicides": ["Bti (Bacillus thuringiensis)", "temefos"],
        "source_reduction": "Remove standing water"
    }
```

---

## Host-Parasite Interactions

### Immune Response

```python
class ParasiteImmunology:
    """Immune response to parasites"""
    
    INNATE_RESPONSE = {
        "macrophages": "Phagocytosis, cytokine production",
        "eosinophils": "Attack helminths via ADCC",
        "NK_cells": "Produce IFN-γ in leishmaniasis",
        "granulocytes": "Neutrophils kill some protozoa"
    }
    
    ADAPTIVE_RESPONSE = {
        "Th1": {
            "parasites": "Intracellular (Leishmania, Toxoplasma)",
            "cytokines": "IFN-γ, IL-2",
            "protection": "Cell-mediated immunity"
        },
        "Th2": {
            "parasites": "Extracellular (helminths)",
            "cytokines": "IL-4, IL-5, IL-13",
            "protection": "IgE, eosinophils, mast cells"
        }
    }
    
    IMMUNE_EVASION = {
        "antigenic_variation": "Trypanosoma, Plasmodium",
        "molecular_mimicry": "Schistosoma",
        "immunosuppression": "Many parasites suppress host immunity"
    }
```

### Pathogenesis Mechanisms

|Mechanism|Example|
|---------|-------|
|Mechanical damage|Tissue invasion, obstruction|
|Immunopathology|Immune complex, granulomas|
|Nutrient competition|Anemia in hookworm|
|Toxin production|Exotoxins from some protozoa|

---

## Diagnostic Methods

### Microscopy

|Technique|Use|Detection Limit|
|----------|---|----------------|
|Thick smear|Detection|10-40 parasites/μL|
|Thin smear|Species ID|Requires higher density|
|Kato-Katz|Stool helminths|Egg counting|
|Formalin-ether concentration|Increased yield|Cysts, ova|

### Molecular Methods

|Method|Application|
|------|-----------|
|PCR|Species identification|
|RT-PCR|Drug resistance|
|Nucleic acid sequencing|Species, strain typing|

---

## Treatment Strategies

### Antiprotozoal Drugs

```python
class AntiparasiticTreatment:
    """Treatment protocols"""
    
    DRUG_CLASSES = {
        "aminoquinolines": {
            "chloroquine": "P. vivax, ovale, malariae (not falciparum)",
            "primaquine": "Liver hypnozoites (vivax, ovale)",
            "tafenoquine": "Single dose radical cure"
        },
        "artemisinins": {
            "artemether": "ACT component",
            "artesunate": "Severe malaria IV",
            "artemisinin_derivatives": "Fast-acting blood schizonticide"
        },
        "isonicotinic_acid_hydrazides": {
            "isoniazid": "Mycobacteria (not parasites)"
        },
        "nitroimidazoles": {
            "metronidazole": "Giardia, Entamoeba, Trichomonas",
            "tinidazole": "Single dose alternatives"
        }
    }
```

---

## Common Errors to Avoid

1. **Ignoring species identification** — Different species need different treatment
2. **Forgetting G6PD testing** — Primaquine causes hemolysis
3. **Incomplete dosing** — Single-dose treatments often need follow-up
4. **Ignoring re-infection** — Environmental control essential
5. **Wrong specimen type** — Blood vs. stool vs. tissue
6. **Not considering co-infections** — Common in endemic areas
7. **Drug resistance** — Know local resistance patterns
8. **Confusing cure with elimination** — Different public health goals

