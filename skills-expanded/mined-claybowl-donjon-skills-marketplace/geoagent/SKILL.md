# GeoAgent

CVPR’26 vision-language model for image geolocation with human-like, interpretable reasoning across multiple grains (city/region/country/continent). Built on Qwen2.5-VL and trained with reinforcement learning signals including a geo-similarity reward (spatial + semantic similarity) and a consistency reward that checks reasoning-chain integrity. Ships with the GeoSeek datasets (CoT-labeled 10k, RL fine-tune 20k, validation 3k) and scripts for inference/training.

## Triggers
- "geoagent"
- "image geolocation"
- "where was this photo taken"
- "geolocate image"
- "vision language model"
- "qwen2.5 vl"

## Description
GeoAgent is a vision-language model specialized for determining the geographic location where an image was taken. It provides human-like, interpretable reasoning across multiple geographic scales (from city to continent level) and is built on the Qwen2.5-VL foundation with specialized training for geolocation tasks.

## Features
- Image geolocation across multiple scales: city, region, country, continent
- Built on Qwen2.5-VL vision-language model
- Reinforcement learning training with:
  - Geo-similarity reward (spatial + semantic similarity)
  - Consistency reward (reasoning-chain integrity)
- GeoSeek datasets:
  - Chain-of-Thought labeled: 10k images
  - RL fine-tune: 20k images
  - Validation: 3k images
- Inference and training scripts included
- Interpretable reasoning chains
- Human-like geolocation capabilities

## Usage
Use when you need to determine the geographic location of an image with explainable reasoning, particularly for OSINT, journalism, or verification tasks.

## Example
```
/geoagent geolocate this-image.jpg
/geoagent analyze reasoning for location prediction
/geoagent train on custom geolocation dataset
/geoagent evaluate on geoseek benchmark
```
