# Variant Annotation

Annotation and clinical interpretation of DNA variants in cancer. Covers VCF normalization and filtering, functional annotation with VEP, germline classification under ACMG/AMP, somatic classification under the AMP/ASCO/CAP tiers and the ClinGen/CGC/VICC oncogenicity standard, tumor mutational burden, microsatellite instability, and neoantigen prediction.

## When to Use This Skill

Activate when the user requests:
- VCF filtering, normalization, or merging
- Functional annotation (VEP, SnpEff, ANNOVAR)
- Germline variant classification (ACMG/AMP, pathogenic vs benign)
- Somatic variant classification (tiers, oncogenicity, actionability)
- Driver vs passenger discrimination
- OncoKB or CIViC evidence lookup
- Tumor mutational burden calculation
- Microsatellite instability estimation
- Neoantigen prediction or HLA binding
- Interpreting a variant of uncertain significance

## Inputs

| Data Type | Format | Source |
|-----------|--------|--------|
| Variant calls | VCF 4.2+, bgzipped and indexed | GATK, Mutect2, DeepVariant, Strelka2 |
| Reference genome | FASTA with `.fai` | GRCh38 (or GRCh37 for legacy cohorts) |
| Somatic MAF | Mutation Annotation Format | TCGA GDC, cBioPortal |
| Panel definition | BED | Assay manufacturer, for TMB denominators |
| HLA type | 4-digit alleles | OptiType, HLA-HD, arcasHLA |

---

## Environment

Versions verified 2026-08.

```
bcftools            1.24        VCF manipulation, normalization
Ensembl VEP         116.1       functional annotation, the current default
SnpEff              5.4c        alternative annotator
ANNOVAR             current     still distributed, registration required

Bioconductor
  VariantAnnotation 1.58.0      VCF parsing and coding consequences in R
  maftools          2.28.0      somatic MAF summarization, TMB, signatures

Neoantigens
  pVACtools         7.1.2       neoantigen pipeline (griffithlab)
  NetMHCpan         4.1+        MHC class I binding; academic licence
```

```
Microsatellite instability, and which tool is still alive:

  msisensor       ARCHIVED. ding-lab/msisensor was archived, last push 2021.
                  Do not start new work on it.
  msisensor-pro   v1.3.0 (2024-09). Current choice, tumor-only or paired.
  msisensor2      last push 2024-04. Tumor-only, no matched normal.
  MANTIS          paired tumor/normal, still used in clinical settings.

All four are read-based. MSI can also be inferred from a panel using
MSIsensor-pro's baseline mode, but the baseline must be built on the same
assay or the calls are not comparable.
```

---

## The Three Frameworks

This is the part that gets conflated, and conflating it produces reports that are wrong in a way reviewers notice.

```
GERMLINE PATHOGENICITY            ACMG/AMP 2015
  Question: does this inherited variant cause disease?
  Output:   Pathogenic / Likely pathogenic / VUS / Likely benign / Benign
  Applies:  germline findings only

SOMATIC ONCOGENICITY              ClinGen/CGC/VICC 2022 SOP
  Question: is this variant driving the cancer?
  Output:   Oncogenic / Likely oncogenic / VUS / Likely benign / Benign
  Applies:  somatic variants, biology only, no treatment implication

SOMATIC CLINICAL SIGNIFICANCE     AMP/ASCO/CAP 2017 tiers
  Question: does this variant change patient management?
  Output:   Tier I (strong) / II (potential) / III (unknown) / IV (benign)
  Applies:  somatic variants, actionability in a given tumour type
```

```
Oncogenicity and clinical significance are DIFFERENT AXES, not alternatives.

  A KRAS G12D is clearly oncogenic and may still be Tier III in a tumour type
  with no approved KRAS-directed option.

  A variant may be Tier I because it predicts resistance, without being a
  driver at all.

ClinGen's own guidance is that somatic expert panels should apply BOTH the
oncogenicity SOP and the AMP/ASCO/CAP guidelines, not choose between them.
Report both, and say which is which.

Never apply ACMG/AMP to a somatic variant. The criteria assume germline
inheritance, population frequency in gnomAD as evidence of benignity, and
segregation data. None of that transfers.
```

## VCF Processing

### Normalize before anything else

Un-normalized VCFs are the single largest source of silent annotation failure. The same variant can be written several ways, and a lookup against a knowledgebase misses every representation but one.

```bash
# Split multiallelic sites, left-align, and trim to the minimal representation
bcftools norm -m -any -f GRCh38.fa -Oz -o normalized.vcf.gz input.vcf.gz
bcftools index normalized.vcf.gz
```

