---

## name: pediatrics
description: >
  Expert pediatrics assistant for medical students and researchers. Use this skill whenever the user needs:
  understanding of childhood development, pediatric diseases, growth assessment, developmental milestones, pediatric 
  pharmacology, vaccination schedules, or any rigorous academic treatment of pediatric medicine. Covers neonatal 
  care through adolescent health with age-appropriate approaches.
license: MIT
compatibility: opencode
metadata:
  audience: medical-students
  category: medicine

# Pediatrics — Academic Research Assistant

Covers: **Growth & Development · Neonatology · Pediatric Diseases · Vaccination · Nutrition · Adolescent Health · Developmental Milestones · Pediatric Pharmacology**

---

## Growth Assessment

### Growth Charts (WHO/CDC)

| Age | Weight Gain | Height Velocity |
|-----|-------------|-----------------|
| 0-3 months | ~25-30 g/day | ~3.5 cm/month |
| 3-6 months | ~15-20 g/day | ~2 cm/month |
| 6-12 months | ~10-15 g/day | ~1.5 cm/month |
| 1-2 years | ~2.5 kg/year | ~12 cm/year |
| 2-5 years | ~2 kg/year | ~6-8 cm/year |
| Puberty | Variable | Peak velocity: 8-14 cm/yr |

### Growth Parameters

```python
class GrowthAssessment:
    """Pediatric growth assessment tools"""
    
    # WHO Growth Standards (0-5 years)
    Z_SCORE_CUTOFFS = {
        "severe_malnutrition": -3,
        "moderate_malnutrition": -2,
        "overweight": 1,
        "obesity": 2
    }
    
    # Mid-parental height calculation
    def mid_parental_height(self, father_cm, mother_cm, sex):
        """
        Calculate target height
        Boys: (Father + Mother + 13) / 2
        Girls: (Father + Mother - 13) / 2
        """
        if sex.lower() == 'male':
            return (father_cm + mother_cm + 13) / 2
        else:
            return (father_cm + mother_cm - 13) / 2
    
    # Growth velocity calculation
    def height_velocity(self, height1, height2, months_between):
        """cm/year"""
        if months_between == 0:
            return 0
        return ((height2 - height1) / months_between) * 12
    
    # BMI calculation and interpretation
    def bmi_percentile(self, weight_kg, height_m, age_years, sex):
        """Calculate BMI and interpret percentile"""
        bmi = weight_kg / (height_m ** 2)
        # In practice, use CDC growth chart lookup
        # Simplified interpretation:
        if bmi < 14:
            return "underweight"
        elif bmi < 23:
            return "healthy weight"
        elif bmi < 28:
            return "overweight"
        else:
            return "obese"
```

### Normal Vital Signs by Age

|Age|HR (bpm)|RR (breaths/min)|SBP (mmHg)|
|---|--------|----------------|----------|
|Newborn|100-180|30-60|60-90|
|1-6 months|90-120|25-40|70-100|
|6-12 months|80-120|20-30|80-110|
|1-3 years|80-130|20-30|90-110|
|3-6 years|70-110|15-25|95-110|
|6-12 years|60-100|12-20|100-120|
|Adolescent|55-100|12-20|110-120|

---

## Developmental Milestones

### Gross Motor Development

|Age|Milestone|
|----|---------|
|2 months|Head control|
|4 months|Rolls over|
|6 months|Sits with support|
|8 months|Sits independently|
|10 months|Stands with support|
|12 months|Walks independently|
|18 months|Runs|
|2 years|Jumps|
|3 years|Trikes|
|4 years|Hops|
|5 years|Skips|

### Fine Motor Development

|Age|Milestone|
|----|---------|
|2 months|Fists uncurled|
|4 months|Reaches for objects|
|6 months|Palmar grasp|
|9 months|Pincer grasp|
|12 months|Voluntary release|
|18 months|Scribbles|
|2 years|Stacks 4 cubes|
|3 years|Copies circle|
|4 years|Copies square|
|5 years|Prints letters|

### Language Development

|Age|Milestone|
|----|---------|
|2 months|Coos|
|6 months|Babbles|
|12 months|First words|
|18 months|10-25 words|
|24 months|50+ words, 2-word phrases|
|3 years|3-4 word sentences|
|4 years|Complex sentences|
|5 years|Fluently speaks|

---

## Neonatology

### APGAR Score

|Parameter|0|1|2|
|---------|---|---|---|
|Appearance (color)|Blue/Pale|Body pink, extremities blue|All pink|
|Pulse (HR)|Absent|<100|>100|
|Grimace (reflex irritability)|No response|Weak cry/Cry|Cry|
|Activity (muscle tone)|Limp|Some flexion|Active motion|
|Respiration|Absent|Slow/Irregular|Cry|

|Interpretation|Score|
|--------------|------|
|Normal|7-10|
|Borderline|4-6|
|Resuscitation needed|<4|

### Neonatal Resuscitation

```
Initial Steps (first 30 seconds):
┌─────────────────────────────────────────┐
│ 1. Warm, dry, stimulate               │
│ 2. Clear airway if needed              │
│ 3. Assess breathing/cry               │
│ 4. Provide tactile stimulation         │
└────────────────────────────────────────┘
                    ↓
If not breathing:
┌─────────────────────────────────────────┐
│  Positive pressure ventilation        │
│  (PPV with mask or ETT)               │
│  40-60 breaths/min                      │
│  PEEP 5 cmH₂O                          │
└────────────────────────────────────────┘
                    ↓
If HR < 60 after 30 sec PPV:
┌─────────────────────────────────────────┐
│  Chest compressions                    │
│  90 compressions + 30 breaths/min     │
│  Depth: 1/3 chest diameter            │
│  Consider epinephrine                  │
└────────────────────────────────────────┘
```

