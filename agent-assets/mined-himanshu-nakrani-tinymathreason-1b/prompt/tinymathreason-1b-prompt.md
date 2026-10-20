You are a senior ML engineer and LLM researcher with deep experience in
pretraining, post-training, and deploying language models. You have shipped
models at scale on TPU v4 clusters using JAX/MaxText and on GPUs using
PyTorch/TRL/Axolotl. You write clean, production-grade, well-documented code.

I am building a portfolio project called:

  "TinyMathReason-1B: A 1 Billion Parameter Mathematical Reasoning LLM
   Built from Scratch on TPU v4-32"

My goal is LEARNING + PORTFOLIO (not SOTA). I want to deeply understand the
entire LLM stack: tokenizer → architecture → pretraining → SFT → DPO/GRPO →
evaluation → release. The final model does not need to beat any benchmark
record — it needs to clearly demonstrate mathematical reasoning improvement
across training stages, and the project must be professionally documented.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROJECT SPEC:

Model:
  - ~1.1B parameter Llama-style decoder-only transformer
  - Architecture: RMSNorm, RoPE, SwiGLU, Grouped Query Attention (GQA)
  - Target config (adjust if needed to hit ~1.1B total params):
      hidden_dim: 2048
      num_layers: 22
      num_attention_heads: 16
      num_kv_heads: 4 (GQA, 4:1 ratio)
      intermediate_dim: 5632 (SwiGLU)
      vocab_size: 32,000
      max_seq_len: 4096
  - Precision: bfloat16 throughout
  - This is essentially the TinyLlama architecture — battle-tested

Pretraining (from scratch):
  - Train from randomly initialized weights on ~250B–350B tokens
  - Data mix (by token count):
      - FineWeb-Edu (general high-quality text): ~40% (~100B–140B tokens)
      - OpenWebMath (mathematical web text): ~35% (~87B–122B tokens)
      - Proof-Pile-2 subset (proofs, textbooks, papers): ~15% (~37B–52B tokens)
      - Stack-Edu subset (code — helps reasoning): ~10% (~25B–35B tokens)
  - Framework: MaxText on TPU v4-32 (JAX). This is the primary framework.
  - Sequence length: 4096 (packed documents with document separators)
  - Optimizer: AdamW (β1=0.9, β2=0.95, weight_decay=0.1)
  - LR schedule: linear warmup (2000 steps) + cosine decay to 0.1× peak LR
  - Peak learning rate: 3e-4 (standard for 1B models)
  - Global batch size: target ~4M tokens per step (1024 sequences × 4096 tokens)
  - Gradient clipping: 1.0
  - Checkpointing: save full checkpoint to GCS every 2 hours AND every
    5000 steps (whichever comes first). This is critical because the TPU
    is a spot instance and can be preempted at any time.
  - Expected throughput: ~2,500–4,000 tokens/sec/chip (will measure in
    smoke test)
  - Expected total training time: ~12–14 days (with spot preemptions)

Post-Training Stage 1 — Supervised Fine-Tuning (SFT):
  - Datasets:
      - MathInstruct (260k chain-of-thought math examples)
      - MetaMathQA (395k augmented math QA with reasoning)
      - GSM8K training split (7.5k grade school math with solutions)
      - NuminaMath-CoT (if available — high quality competition math)
  - Combined: ~600k–700k instruction examples
  - Format: ChatML or Llama chat template
      <|im_start|>system
      You are a mathematical reasoning assistant. Solve problems
      step by step, showing all work clearly.
      <|im_end|>
      <|im_start|>user
      {problem}
      <|im_end|>
      <|im_start|>assistant
      {detailed chain-of-thought solution}
      <|im_end|>
  - Framework: TRL SFTTrainer (PyTorch)
  - Run on: GPU (Thunder Compute $20 or Modal $30)
  - Hyperparameters:
      - Learning rate: 2e-5
      - Epochs: 2–3
      - Batch size: 32–64
      - Warmup ratio: 0.05
      - Cosine LR schedule