```
What each part fixes:

  -m -any      splits multiallelic records into one ALT per line. A
               knowledgebase keyed on a single ALT never matches a
               multiallelic record.
  -f <ref>     left-aligns indels against the reference. AAT->AT and
               ATT->AT can describe the same deletion; only one is canonical.
  trimming     removes shared leading/trailing bases so the representation
               is minimal.

Skipping this does not raise an error. It produces annotations that are
simply absent, and absent looks like "not in the database".
```

### Filtering

```bash
# Keep PASS calls only, then apply depth and allele fraction thresholds
bcftools view -f PASS normalized.vcf.gz \
  | bcftools filter -i 'FORMAT/DP >= 20 && FORMAT/AF >= 0.05' -Oz -o filtered.vcf.gz
```

```
Thresholds are assay-dependent, not universal:

  Germline, WGS/WES     DP >= 10-20, AF >= 0.25 for het calls
  Somatic, tumour-only  DP >= 50, AF >= 0.05, and a panel of normals
  Somatic, deep panel   DP >= 500, AF >= 0.01 possible; below 0.05 needs UMIs
  ctDNA                 AF >= 0.001 with UMI consensus, otherwise noise

Tumour-only calling without a matched normal cannot separate somatic from
germline. Expect 30-60% of calls to be germline unless you filter against
gnomAD and a panel of normals, and say in the report that you did so.
```

### Reference genome

```
GRCh37 and GRCh38 coordinates are NOT interchangeable. A position annotated
against the wrong build silently lands in a different gene.

Check the VCF header contig lines before annotating. If the source is TCGA
legacy data it is GRCh37; current GDC releases are GRCh38.

Chromosome naming also differs: "1" (Ensembl) vs "chr1" (UCSC/GDC). A build
mismatch usually errors; a naming mismatch often just returns nothing.
```

## Functional Annotation

### VEP

```bash
vep --input_file filtered.vcf.gz --output_file annotated.vcf \
    --vcf --cache --offline --assembly GRCh38 \
    --everything \
    --pick_allele_gene \
    --fasta GRCh38.fa \
    --plugin dbNSFP,dbNSFP.gz,SIFT_score,Polyphen2_HDIV_score,REVEL_score,CADD_phred \
    --plugin SpliceAI,snv=spliceai_snv.vcf.gz,indel=spliceai_indel.vcf.gz
```

```
The transcript choice is a scientific decision, not a formatting one.

  (no flag)          one line per transcript. Complete, but a variant can
                     appear 30 times with different consequences.
  --pick             ONE consequence per variant, chosen by VEP's ordering.
                     Convenient and lossy.
  --pick_allele_gene one per allele per gene. Usually the right default for
                     clinical reporting.
  --flag_pick        annotates everything but marks the picked one. Best when
                     you want the full picture and a canonical choice.

Reporting "the" consequence of a variant without stating the transcript is
ambiguous. MANE Select is the current convention for a canonical human
transcript; state which transcript the report used.
```

### Choosing an annotator

```
VEP        Ensembl, release 116.1, updated with each Ensembl release.
           Richest plugin ecosystem (dbNSFP, SpliceAI, LoFtee, AlphaMissense).
           Default choice.

SnpEff     5.4c. Fast, self-contained, easy to run on non-model organisms.
           Fewer clinical plugins.

ANNOVAR    Still distributed and widely cited. Registration required, and
           its database bundles are updated on their own schedule rather
           than with a genome release. Check the date on any -operation
           database you use.
```

## Germline Classification

ACMG/AMP 2015 remains the framework. ClinGen has not replaced it; it publishes criterion-level refinements that supersede the original wording.

```
Evidence strength combines into a classification:

  Pathogenic       1 Very strong + >=1 Strong, or other documented combinations
  Likely path.     combinations one step weaker
  VUS              insufficient or conflicting evidence
  Likely benign / Benign   BA1, BS, BP criteria

Refinements to apply, from ClinGen (current as of the July 2025 guidance page):

  PM2      absence/rarity recalibrated to SUPPORTING strength, not moderate
  PS2/PM6  de novo criteria, with a points table by phenotype specificity
  PM3      in trans observations, scaled by how well the second variant is
           classified
  BA1      has an exception list; some variants exceed 5% and are still
           pathogenic in specific populations
  splicing recommendations updated March 2024
  gnomAD   v4-specific guidance issued March 2024

A points-based formulation (Tavtigian et al.) is ENDORSED by ClinGen, not
mandated. Using it is defensible; claiming it is the official replacement
for the 2015 rules is not.
```

