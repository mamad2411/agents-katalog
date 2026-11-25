---

## name: anatomy
description: >
  Expert anatomy assistant for medical students and researchers. Use this skill whenever the user needs:
  understanding human body structure, organ systems, anatomical terminology, comparative anatomy, or any rigorous academic 
  treatment of anatomy. Covers skeletal, muscular, nervous, cardiovascular, respiratory, and digestive systems.
license: MIT
compatibility: opencode
metadata:
  audience: medical-students
  category: medicine

# Anatomy — Academic Research Assistant

Covers: **Skeletal System · Muscular System · Nervous System · Cardiovascular System · Respiratory System · Digestive System · Anatomical Planes**

---

## Anatomical Terminology

### Directional Terms

|Term|Opposite|Meaning|
|----|---------|-------|
|Anterior/Posterior|Ventral/Dorsal|Toward front/back|
| Superior/Inferior|Cranial/Caudal|Toward head/feet|
|Medial/Lateral|—|Toward midline/away|
|Proximal/Distal|—|Toward trunk/away|
|Superficial/Deep|—|Toward surface/inside|
|Palmar/Plantar|Volar|Hand/foot surface|

### Anatomical Planes

|Plane|Divides|Example use|
|------|--------|-----------|
|Sagittal|Left/right|MRI midsagittal|
|Coronal (Frontal)|Anterior/posterior|Coronal CT|
|Transverse (Axial)|Superior/inferior|CT axial slices|
|Oblique|Angled|Specialized imaging|

---

## Skeletal System

### Bone Classification

|Category|Examples|Features|
|--------|--------|-----------|
|Long bones|Femur, humerus|Shaft + epiphyses|
|Short bones|Carpals, tarsals|Cube-shaped|
|Flat bones|Scapula, skull|Thin, protective|
|Irregular bones|Vertebrae|Complex shapes|
|Sesamoid bones|Patella|Embedded in tendon|

### Axial Skeleton

```python
class SkeletalAnatomy:
    """Skeletal system information"""
    
    # Skull bones
    SKULL_BONES = {
        "cranial": ["frontal", "parietal (2)", "temporal (2)", 
                    "occipital", "sphenoid", "ethmoid"],
        "facial": ["nasal (2)", "maxilla (2)", "zygomatic (2)",
                   "mandible", "palatine (2)", "lacrimal (2)", "vomer"]
    }
    
    # Vertebral column
    VERTEBRAL_REGIONS = {
        "cervical": {"count": 7, "features": "Transverse foramina, bifid spinous"},
        "thoracic": {"count": 12, "features": "Costal facets"},
        "lumbar": {"count": 5, "features": "Large bodies, no foramina"},
        "sacral": {"count": 5, "fused": True},
        "coccygeal": {"count": 4, "fused": True}
    }
    
    # Major bone markings
    BONE_MARKINGS = {
        "processes": ["spinous", "transverse", "condyle", "tubercle", 
                      "trochanter", "tuberosity"],
        "depressions": ["fossa", "acetabulum", "glenoid cavity"],
        "openings": ["foramen", "meatus", "sinus", "canal"]
    }
```

### Appendicular Skeleton

|Bone|Location|Joints|
|----|--------|-------|
|Clavicle|Shoulder girdle|Sternoclavicular, acromioclavicular|
|Scapula|Posterior thorax|Glenohumeral|
|Humerus|Arm|Elbow|
|Radius/Forearm|Wrist, elbow|
|Femur|Thigh|Hip, knee|
|Tibia/Fibula|Leg|Ankle, knee|
|Pelvis|Hip|Ox Coxae|

---

## Muscular System

### Muscle Classification

|Type|Characteristics|Examples|
|-----|---------------|--------|
|Skeletal|Striated, voluntary|Most body muscles|
|Smooth|Involuntary, non-striated|Vessels, gut|
|Cardiac|Involuntary, striated|Heart|

### Major Muscle Groups

```python
class MuscularAnatomy:
    """Muscle information"""
    
    # Upper limb
    SHOULDER_MUSCLES = {
        "rotator_cuff": ["supraspinatus", "infraspinatus", 
                         "teres minor", "subscapularis"],
        "other": ["deltoid", "pectoralis major", "latissimus dorsi"]
    }
    
    ARM_MUSCLES = {
        "anterior": ["biceps brachii", "brachialis", "coracobrachialis"],
        "posterior": ["triceps brachii"]
    }
    
    # Lower limb
    HIP_MUSCLES = {
        "flexors": ["iliopsoas", "rectus femoris", "tensor fasciae latae"],
        "extensors": ["gluteus maximus", "hamstrings"],
        "abductors": ["gluteus medius", "gluteus minimus"],
        "adductors": ["adductor magnus", "adductor longus", "pectineus"]
    }
    
    LEG_MUSCLES = {
        "anterior": ["quadriceps femoris", "tibialis anterior"],
        "posterior": ["hamstrings", "gastrocnemius", "soleus"]
    }
```

### Muscle Attachment Patterns

|Origin|Insertion|Movement|
|-------|---------|--------|
|Movable bone (proximal)|Stationary bone (distal)|Contraction moves|

---

## Nervous System

### Central Nervous System

