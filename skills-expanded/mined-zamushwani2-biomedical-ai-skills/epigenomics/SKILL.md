# Epigenomics

ATAC-seq and ChIP-seq analysis for chromatin accessibility and transcription factor binding. Covers the filtering that precedes peak calling, ATAC-specific peak calling, differential binding and the DiffBind 3.x changes that silently alter results, motif enrichment, TF activity from accessibility, and assigning peaks to genes without pretending distance is regulation.

## When to Use This Skill

Activate when the user requests:
- ATAC-seq or ChIP-seq peak calling, or MACS
- Differential accessibility or differential binding
- Motif enrichment, TF footprinting, or chromVAR
- Assigning peaks to genes, or enhancer-promoter linking
- Integrating accessibility or binding with expression
- Chromatin QC: FRiP, TSS enrichment, fragment size distribution

## Inputs

| Data Type | Form | Note |
|-----------|------|------|
| Aligned reads | BAM, duplicates marked | ATAC needs chrM and blacklist removal first |
| Peaks | narrowPeak / broadPeak | narrow for TF and ATAC, broad for most histone marks |
| Sample sheet | CSV with condition, replicate, bamReads, peaks | DiffBind's entry point |
| Genome annotation | TxDb or GTF | for TSS enrichment and peak annotation |
| Motif database | JASPAR | version changes the answer |

---

## Environment

Versions verified 2026-08.

```bash
pip install MACS3          # 3.0.4  peak calling
pip install deeptools      # 3.5.6  coverage, matrices, QC plots
```

```r
BiocManager::install(c("DiffBind",     # 3.22.2  differential binding
                       "csaw",         # 1.46.0  window-based differential
                       "chromVAR",     # 1.34.1  TF activity from accessibility
                       "ChIPseeker",   # 1.48.0  peak annotation
                       "motifmatchr",  # 1.34.0  motif scanning
                       "TFBSTools",    # 1.50.0
                       "JASPAR2024",   # motif database
                       "rGREAT"))      # 2.14.0  regulatory region enrichment
```

```
Use MACS3 (3.0.4, released 2026-02), not MACS2. MACS2's last release was
2023-07 and development moved to MACS3, which is actively maintained. Most
tutorials still say macs2; the command is macs3 and the options differ in
places.

JASPAR2024 is the latest Bioconductor release; JASPAR2026 does not exist.
Record which JASPAR version you used, because motif matrices are revised
between releases and enrichment results move with them.
```

## Before Peak Calling

Peak calling is the step everyone photographs, and the filtering before it decides the result.

```
ATAC-seq, in order:
  1. Remove MITOCHONDRIAL reads. chrM is nucleosome-free and Tn5 cuts it
     freely, so it routinely takes 20-50% of an ATAC library and in bad
     preps far more. Leaving it in distorts library-size normalization for
     every downstream comparison.
  2. Remove ENCODE BLACKLIST regions. These are artefact-prone regions that
     pile up reads regardless of biology and will otherwise appear as
     confident peaks in every sample.
  3. Mark and remove duplicates. ATAC duplicate rates are high.
  4. Apply the Tn5 SHIFT: +4 on the plus strand, -5 on the minus strand.
     Tn5 inserts as a dimer spanning 9 bp, so the cut site is offset from
     the read start. Skipping this displaces every footprint by a few bases,
     which matters for motif and footprint analysis and not much for coarse
     peak calls.

ChIP-seq:
  Blacklist and duplicate removal apply equally. The input/control track is
  not optional for point-source factors; without it, open chromatin reads as
  binding.
```

```
QC that is worth the time, before any peak is trusted:
  FRiP              fraction of reads in peaks. Low FRiP means the
                    enrichment failed; the peaks are noise you can still
                    call and plot.
  TSS enrichment    ATAC libraries should show a sharp pileup at
                    transcription start sites. A flat profile is a failed
                    library, not a biological finding.
  Fragment sizes    ATAC shows a nucleosome-free peak below ~100 bp and
                    periodicity at multiples of ~200 bp. Absent periodicity
                    means over-digestion or degraded nuclei.
```

