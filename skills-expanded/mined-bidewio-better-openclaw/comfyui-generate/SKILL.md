---
name: comfyui-generate
description: "Generate images and media using ComfyUI's node-based workflow API at {{COMFYUI_HOST}}:{{COMFYUI_PORT}}."
metadata:
  openclaw:
    emoji: "🎨"
---

# ComfyUI Image Generation Skill

ComfyUI node-based workflow server is available at `http://{{COMFYUI_HOST}}:{{COMFYUI_PORT}}` within the Docker network.

> ⚠️ **GPU Required**: ComfyUI requires an NVIDIA GPU with CUDA support and the NVIDIA Container Toolkit installed on the host. Without GPU acceleration, image generation is extremely slow.

## Queue a Workflow (Text-to-Image)

Submit a workflow graph as JSON to generate images:

```bash
curl -X POST "http://{{COMFYUI_HOST}}:{{COMFYUI_PORT}}/prompt" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": {
      "3": {
        "class_type": "KSampler",
        "inputs": {
          "seed": 42,
          "steps": 20,
          "cfg": 7.0,
          "sampler_name": "euler",
          "scheduler": "normal",
          "denoise": 1.0,
          "model": ["4", 0],
          "positive": ["6", 0],
          "negative": ["7", 0],
          "latent_image": ["5", 0]
        }
      },
      "4": {
        "class_type": "CheckpointLoaderSimple",
        "inputs": { "ckpt_name": "v1-5-pruned-emaonly.safetensors" }
      },
      "5": {
        "class_type": "EmptyLatentImage",
        "inputs": { "width": 512, "height": 512, "batch_size": 1 }
      },
      "6": {
        "class_type": "CLIPTextEncode",
        "inputs": {
          "text": "a beautiful sunset over mountains, photorealistic",
          "clip": ["4", 1]
        }
      },
      "7": {
        "class_type": "CLIPTextEncode",
        "inputs": {
          "text": "ugly, blurry, low quality",
          "clip": ["4", 1]
        }
      },
      "8": {
        "class_type": "VAEDecode",
        "inputs": { "samples": ["3", 0], "vae": ["4", 2] }
      },
      "9": {
        "class_type": "SaveImage",
        "inputs": { "filename_prefix": "ComfyUI", "images": ["8", 0] }
      }
    }
  }'
```

The response returns a `prompt_id` you can use to track the job.

## Check Job Status

```bash
# Get history for a specific prompt
curl "http://{{COMFYUI_HOST}}:{{COMFYUI_PORT}}/history/<prompt_id>"
```

## Retrieve Generated Images

```bash
# View a generated image by filename and subfolder
curl "http://{{COMFYUI_HOST}}:{{COMFYUI_PORT}}/view?filename=ComfyUI_00001_.png&subfolder=&type=output"
```

## System Info

```bash
# Check system stats (GPU, memory, queue length)
curl "http://{{COMFYUI_HOST}}:{{COMFYUI_PORT}}/system_stats"

# Get available object types (all node classes)
curl "http://{{COMFYUI_HOST}}:{{COMFYUI_PORT}}/object_info"

# Get current queue status
curl "http://{{COMFYUI_HOST}}:{{COMFYUI_PORT}}/queue"
```

## Interrupt / Clear Queue

```bash
# Interrupt the current generation
curl -X POST "http://{{COMFYUI_HOST}}:{{COMFYUI_PORT}}/interrupt"

# Clear the pending queue
curl -X POST "http://{{COMFYUI_HOST}}:{{COMFYUI_PORT}}/queue" \
  -H "Content-Type: application/json" \
  -d '{"clear": true}'
```

## Tips for AI Agents

- Every ComfyUI workflow is a **JSON node graph**. You can export any workflow from the UI as JSON and replay it via the API.
- Use `/system_stats` to check GPU availability and VRAM before queuing heavy jobs.
- Use `/queue` to monitor how many jobs are pending before submitting more.
- Set deterministic `seed` values for reproducible results.
- Lower `steps` (10-15) for quick drafts; higher (30-50) for quality.
- Adjust `cfg` (classifier-free guidance): 5-8 for natural images, 10-15 for stylized.
- Check `/object_info` to discover available node types and their inputs.
- Combine with **Ollama** to let an LLM write the prompt text, then pass it to ComfyUI for generation.
- Store generated images in **MinIO** for persistent object storage.
