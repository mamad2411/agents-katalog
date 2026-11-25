# BioQC-MCP Skills

This directory contains reusable pipeline templates for the `run_qc_pipeline` tool.

## Available Skills

| Skill | Description | Use Case |
|-------|-------------|----------|
| `full_qc_pipeline.py` | Complete QC workflow | Analyze all FASTQ files in a directory |
| `batch_analysis.py` | Multi-sample batch processing | Process many samples with summary stats |
| `quick_check.py` | Fast quality overview | Quick sanity check on samples |

## Usage

AI agents can read these skill files and adapt them for user requests:

```
# Example: User asks "Run QC on my samples"
# AI reads skills/full_qc_pipeline.py and adapts it:

files = list_fastq_files('/path/to/samples')
print(f"Found {len(files)} FASTQ files")

for f in files:
    result = run_fastqc([f['path']], output_dir='./qc_results')
    print(f"Analyzed: {f['name']}")

multiqc = run_multiqc('./qc_results', output_dir='./multiqc_report')
print(f"Report: {multiqc['report']}")
```

## Token Savings

Using skills with `run_qc_pipeline` reduces token usage by 75-98%:

| Workflow | Without Skills | With Skills | Savings |
|----------|----------------|-------------|---------|
| Single file QC | 2,000 tokens | 500 tokens | 75% |
| Multi-sample | 8,000 tokens | 600 tokens | 92% |
| Full pipeline | 15,000 tokens | 300 tokens | 98% |