## Peak Calling

```bash
# ATAC: no model building, shift to cut sites, extend around them
macs3 callpeak -t sample.bam -f BAMPE -g hs -n sample \
  --nomodel --shift -100 --extsize 200 --keep-dup all -q 0.05

# ChIP, point-source TF, with input control
macs3 callpeak -t chip.bam -c input.bam -f BAM -g hs -n tf --q 0.05

# ChIP, broad histone mark
macs3 callpeak -t chip.bam -c input.bam -f BAM -g hs -n mark --broad
```

```
--nomodel for ATAC because MACS's model building estimates a fragment-size
shift from a paired peak model that assumes a point-source ChIP signal.
ATAC does not have that structure, so the estimated shift is meaningless.

--shift -100 --extsize 200 centres a 200 bp window on each cut site. This is
the cut-site convention; if you instead use BAMPE and let MACS use the real
fragments, do NOT also pass --shift, because you would be shifting fragments
that are already correctly placed. Pick one convention and say which.

--broad for histone marks that spread (H3K27me3, H3K36me3, H3K9me3). Calling
them narrow fragments one domain into many small peaks and inflates the peak
count without adding information. H3K4me3 and most TFs are narrow.
```

## Differential Binding: DiffBind 3.x Changed the Answers

This section exists because DiffBind's version 3 altered defaults in ways that change results without erroring.

```
Verified from the package's own NEWS:

1. dba.count() NOW CENTRES ON SUMMITS BY DEFAULT, giving 401 bp intervals.
   The previous default did not recentre. Every peak's width changes, so
   every count changes. To restore the old behaviour: summits = FALSE.

2. THE MODELLING DEFAULT CHANGED. The pre-3.0 methods are kept for backward
   compatibility but are no longer the default. To repeat an earlier
   analysis you must call dba.contrast(design = FALSE).

3. NORMALIZATION MOVED OUT OF dba.analyze(). The options bSubControl,
   bFullLibrarySize, filter and filterFun were removed from dba.analyze()
   and now live in the new dba.normalize(). Old scripts passing them to
   dba.analyze() silently lose those settings.

A script written for DiffBind 2.x therefore runs on 3.x and returns
different numbers. That is worse than an error. Pin the version, and if you
are reproducing published results, check which major version produced them.
```

```r
library(DiffBind)   # 3.22.2

dbo <- dba(sampleSheet = samples)
dbo <- dba.count(dbo, summits = 200)       # state the value; do not rely on the default
dbo <- dba.normalize(dbo, normalize = DBA_NORM_NATIVE)
dbo <- dba.contrast(dbo, design = ~Condition)
dbo <- dba.analyze(dbo)
res <- dba.report(dbo)
```

```
Two current issues in 3.22.x worth knowing:

bSubControl was not preserved. In versions before 3.22.2, a bSubControl set
in dba.count() was not carried onto the returned object, so a later
dba.normalize() (and therefore dba.analyze()) could silently fall back to
control subtraction based on whether a greylist existed. Fixed in 3.22.2.
If you are on an earlier 3.x, upgrade or set it explicitly at every step.

dba.plotProfile() is disabled. As of 3.22.1 it prints a notice and returns
NULL invisibly, because its backend (profileplyr) is not installable in
current Bioconductor. Use deeptools (computeMatrix / plotHeatmap) for
profile plots instead of waiting for it.
```

```
csaw is the alternative worth knowing: it tests windows across the genome
rather than a fixed peak set, which avoids the bias introduced when peaks
are called on the same data used for testing. Slower and less convenient,
more defensible when the peak set itself might differ between conditions.
```

## Motif Enrichment and TF Activity

```
Two different questions people conflate:

  "Which motifs are over-represented in my peaks?"
     -> motif enrichment against a background. The BACKGROUND choice is the
        analysis. GC-matched, accessibility-matched background sequences,
        not random genome, or GC-rich motifs win regardless of biology.

  "Which TFs change activity between my samples?"
     -> chromVAR. It computes per-sample deviations in accessibility over
        peaks containing each motif, corrected against background peak sets
        matched for GC content and average accessibility.

chromVAR gives TF-MOTIF activity, not TF activity. Family members sharing a
motif are indistinguishable: a strong "FOS/JUN" deviation does not say which
family member is active, and expression data is needed to narrow it.
```