```python
class NervousAnatomy:
    """Nervous system information"""
    
    # Brain regions
    BRAIN_REGIONS = {
        "forebrain": {
            "telencephalon": ["cerebral cortex", "basal ganglia", "limbic system"],
            "diencephalon": ["thalamus", "hypothalamus", "epithalamus"]
        },
        "midbrain": ["tectum", "tegmentum", "crura cerebri"],
        "hindbrain": {
            "metencephalon": ["pons", "cerebellum"],
            "myelencephalon": ["medulla oblongata"]
        }
    }
    
    # Cranial nerves
    CRANIAL_NERVES = {
        1: "Olfactory (sensory)",
        2: "Optic (sensory)",
        3: "Oculomotor (motor)",
        4: "Trochlear (motor)",
        5: "Trigeminal (mixed)",
        6: "Abducens (motor)",
        7: "Facial (mixed)",
        8: "Vestibulocochlear (sensory)",
        9: "Glossopharyngeal (mixed)",
        10: "Vagus (mixed)",
        11: "Accessory (motor)",
        12: "Hypoglossal (motor)"
    }
    
    # Spinal cord segments
    SPINAL_CORD = {
        "cervical": {"pairs": 8, "levels": "C1-C8"},
        "thoracic": {"pairs": 12, "levels": "T1-T12"},
        "lumbar": {"pairs": 5, "levels": "L1-L5"},
        "sacral": {"pairs": 5, "levels": "S1-S5"},
        "coccygeal": {"pairs": 1, "levels": "Co1"}
    }
```

### Peripheral Nervous System

|Division|Components|Function|
|--------|----------|---------|
|Somatic|12 cranial + 31 spinal|Voluntary movement|
|Autonomic|Sympathetic/parasympathetic|Involuntary|

---

## Cardiovascular System

### Heart Anatomy

```
Heart Layers:
┌────────────────────────────────────┐
│     Pericardium (visceral/parietal)│
├────────────────────────────────────┤
│     Myocardium                     │
├────────────────────────────────────┤
│     Endocardium                    │
└────────────────────────────────────┘

Chambers: RA → RV → LA → LV
Valves:   Tricuspid → Pulmonic → Mitral → Aortic
```

### Great Vessels

```python
class CardiovascularAnatomy:
    """Cardiovascular system"""
    
    # Heart conduction system
    CONDUCTION_SYSTEM = {
        "SA_node": {"location": "Right atrium, crista terminalis",
                    "rate": "60-100 bpm"},
        "AV_node": {"location": "Tricuspid valve area",
                    "rate": "40-60 bpm"},
        "Bundle_of_His": {"location": "Interventricular septum"},
        "Purkinje_fibers": {"location": "Ventricular walls"}
    }
    
    # Blood supply
    CORONARY_ARTERIES = {
        "LAD": {"supplies": "Anterior wall, septum", "branch": "Left coronary"},
        "LCx": {"supplies": "Lateral wall", "branch": "Left coronary"},
        "RCA": {"supplies": "Right atrium, posterior wall", "branch": "Right coronary"}
    }
```

---

## Respiratory System

### Airway Divisions

```python
class RespiratoryAnatomy:
    """Respiratory system"""
    
    # Conducting zone
    CONDUCTING_ZONE = [
        "Nose → Nasal cavity",
        "Pharynx → Larynx",
        "Trachea → Bronchi",
        "Bronchioles → Terminal bronchioles"
    ]
    
    # Respiratory zone
    RESPIRATORY_ZONE = [
        "Respiratory bronchioles",
        "Alveolar ducts",
        "Alveolar sacs"
    ]
    
    # Lobes and segments
    LUNG_SEGMENTS = {
        "right_upper": ["apical", "posterior", "anterior"],
        "right_middle": ["lateral", "medial"],
        "right_lower": ["superior", "medial basal", "anterior basal",
                       "lateral basal", "posterior basal"],
        "left_upper": ["apicoposterior", "anterior", "lingular"],
        "left_lower": ["superior", "anteromedial basal",
                      "lateral basal", "posterior basal"]
    }
```

---

## Digestive System

### GI Tract Layers

```
From lumen outward:
1. Mucosa: epithelium, lamina propria, muscularis mucosae
2. Submucosa: connective tissue, vessels, Meissner's plexus
3. Muscularis externa: circular, longitudinal, Auerbach's plexus
4. Adventitia/Serosa: connective tissue
```

### Accessory Organs

|Organ|Function|Duct|
|-----|--------|-----|
|Liver|Bile production|Hepatic → Cystic → Common bile|
|Gallbladder|Bile storage|Cystic → Common bile|
|Pancreas|Digestion + hormones|Pancreatic → Common|
|Salivary glands|Digestion|Various|

---

## Common Errors to Avoid

1. **Confusing anatomical terms** — Anterior vs. posterior
2. **Wrong muscle origins/insertions** — Know functional significance
3. **Misidentifying foramina** — Each has specific contents
4. **Confusing nerves and vessels** — Different anatomical courses
5. **Ignoring clinical correlations** — Anatomy has medical relevance
6. **Not knowing left vs. right** — Anatomical position standard
7. **Overlooking variations** — Normal anatomical variants exist
8. **Forgetting embryological origins** — Explains relationships