Post-Training Stage 2 — Preference Optimization:
  - Method: DPO (Direct Preference Optimization) as primary method.
    If time permits, also try GRPO (Group Relative Policy Optimization,
    the DeepSeek-R1 method) — this is a bonus that looks excellent on
    portfolio.
  - Preference data generation strategy:
      1. Take 10k–20k math problems from GSM8K + MATH + MathInstruct
      2. Generate 4–8 candidate solutions per problem using the SFT model
         (temperature sampling)
      3. Score each solution: correct final answer = chosen, wrong = rejected
      4. This gives ~10k–20k (chosen, rejected) pairs
  - Framework: TRL DPOTrainer (PyTorch)
  - Run on: GPU (Modal $30)
  - Hyperparameters:
      - Learning rate: 5e-7
      - β (DPO): 0.1
      - Epochs: 1–2
      - Batch size: 16–32

Evaluation:
  - Benchmarks (run at EVERY stage — base, after SFT, after DPO):
      - GSM8K (0-shot and 8-shot, maj@1)
      - MATH (4-shot)
      - ARC-Easy (0-shot)
      - ARC-Challenge (25-shot)
      - HellaSwag (10-shot) — to check general capability
      - MMLU (5-shot) — to check general knowledge
  - Tool: lm-evaluation-harness (EleutherAI)
  - Custom evaluation:
      - 30 hand-curated math problems (10 easy, 10 medium, 10 hard)
      - Side-by-side comparison with TinyLlama-1.1B (same parameter count)
      - Side-by-side comparison with Qwen2.5-0.5B and Qwen2.5-1.5B
  - Qualitative analysis:
      - Show 20 examples of model reasoning (before/after each stage)
      - Analyze failure modes
      - Analyze reasoning chain quality

Infra & Resources (hard constraints — optimize within these):
  - GCP TPU v4-32 spot cluster: 3 weeks total
      - 32 TPU v4 chips, 16 TPU v4 cores
      - Spot instance (can be preempted — must handle gracefully)
      - Region: us-central2-b (or wherever allocated)
      - Storage: GCS bucket in same region
  - Vultr $250 credit (EXPIRES IN 10 DAYS — must use immediately):
      - Use for: CPU-heavy data processing, tokenizer training,
        dataset downloading, cleaning, tokenization, sharding
      - Recommended: c2-standard-30 or similar large CPU instances
  - Thunder Compute $20 credit:
      - Use for: SFT training, small debugging runs, checkpoint
        conversion testing
  - Lightning AI $10 credit:
      - Use for: experiment tracking notebooks, W&B integration,
        visualization, small tests
  - Modal $30 credit:
      - Use for: DPO/GRPO training, batch evaluation runs, preference
        data generation, Gradio demo hosting

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DELIVERABLES I NEED FROM YOU (provide ALL of these in full):

1. ARCHITECTURE DESIGN
   - Exact model config with all hyperparameters
   - Layer-by-layer parameter count calculation proving total is ~1.1B
   - Comparison table with TinyLlama-1.1B, SmolLM2-1.7B, Qwen2.5-0.5B,
     Qwen2.5-1.5B, Llama-3.2-1B (architecture configs side by side)
   - Justify every architecture choice (why GQA 4:1, why 22 layers,
     why 5632 intermediate dim, etc.)
   - PyTorch model definition code (complete nn.Module implementation)
     that I can use for understanding even though training uses MaxText

2. TOKENIZER TRAINING
   - Complete Python script to train a 32k vocab BPE tokenizer using
     the `tokenizers` library (HuggingFace) or `sentencepiece`
   - Data sampling strategy: which subset of which dataset to use for
     tokenizer training (recommend ~10–50GB of text)
   - Special tokens: BOS, EOS, PAD, UNK, and any chat-specific tokens
     needed for later SFT (e.g., <|im_start|>, <|im_end|>)
   - Script to test tokenizer quality:
       - Compression ratio on math text vs general text
       - Fertility (tokens per word) on English, math, code
       - Encode-decode roundtrip test
       - Comparison with Llama/Qwen tokenizers on sample texts
   - Script to convert tokenizer to format needed by MaxText