```r
library(chromVAR); library(motifmatchr); library(JASPAR2024)

motifs   <- TFBSTools::getMatrixSet(JASPAR2024::JASPAR2024(),
                                    list(species = 9606, collection = "CORE"))
matches  <- matchMotifs(motifs, peaks, genome = BSgenome.Hsapiens.UCSC.hg38)
dev      <- computeDeviations(object = counts, annotations = matches)
```

```
Record the JASPAR release. Matrices are revised between releases, so
enrichment computed against JASPAR2020 and JASPAR2024 are not the same
analysis, and the difference is invisible in the output.
```

## Peaks to Genes

```
NEAREST GENE IS AN ASSUMPTION, NOT A RESULT.

Enhancers regularly skip over the nearest gene to act on one hundreds of
kilobases away, and a peak's nearest gene is frequently not its target.
Annotating peaks to nearest TSS is a reasonable first pass and a poor final
answer.

Better, in increasing order of evidence:
  nearest TSS               convenient, often wrong for distal peaks
  within a fixed window     no better, just wider
  correlation across samples accessibility-expression correlation over a
                            cohort; needs many samples
  chromatin conformation    Hi-C, HiChIP, Capture-C. The only direct
                            evidence of contact.

rGREAT takes a different approach, testing enrichment over regulatory
DOMAINS rather than assigning each peak to one gene, which sidesteps the
one-peak-one-gene assumption for pathway-level questions.

Say which method you used. A figure captioned "genes near differential
peaks" makes a much weaker claim than "genes contacted by differential
peaks", and only the second needs conformation data.
```

## Integrating With Expression

```
Accessibility and expression are correlated but far from equivalent. A
promoter can be open and the gene silent; a gene can be expressed with no
detectable accessibility change between your conditions.

Expect modest concordance and do not treat discordance as failure. The
informative cases are usually the discordant ones: accessible-but-silent
regions are poised or repressed by another mechanism.

When testing whether differential peaks explain differential expression,
the peak set and the expression set must come from the SAME samples, or at
minimum the same conditions with stated batch structure. Joining ATAC from
one study to RNA from another and reporting correlation measures study
differences as much as regulation.
```

## Output Specification

| Output | Format | Description |
|--------|--------|-------------|
| `peaks/` | narrowPeak / broadPeak | with the MACS3 command that produced them |
| `qc.csv` | CSV | FRiP, TSS enrichment, chrM fraction, duplicate rate per sample |
| `consensus_peaks.bed` | BED | with how the consensus was defined |
| `differential.csv` | CSV | DiffBind or csaw results, with `summits` and normalization recorded |
| `motif_enrichment.csv` | CSV | with the background definition and JASPAR version |
| `chromvar_deviations.csv` | CSV | labelled TF-motif, not TF |
| `peak_gene_links.csv` | CSV | with the linking method named |

## Validation Checks

```
Pre-peak
  chrM removed and its fraction reported.
  ENCODE blacklist applied.
  Duplicates marked and removed; rate reported.
  Tn5 shift applied for footprint-level work, and stated either way.
  FRiP and TSS enrichment computed before peaks are used.

Peak calling
  MACS3, not MACS2.
  --nomodel used for ATAC, with one shift convention, not two.
  --broad used for spreading histone marks, narrow for TFs and ATAC.
  Input control used for point-source ChIP.

Differential
  DiffBind version recorded; `summits` set explicitly rather than defaulted.
  Normalization set through dba.normalize(), not assumed.
  On DiffBind < 3.22.2, bSubControl set explicitly at every step.

Motif and linking
  Background is GC- and accessibility-matched, not random genome.
  JASPAR release recorded.
  chromVAR results labelled TF-motif rather than TF.
  Peak-to-gene method named; nearest-TSS not described as a target.
```

## Common Pitfalls

