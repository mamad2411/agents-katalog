# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

NTU ML Spring 2026 Homework 4: Training a Transformer (GPT-2) for Pokémon image generation via next-token prediction on pixel color sequences.

The core notebook is `ML2026_Spring_HW4_Training_Transformer.ipynb`.

## Task

Train a GPT-2 decoder-only transformer to predict Pokémon image pixels sequentially (next-token prediction). Images are encoded as sequences of color indices from a discrete colormap. The model learns to generate Pokémon by predicting the next pixel color given preceding pixels.

## Model Architecture

GPT-2 with custom config:
- 2 layers, 2 attention heads, 64-dim embeddings
- Context window: 128 tokens
- Vocab size: number of unique colors in the colormap
- Activation: GELU; dropout 0.1 on attention/embedding/residual

## Data

Loaded from HuggingFace Hub:
- `lca0503/ml2025-hw4-pokemon` — Pokémon pixel sequences (train/test split)
- `lca0503/ml2025-hw4-colormap` — discrete color palette for encoding/decoding

## Training

- Loss: CrossEntropyLoss (next-token prediction)
- Optimizer: Adam
- 50 epochs; save checkpoint with lowest training loss
- Best model checkpoint used for inference

## Inference & Submission

- Load best checkpoint, run generation on test set
- Save predictions to a `.txt` file
- Submit `.txt` to Judgeboi for grading

## Running the Notebook

```bash
# Install dependencies (run once)
pip install transformers datasets tqdm pillow matplotlib torch

# Launch notebook
jupyter notebook ML2026_Spring_HW4_Training_Transformer.ipynb

# Or run all cells non-interactively
jupyter nbconvert --to notebook --execute ML2026_Spring_HW4_Training_Transformer.ipynb --output executed.ipynb
```

## Last session

```sh
claude --resume ccc0515d-ad04-4a35-9fa6-6754062ebfe2
```