3. DATA PROCESSING PIPELINE
   - Complete Python scripts for each step:
     a. download_datasets.py
        - Downloads FineWeb-Edu, OpenWebMath, Proof-Pile-2, Stack-Edu
          from HuggingFace Hub
        - Handles streaming for large datasets
        - Saves raw data to disk in efficient format
     b. clean_and_filter.py
        - Text cleaning (unicode normalization, whitespace, etc.)
        - Quality filtering (perplexity, length, dedup)
        - Language detection (keep English only for simplicity)
        - Remove near-duplicates (MinHash + LSH using datasketch)
     c. mix_datasets.py
        - Implements the 40/35/15/10 ratio
        - Interleaves datasets properly
        - Outputs combined stream
     d. tokenize_and_pack.py
        - Tokenizes with our custom tokenizer
        - Packs multiple documents into 4096-token sequences
        - Adds document separator tokens
        - Handles padding for final sequences
     e. create_shards.py
        - Creates sharded .array_record files (MaxText native format)
          OR .jsonl.zst OR .tfrecord — whichever MaxText needs
        - Each shard: ~100MB–500MB
        - Creates manifest/index file
     f. upload_to_gcs.py
        - Uploads all shards to GCS bucket
        - Verifies upload integrity (checksums)
        - Prints final stats (total tokens, total shards, total size)
   - Makefile or shell script that runs the entire pipeline end-to-end
   - Exact Vultr instance setup commands (OS, packages, disk, etc.)
   - Cost estimate for Vultr usage

4. PRETRAINING CONFIG & SCRIPTS
   - OPTION A (PRIMARY): MaxText on TPU v4-32
     - Step-by-step instructions to:
       1. Set up TPU v4-32 VM
       2. Clone and install MaxText
       3. Configure model architecture (map our 1.1B config to MaxText
          config format)
       4. Configure data loading from GCS
       5. Configure optimizer, LR schedule, checkpointing
     - Complete MaxText config file (YAML or Python — whatever MaxText
       uses). Every field filled in. No placeholders.
     - Exact launch command to start training
     - Exact command to resume from checkpoint after spot preemption
     - Script to monitor training (parse logs, plot loss curves)
     - Script to handle spot preemption automatically (detect preemption,
       wait, restart)
     - W&B integration setup
     - Expected training metrics:
       - Tokens per second per chip
       - Steps per hour
       - Total steps needed for 300B tokens
       - Total estimated wall-clock time
   - OPTION B (ALTERNATIVE): Brief note on how to do the same with
     Nanotron or torchtitan (just config, not full scripts)

5. CHECKPOINT CONVERSION
   - Complete script: convert_checkpoint.py
     - Converts MaxText checkpoint → HuggingFace format
     - Loads into a standard HuggingFace model class
     - Verifies conversion by running inference on 10 test prompts
     - Saves in safetensors format
   - This is critical because SFT/DPO will use HuggingFace/TRL

6. SFT TRAINING CODE
   - Complete Python script: train_sft.py
     - Loads HuggingFace checkpoint from step 5
     - Loads and combines MathInstruct + MetaMathQA + GSM8K train
     - Applies chat template (ChatML format)
     - Uses TRL SFTTrainer with proper config
     - Supports DeepSpeed ZeRO-2 for memory efficiency on single GPU
     - Saves final model + tokenizer
     - Logs to W&B
   - Data preparation script: prepare_sft_data.py
     - Downloads all SFT datasets
     - Converts to unified format
     - Applies chat template
     - Splits into train/val (99/1)
     - Saves as HuggingFace Dataset
   - Exact commands to run on Thunder Compute
   - Hyperparameter config file (separate YAML)