```
Population frequency, done correctly:

  Use the popmax (grpmax) filtering allele frequency, not the global AF.
  A variant at 0.1% globally can be 4% in one ancestry group, which is
  strong evidence of benignity that a global AF hides.

  gnomAD v4 separates exomes and genomes; check which subset supports the
  count, and check the allele NUMBER. A frequency computed from 4 alleles
  is not evidence.
```

## Somatic Classification

### Oncogenicity: is it a driver?

```
ClinGen/CGC/VICC 2022 SOP. Evidence weighted very strong / strong /
moderate / supporting, in the spirit of ACMG/AMP but with cancer-specific
criteria and a points-based sum.

Signals that carry weight:
  Null variant in a bona fide TUMOUR SUPPRESSOR       strong
  Well-established hotspot in an ONCOGENE             strong
  Functional data showing gain or loss of function    strong to moderate
  Recurrence across independent tumours (COSMIC)      moderate
  Computational prediction alone                      supporting at best

The gene's mechanism decides which criteria apply. A truncating variant is
strong evidence in a tumour suppressor and usually irrelevant in an oncogene.
Applying tumour-suppressor logic to an oncogene is the most common error here.
```

### Clinical significance: does it change management?

```
AMP/ASCO/CAP 2017 tiers, always tumour-type specific:

  Tier I    Strong clinical significance
            IA: FDA-approved therapy or professional guideline, THIS tumour type
            IB: well-powered studies with consensus
  Tier II   Potential clinical significance
            IIC: approved for a DIFFERENT tumour type, or in trial eligibility
            IID: plausible from smaller studies
  Tier III  Unknown clinical significance
  Tier IV   Benign or likely benign

BRAF V600E is Tier IA in melanoma and Tier IIC in colorectal cancer, where
single-agent BRAF inhibition fails because of EGFR feedback. Same variant,
same oncogenicity, different tier. Tier assignment without naming the tumour
type is meaningless.
```

### Knowledgebases

```bash
# OncoKB: therapeutic levels of evidence, requires a free academic token
curl -H "Authorization: Bearer $ONCOKB_TOKEN" \
  "https://www.oncokb.org/api/v1/annotate/mutations/byGenomicChange?genomicLocation=7,140453136,140453136,A,T"

# CIViC: open, no token
curl "https://civicdb.org/api/variants?count=1&name=V600E"
```

```
OncoKB levels are not AMP tiers, though they map roughly:
  Level 1  FDA-recognized biomarker for an approved drug, this indication
  Level 2  standard care biomarker per guidelines
  Level 3A clinical evidence in this indication
  Level 3B clinical evidence in a different indication
  Level 4  compelling biological evidence
  R1/R2    resistance

Both databases are curated snapshots. Record the version or access date in
the report, because a Tier III today can become Tier I after an approval.
```

## Tumour Mutational Burden

```
TMB = eligible somatic mutations / eligible megabases of the panel.

Every term is assay-specific, which is why panel TMB values are not
comparable across assays without harmonization:

  numerator    Are synonymous variants counted? FMI counts them; many
               pipelines do not. Including them raises TMB by roughly 20-30%.
               Are indels counted? Are hotspots removed?
  denominator  The callable territory of THAT panel, not the panel's
               nominal size.
  germline     Tumour-only assays must filter germline variants; the method
               used changes the count materially.

The Friends of Cancer Research TMB Harmonization Project exists precisely
because panel TMB did not agree across vendors. A "TMB-high" call is only
interpretable alongside the assay and its cutoff.
```

```r
library(maftools)   # v2.28.0

maf <- read.maf("cohort.maf")
tmb_res <- tmb(maf, captureSize = 50, logScale = TRUE)
# captureSize is the panel's callable Mb. The default is NOT your panel.
# Passing the wrong captureSize scales every TMB value linearly.
```

The FDA approval for pembrolizumab in TMB-high solid tumours uses **≥10 mutations/Mb as measured by FoundationOne CDx**. That threshold is tied to that assay. Applying 10 mut/Mb to a different panel, or to WES, is an extrapolation and should be stated as one.

## Microsatellite Instability

```bash
# msisensor-pro, paired tumour/normal
msisensor-pro msi -d microsatellites.list -n normal.bam -t tumor.bam -o msi_out

# tumour-only requires a baseline built from normals ON THE SAME ASSAY
msisensor-pro baseline -d microsatellites.list -i normal_configure.txt -o baseline_dir
msisensor-pro pro -d baseline_dir/*.baseline -t tumor.bam -o msi_out
```