### Before peak calling
1. **Leaving mitochondrial reads in an ATAC library**: chrM is nucleosome-free and commonly takes 20–50% of reads, distorting library-size normalization for every comparison. Remove it and report the fraction.
2. **Skipping the ENCODE blacklist**: artefact regions pile up reads regardless of biology and appear as confident peaks in every sample.
3. **Omitting the Tn5 shift**: Tn5 inserts as a dimer spanning 9 bp, so cut sites sit +4/−5 from read starts. Footprint and motif positions are displaced without it.
4. **Reporting peaks without FRiP or TSS enrichment**: a failed library still yields peaks you can call and plot. A flat TSS profile is a failed experiment, not a finding.

### Peak calling
5. **Using `macs2`**: development moved to MACS3 (3.0.4); MACS2's last release was 2023.
6. **Letting MACS build a model for ATAC**: the paired-peak model assumes point-source ChIP structure that ATAC lacks, so the estimated shift is meaningless. Use `--nomodel`.
7. **Combining `BAMPE` with `--shift`**: paired-end fragments are already correctly placed. Shifting them again double-corrects. Choose the cut-site convention or the fragment convention.
8. **Calling broad histone marks as narrow**: H3K27me3 and H3K36me3 fragment into many small peaks, inflating peak counts without adding information.

### DiffBind
9. **Relying on `dba.count()` defaults across versions**: 3.x centres on summits by default (401 bp intervals) where earlier versions did not. Every count changes. Set `summits` explicitly.
10. **Reusing a DiffBind 2.x script on 3.x**: the modelling default changed, so reproducing an older analysis needs `dba.contrast(design = FALSE)`. The script runs either way and returns different numbers.
11. **Passing normalization options to `dba.analyze()`**: `bSubControl`, `bFullLibrarySize`, `filter` and `filterFun` moved to `dba.normalize()` in 3.0 and are silently lost otherwise.
12. **Running DiffBind below 3.22.2 with `bSubControl`**: it was not preserved from `dba.count()`, so analysis could silently fall back to control subtraction. Upgrade or set it at every step.
13. **Waiting on `dba.plotProfile()`**: it is disabled as of 3.22.1 and returns NULL invisibly because its backend is uninstallable. Use deeptools.

### Motif and linking
14. **Enriching motifs against a random-genome background**: GC-rich motifs win regardless of biology. Match background on GC and accessibility.
15. **Calling chromVAR output TF activity**: it is TF-*motif* activity, and family members sharing a motif are indistinguishable without expression data.
16. **Not recording the JASPAR release**: matrices are revised between releases, so the same peaks give different enrichment and the difference is invisible.
17. **Reporting nearest-TSS assignment as the target gene**: enhancers routinely skip the nearest gene. Only conformation data shows contact.

### Integration
18. **Treating accessibility–expression discordance as failure**: an accessible silent promoter is poised or otherwise repressed, and the discordant cases are usually the informative ones.
19. **Correlating ATAC from one study with RNA from another**: the correlation measures study differences as much as regulation. Use matched samples.

## Related Skills

- [`cancer-multiomics`](../cancer-multiomics/SKILL.md): the expression side of accessibility-expression integration, and methylation as a third layer
- [`multiomics-integration`](../multiomics-integration/SKILL.md): joint modelling when accessibility is one view among several
- [`single-cell-atlas`](../single-cell-atlas/SKILL.md): the single-cell counterpart, where accessibility is sparse per cell
- [`spatial-transcriptomics`](../spatial-transcriptomics/SKILL.md): shared discipline on QC that is local rather than global

## Public Datasets for Testing

| Dataset | Content | Access |
|---------|---------|--------|
| ENCODE | ATAC-seq and ChIP-seq across cell lines, uniformly processed | encodeproject.org, open |
| ENCODE blacklist | Artefact regions for hg38 and mm10 | Boyle-Lab/Blacklist, open |
| TCGA ATAC-seq | Pan-cancer chromatin accessibility | GDC, open |
| Roadmap Epigenomics | Histone marks across primary tissues | open |
| JASPAR2024 | Curated TF binding motifs | Bioconductor |