7. DPO / GRPO TRAINING CODE
   - Script: generate_preferences.py
     - Loads SFT model
     - Takes math problems as input
     - Generates N candidate solutions per problem (temperature=0.7–1.0)
     - Scores solutions by checking final answer correctness
     - Creates (prompt, chosen, rejected) dataset
     - Saves as HuggingFace Dataset
   - Script: train_dpo.py
     - Loads SFT model as both policy and reference
     - Trains DPO using TRL DPOTrainer
     - Logs to W&B
     - Saves final model
   - Script: train_grpo.py (BONUS — if time permits)
     - Implements simplified GRPO loop
     - Uses reward = correctness of final answer
     - This is the DeepSeek-R1 approach
   - Exact commands to run on Modal (including Modal app definition
     if using Modal's serverless GPU)

8. EVALUATION SUITE
   - Script: run_benchmarks.py
     - Wraps lm-evaluation-harness
     - Runs all benchmarks: GSM8K, MATH, ARC-E, ARC-C, HellaSwag, MMLU
     - Outputs clean JSON + markdown table
     - Supports running on any checkpoint (base, SFT, DPO)
   - Script: run_custom_eval.py
     - 30 hand-curated math problems (include the actual problems in
       the script)
     - Generates model outputs
     - Formats as markdown comparison table
   - Script: generate_comparison.py
     - Runs same prompts on:
       - Our base model (after pretraining)
       - Our SFT model
       - Our DPO model
       - TinyLlama-1.1B (from HuggingFace)
       - Qwen2.5-0.5B (from HuggingFace)
     - Outputs side-by-side comparison markdown
   - Script: plot_training_curves.py
     - Reads W&B logs or training logs
     - Plots: loss curve, learning rate, throughput, eval metrics
     - Saves publication-quality figures (matplotlib/seaborn)

9. GITHUB REPO STRUCTURE
   - Exact folder and file tree with EVERY file listed
   - Complete README.md (full content, not placeholder) including:
     - Project title and badge icons
     - One-paragraph summary
     - Architecture diagram (ASCII or description for later diagram)
     - Results table
     - Quick start guide
     - Full training reproduction guide
     - Dataset description
     - Hardware requirements
     - Citation format
     - License
     - Acknowledgments
   - .gitignore (comprehensive for Python + ML + data)
   - LICENSE (Apache 2.0)
   - requirements/ folder with separate files:
     - requirements-data.txt (data processing)
     - requirements-train.txt (MaxText/JAX)
     - requirements-sft.txt (TRL/PyTorch)
     - requirements-eval.txt (lm-evaluation-harness)
   - Makefile with targets for every major step

10. HUGGINGFACE MODEL CARD
    - Complete model card in markdown format
    - All sections filled in:
      - Model description
      - Training data and mix ratios
      - Training procedure and hyperparameters
      - Hardware used
      - Evaluation results (template with placeholder numbers)
      - Intended uses and limitations
      - Ethical considerations
      - Environmental impact (estimated CO2)
      - Citation
    - Include separate cards for: base model, SFT model, DPO model

11. TRAINING REPORT TEMPLATE
    - Complete outline for a 15-page PDF training report
    - For each section, provide:
      - What to write (2–3 sentence description)
      - What figures/tables to include
      - What analysis to perform
    - Sections:
      1. Abstract
      2. Introduction & Motivation
         - Why train from scratch vs fine-tune
         - Why mathematical reasoning
         - Learning objectives
      3. Related Work
         - TinyLlama, SmolLM2, DeepSeek-Math, Qwen2.5-Math
      4. Architecture Design
         - Config table
         - Design decisions and justifications
      5. Data Curation
         - Source descriptions
         - Cleaning pipeline
         - Mix ratios and justification
         - Data statistics (token counts, document lengths, etc.)
      6. Tokenizer
         - Training procedure
         - Quality analysis
         - Comparison with existing tokenizers
      7. Pretraining
         - Setup and hyperparameters
         - Loss curves and analysis
         - Throughput measurements
         - Spot preemption handling
         - Intermediate evaluation checkpoints
      8. Post-Training: SFT
         - Data and format
         - Training details
         - Impact on reasoning quality
      9. Post-Training: DPO/GRPO
         - Preference data generation
         - Training details
         - Impact analysis
      10. Evaluation Results
          - Benchmark tables (base vs SFT vs DPO)
          - Comparison with TinyLlama, Qwen2.5
          - Qualitative examples (10 best, 5 failures)
      11. Ablation Studies
          - Effect of data mix ratio
          - Effect of training tokens
          - SFT vs SFT+DPO
      12. Lessons Learned
          - What worked, what didn't
          - What I would do differently
          - TPU training tips
      13. Limitations & Future Work
      14. Conclusion
      15. References
    - Suggest specific LaTeX template (NeurIPS or simple academic style)

12. BLOG POST OUTLINE
    - Structure for a technical blog post titled:
      "How I Built a 1B Mathematical Reasoning LLM from Scratch
       on a TPU v4-32 Cluster in 3 Weeks"
    - Include:
      - Hook/intro paragraph (draft it)
      - Section breakdown with key points per section
      - What screenshots/figures to include
      - Call to action (link to model, GitHub, report)
      - SEO-friendly structure
    - Target: 2000–3000 word post

13. DAY-BY-DAY EXECUTION PLAN
    - Detailed 23-day schedule in table format
    - For each day:
      - What tasks to complete
      - Which resource to use (TPU / Vultr / Thunder / Modal / Lightning)
      - Expected deliverable by end of day
      - Estimated cost spent that day
    - Include milestones:
      - Day 1: Project setup complete
      - Day 3: Tokenizer trained and tested
      - Day 5: All data processed and on GCS
      - Day 7: Smoke test on TPU passes (1000 steps, loss decreasing)
      - Day 8: Main pretraining begins
      - Day 14: 150B+ tokens trained, intermediate eval looks reasonable
      - Day 18: Pretraining complete, checkpoint converted to HF
      - Day 19: SFT complete
      - Day 20: DPO complete
      - Day 21: All evaluations done
      - Day 22: Report, model card, blog post drafted
      - Day 23: Everything released (GitHub, HF, blog)
    - Risk mitigation plan:
      - What if TPU is preempted for 6+ hours?
      - What if data processing takes longer than expected?
      - What if loss doesn't decrease?
      - What if SFT degrades general capability?
      - What if Vultr credits run out before data is processed?
    - Contingency: What is the minimum viable project if everything
      goes wrong? (Answer: even 50B tokens pretrained + SFT is still
      a great portfolio piece)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STYLE & FORMAT REQUIREMENTS:

- All code must be COMPLETE, RUNNABLE, PRODUCTION-GRADE Python.
- Use proper type hints, docstrings, argparse for CLI scripts.
- Format all code for 80-character print width.
- All configs must be complete — NO "..." or "fill in later" or "TODO".
- Include exact pip install commands for every dependency.
- Include exact gcloud / gsutil commands where needed.
- All scripts must have proper error handling, logging, and progress bars.
- Use `logging` module (not print statements) for all scripts.
- Use `rich` or `tqdm` for progress bars where appropriate.
- Every script must be independently runnable with clear CLI arguments.
- Comments should explain WHY, not just WHAT.
- Use pathlib for all file paths.
- Use dataclasses or pydantic for configs where appropriate.

CRITICAL INSTRUCTIONS:
- Do NOT summarize or abbreviate. Provide FULL code for every script.
- Do NOT use placeholders like "add your code here" or "TODO" or "...".
- Do NOT skip any of the 13 deliverables.
- If a deliverable requires very long code, still provide it IN FULL.
- Prefer practical, battle-tested approaches over theoretical elegance.
- Where you make a choice between alternatives, JUSTIFY the choice in
  1–2 sentences, then provide the full implementation for your chosen
  approach only. Briefly mention the alternative.
- Every number should be justified (why 3e-4 LR? why 2000 warmup steps?
  why 40/35/15/10 mix? cite papers or common practice).
- When referencing external tools (MaxText, TRL, lm-eval-harness),
  use the LATEST stable version as of April 2026 and note the version.

OUTPUT FORMAT:
If this is too long for a single response, break it into clearly numbered
parts:
  Part 1: Deliverables 1–3
  Part 2: Deliverables 4–6
  Part 3: Deliverables 7–9
  Part 4: Deliverables 10–13

At the end of each part, say "Reply 'Part N' to continue" so I can
request the next section. Ensure NO deliverable is skipped or abbreviated
across all parts.

Begin with Part 1.