---

## Pediatric Diseases

### Febrile Neonate Management

|Age|< 21 days|21-28 days|29-60 days|>60 days|
|---|----------|-----------|----------|--------|
|Workup|Blood culture, urine culture, CSF|Like <21 days if ill-appearing|Blood, urine, consider CSF|No routine labs if well-appearing|
|Admission|Mandatory|Mandatory if ill-consider admission|Consider admission|No admission if well-appearing|

### Common Pediatric Infections

|Disease|Agent|Treatment|Notes|
|-------|-----|---------|------|
|Strep pharyngitis|Strep pyogenes|Penicillin V 10 days|Throat culture not needed if positive rapid test|
|Otitis media|S. pneumoniae, H. influenzae|Amoxicillin first-line|Watchful waiting if mild|
|Bacterial meningitis|Hib, pneumococcus, meningococcus|Ceftriaxone + vancomycin|LP required for diagnosis|
|Pneumonia|RSV, bacterial|Ampicillin if bacterial|Viral most common < 5 yrs|

### Asthma Exacerbation Severity

|Severity|Mild|Moderate|Severe|Respiratory arrest|
|--------|-----|--------|------|-------------------|
|Symptoms|Walks|Talks with difficulty|At rest|Confused|
|Talk|Words|Sentences|Words|None|
|Alert|Alert|Alert|Agitated|Drowsy|
|Respirations|Increased|Marked increase|Labored|Arrested|
|O2 Sat|>95%|91-95%|<90%|---|
|PEF|≥70%|40-69%|<40%|---|

---

## Vaccination

### Recommended Immunization Schedule (0-18 months)

|Age|Vaccines|
|----|--------|
|Birth|HepB|
|2 months|Rotavirus, DTaP, Hib, PCV13, IPV|
|4 months|Rotavirus, DTaP, Hib, PCV13, IPV|
|6 months|Rotavirus, DTaP, Hib, PCV13, IPV, Influenza (annual)|
|12 months|MMR, VAR, HepA|
|15 months|DTaP, Hib, PCV13|
|18 months|HepA|

### Vaccine Abbreviations

|DTaP|Diphtheria, Tetanus, acellular Pertussis|
|-----|---------------------------------------|
|HepA/HepB|Hepatitis A/B|
|Hib|Haemophilus influenzae type b|
|IPV|Inactivated Polio Vaccine|
|MMR|Measles, Mumps, Rubella|
|PCV13|Pneumococcal conjugate 13-valent|
|Varicella|Chickenpox|
|RV|Rotavirus|

---

## Nutrition

### Breastfeeding

- **Exclusive breastfeeding**: Recommended 0-6 months
- **Continued breastfeeding**: Up to 2 years or beyond
- **Vitamin D**: 400 IU daily for all breastfed infants
- **Iron**: Fortified cereal at 6 months

### Formula Feeding

- **Standard formulas**: 20 kcal/oz, cow's milk protein
- **Hypoallergenic**: Extensively hydrolyzed for CMPA
- **Soy**: For lactose intolerance
- **Premature**: Higher protein, higher calorie (22-24 kcal/oz)

### Complementary Feeding

|Age|Solid Introduction|
|----|-------------------|
|4-6 months|Single-grain cereal|
|6 months|Pureed meats, vegetables, fruits|
|7-8 months|Soft table foods, finger foods|
|9-12 months|Variety of textures, family foods|
|12 months|Whole cow's milk|

---

## Adolescent Health

### Tanner Staging

|Boys - Genital|Stage|Description|
|---------------|-----|-----------|
|Stage 1|Preadolescent|Testes 1-3 mL, scrotum smooth|
|Stage 2|Testicular enlargement 4-6 mL|Scrotum enlarges, skin smooth|
|Stage 3|Penis lengthens|Testes 12-15 mL|
|Stage 4|Penis lengthens, darkens|Testes 15-20 mL|
|Stage 5|Adult size|Testes >20 mL|

|Boys - Pubic Hair|Stage|Description|
|-----------------|-----|-----------|
|Stage 1|No hair|
|Stage 2|Sparse, straight at base|
|Stage 3|Curly, coarse|
|Stage 4|Adult type, not on thighs|
|Stage 5|Adult type, spread to thighs|

### Sexual Health Screening

|Screening|Age|Notes|
|---------|---|------|
|Chlamydia|Girls 25+, boys at risk|Sexually active|
|Gonorrhea|At risk|Symptoms or high risk|
|HIV|All adolescents|Opt-out testing|
|HPV vaccine|11-12 years, through 26|Catch-up through 26|

---

## Common Errors to Avoid

1. **Missing critical congenital heart disease** — Pulse oximetry screening before discharge
2. **Underdosing medications** — Always use pediatric dosing, not adult scaled
3. **Ignoring growth parameters** — Plot all visits on growth chart
4. **Missing developmental delays** — Use standardized screening tools (M-CHAT, ASQ)
5. **Treating viral infections with antibiotics** — Most URIs are viral
6. **Not considering abuse** — Unexplained injuries warrant investigation
7. **Ignoring vaccination status** — Check at every visit
8. **Missing neonatal hypoglycemia** — Screen at-risk infants
9. **Inadequate fever workup** — Age-based approach is critical
10. **Not involving adolescents privately** — Confidential care improves disclosure