```
Interpretation:
  MSI-H     typically >= 20% of evaluated microsatellite loci unstable
  MSS       stable

The 20% cutoff is convention, not a law, and depends on the locus panel.
Report the number of loci evaluated alongside the percentage: a 20% call
from 15 informative loci is not the same evidence as 20% from 2000.

MSI-H, dMMR by IHC, and high TMB overlap but are not interchangeable. A
tumour can be MSI-H with unremarkable TMB and vice versa. If a therapy
decision rests on it, confirm with an orthogonal assay.
```

## Neoantigen Prediction

```bash
pvacseq run annotated.vcf SAMPLE \
  HLA-A*02:01,HLA-B*07:02,HLA-C*07:02 \
  MHCflurry NetMHCpan BigMHC_EL \
  output_dir/ \
  --binding-threshold 500 --iedb-install-directory /path/to/iedb
```

```
What binding prediction does and does not tell you:

  Predicts    peptide-MHC binding affinity, and increasingly presentation
              likelihood (eluted-ligand models beat affinity-only models)
  Does NOT    predict immunogenicity. Most predicted binders elicit no T cell
              response. Validation rates in the literature are low single
              digits to low tens of percent.

Requirements that are easy to get wrong:
  HLA typing must be 4-digit and from the patient, not imputed
  Expression matters: a neoantigen from an unexpressed transcript is not a
  neoantigen. Filter on tumour RNA-seq.
  Variant allele fraction matters: subclonal neoantigens are weaker targets
  Run several predictors and use the consensus, not one tool's top hit
```

Treat the output as a ranked hypothesis list for experimental testing, in the same way in-silico perturbation output is treated in `foundation-models`.

## Output Specification

| Output | Format | Description |
|--------|--------|-------------|
| `normalized.vcf.gz` | VCF | Left-aligned, multiallelics split, indexed |
| `annotated.vcf` | VCF | VEP consequences, one per allele per gene |
| `variants.maf` | MAF | Somatic calls in MAF format for cohort tools |
| `germline_classification.csv` | CSV | Variant, ACMG criteria applied, final class |
| `somatic_oncogenicity.csv` | CSV | Variant, ClinGen/CGC/VICC criteria, oncogenicity |
| `somatic_tiers.csv` | CSV | Variant, AMP tier, tumour type, evidence source |
| `tmb.csv` | CSV | Sample, count, callable Mb, TMB, assay name, cutoff used |
| `msi.csv` | CSV | Sample, loci evaluated, unstable loci, percentage, call |
| `neoantigens.tsv` | TSV | Peptide, HLA allele, predicted affinity, expression, VAF |
| `knowledgebase_versions.txt` | Text | OncoKB and CIViC access dates, VEP cache version |

## Validation Checks

```
VCF integrity
  Reference build recorded and matches the annotation source.
  Chromosome naming consistent between VCF, reference, and cache.
  Normalization applied: no multiallelic records remain, indels left-aligned.
  Records before and after normalization counted; splitting increases the count.

Annotation
  Fraction of variants receiving any consequence is near 1. A low rate
  usually means a build or naming mismatch, not a rare cohort.
  Transcript selection flag recorded, and the transcript reported per variant.
  Known positive controls annotate as expected: BRAF V600E as missense,
  TP53 R175H as missense, a known nonsense as stop_gained.

Germline classification
  Population frequency uses popmax with the allele number reported.
  Criteria applied are listed per variant, not just the final class.
  PM2 applied at supporting strength, per current ClinGen guidance.

Somatic classification
  Oncogenicity and clinical tier reported SEPARATELY.
  Tier assignment names the tumour type.
  Knowledgebase access date recorded.
  ACMG/AMP criteria not applied to somatic variants.

TMB
  Numerator rule stated: synonymous included or excluded, indels counted.
  Denominator is the callable Mb of the actual assay.
  Cutoff cited with the assay it was validated on.

MSI
  Loci evaluated reported alongside the unstable percentage.
  Tumour-only calls state which baseline was used.

Neoantigens
  Expression filter applied from matched RNA-seq.
  HLA type is patient-derived and 4-digit.
  Consensus across predictors reported, not a single tool's ranking.
```

## Common Pitfalls

### VCF handling
1. **Annotating without normalizing**: multiallelic and non-left-aligned records fail knowledgebase lookups silently. The variant appears absent from the database rather than raising an error. Run `bcftools norm -m -any -f ref` first, always.
2. **Build mismatch**: GRCh37 coordinates annotated against GRCh38 land in a different gene. Read the VCF header contigs before annotating, and note that TCGA legacy data is GRCh37 while current GDC is GRCh38.
3. **Chromosome naming mismatch**: `1` versus `chr1` typically returns no annotations rather than erroring, which reads as a rare cohort instead of a bug.
4. **Tumour-only calling reported as somatic**: without a matched normal, a large fraction of calls are germline. Filter against gnomAD and a panel of normals, and state that the calls are inferred somatic.

### Annotation
5. **Reporting a consequence without the transcript**: a variant can be missense in one transcript and intronic in another. Name the transcript, and prefer MANE Select as the canonical choice.
6. **Using `--pick` and treating the result as complete**: it collapses to one consequence by VEP's internal ordering. For clinical reporting use `--pick_allele_gene`, or `--flag_pick` to keep everything.
7. **Trusting an ANNOVAR database bundle without checking its date**: those databases update on their own schedule, not with the genome release.

### Classification
8. **Applying ACMG/AMP to somatic variants**: the criteria assume germline inheritance, segregation, and population frequency as benign evidence. Use the ClinGen/CGC/VICC oncogenicity SOP and the AMP/ASCO/CAP tiers instead.
9. **Treating oncogenicity and clinical significance as one axis**: a clearly oncogenic variant can be Tier III where nothing acts on it, and a Tier I variant may not be a driver at all. Report both.
10. **Assigning a tier without naming the tumour type**: BRAF V600E is Tier IA in melanoma and Tier IIC in colorectal cancer. The tier is a property of the variant *in a context*.
11. **Applying tumour-suppressor logic to an oncogene**: a truncating variant is strong evidence of oncogenicity in a tumour suppressor and generally uninformative in an oncogene. The gene's mechanism selects the criteria.
12. **Using global allele frequency instead of popmax**: a variant at 0.1% globally may be 4% in one ancestry group. Global AF hides the evidence of benignity, and it is how VUS accumulate disproportionately in under-represented populations.
13. **Applying PM2 at moderate strength**: ClinGen recalibrated absence/rarity to supporting. Using the 2015 wording overweights it.
14. **Citing the points-based system as the official replacement for ACMG/AMP 2015**: it is endorsed by ClinGen, not mandated. The 2015 framework with ClinGen's criterion-level refinements is the current standard.

### TMB and MSI
15. **Comparing TMB across assays**: numerator rules, denominators, and germline filtering all differ by vendor. The Friends of Cancer Research harmonization effort exists because they disagreed.
16. **Applying the 10 mut/Mb cutoff to any assay**: that threshold was validated on FoundationOne CDx. Using it for WES or another panel is an extrapolation and must be labelled as one.
17. **Passing the default `captureSize` to `maftools::tmb()`**: it scales every value linearly. Pass the callable megabases of the actual panel.
18. **Reporting an MSI percentage without the locus count**: 20% of 15 loci and 20% of 2000 loci are not the same evidence.
19. **Treating MSI-H, dMMR and TMB-high as interchangeable**: they overlap and disagree often enough to matter for a therapy decision.
20. **Starting new work on `msisensor`**: the original ding-lab repository is archived. Use msisensor-pro or msisensor2.

### Neoantigens
21. **Reading binding affinity as immunogenicity**: most predicted binders provoke no T cell response. Validation rates are low.
22. **Predicting neoantigens from unexpressed transcripts**: filter on matched tumour RNA-seq, or the peptide is never presented.
23. **Using imputed rather than patient HLA types**: HLA is the most polymorphic region in the genome. Type it from the patient's own data at 4-digit resolution.

## Related Skills

- [`cancer-multiomics`](../cancer-multiomics/SKILL.md): MAF-level cohort summarization, mutational signatures, driver detection
- [`survival-analysis`](../survival-analysis/SKILL.md): testing whether a classified variant or TMB stratum is prognostic
- [`foundation-models`](../foundation-models/SKILL.md): the same hypothesis-ranking caveat applies to in-silico predictions

## Public Datasets for Testing

| Dataset | Content | Use Case |
|---------|---------|----------|
| TCGA-LUAD (GDC) | Somatic MAF, GRCh38 | TMB distribution, driver frequencies |
| TCGA-UCEC | Somatic MAF | MSI-H enriched, TMB-high tail |
| GIAB HG002 | Germline truth set VCF | Normalization and annotation correctness |
| ClinVar VCF | Classified germline variants | ACMG classification benchmarking |
| COSMIC Cancer Mutation Census | Curated somatic variants | Oncogenicity evidence |
| CIViC (open API) | Curated clinical evidence | Tier assignment testing |
