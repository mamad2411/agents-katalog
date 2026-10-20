---
name: asymmetric-audio-vae-encode-decode
description: Build an AudioVAE with a 16kHz encoder and 48kHz decoder for built-in super-resolution
category: audio
version: 1.0.0
tags: [audio, vae, super-resolution, codec, pytorch]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/OpenBMB/VoxCPM.git
source_ref: main
source_commit: 13605c5a0e6b99d6d3527a43bd1a4e0e69c8800e
source_project: VoxCPM
source_paths:
  - src/voxcpm/modules/audiovae/audio_vae_v2.py
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
---

# AudioVAE with 16kHz encoder + 48kHz decoder for built-in super-resolution

## When to use
Use this pattern when your input audio is available at 16kHz (e.g., telephone recordings, ASR training data) but your output should be broadcast-quality 48kHz. The asymmetric design avoids paying the compute cost of 48kHz encoding, while the decoder learns to reconstruct the high-frequency content, eliminating the need for a separate upsampler module at inference time.

This is a structural choice for audio codec / VAE design, not an inference trick — bake it in at model definition time.

## Pattern

### Encoder (16kHz path)
```python
import torch
import torch.nn as nn

class AudioEncoder16k(nn.Module):
    """Encodes 16kHz waveforms into latent patches."""
    def __init__(self, in_channels=1, latent_dim=64, patch_size=320):
        super().__init__()
        # patch_size=320 @ 16kHz = 20ms patches
        self.conv_in = nn.Conv1d(in_channels, 64, kernel_size=7, padding=3)
        self.encoder_blocks = nn.Sequential(
            nn.Conv1d(64, 128, kernel_size=4, stride=2, padding=1),  # 8kHz
            nn.ELU(),
            nn.Conv1d(128, 256, kernel_size=4, stride=2, padding=1), # 4kHz
            nn.ELU(),
            nn.Conv1d(256, latent_dim * 2, kernel_size=1),           # mean + logvar
        )

    def forward(self, x_16k: torch.Tensor):
        # x_16k: [B, 1, T_16k]
        h = self.conv_in(x_16k)
        h = self.encoder_blocks(h)
        mean, logvar = h.chunk(2, dim=1)
        return mean, logvar
```

### Decoder (48kHz path — 3× upsampling built in)
```python
class AudioDecoder48k(nn.Module):
    """Decodes latent patches to 48kHz waveforms via learned upsampling."""
    def __init__(self, latent_dim=64, out_channels=1):
        super().__init__()
        self.conv_in = nn.Conv1d(latent_dim, 256, kernel_size=1)
        self.decoder_blocks = nn.Sequential(
            # 4kHz latent → 8kHz
            nn.ConvTranspose1d(256, 128, kernel_size=4, stride=2, padding=1),
            nn.ELU(),
            # 8kHz → 16kHz
            nn.ConvTranspose1d(128, 64, kernel_size=4, stride=2, padding=1),
            nn.ELU(),
            # 16kHz → 48kHz (3×)
            nn.ConvTranspose1d(64, 32, kernel_size=6, stride=3, padding=1),
            nn.ELU(),
        )
        self.conv_out = nn.Conv1d(32, out_channels, kernel_size=7, padding=3)

    def forward(self, z: torch.Tensor):
        # z: [B, latent_dim, T_latent]
        h = self.conv_in(z)
        h = self.decoder_blocks(h)
        return torch.tanh(self.conv_out(h))  # [B, 1, T_48k]
```

### VAE wrapper
```python
class AsymmetricAudioVAE(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = AudioEncoder16k()
        self.decoder = AudioDecoder48k()

    def encode(self, x_16k):
        mean, logvar = self.encoder(x_16k)
        std = torch.exp(0.5 * logvar)
        z = mean + std * torch.randn_like(std)
        return z, mean, logvar

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x_16k):
        z, mean, logvar = self.encode(x_16k)
        x_48k_hat = self.decode(z)
        return x_48k_hat, mean, logvar
```

### Inference: encode at 16kHz, decode to 48kHz
```python
# Typical inference usage
vae = AsymmetricAudioVAE().eval()
with torch.no_grad():
    z, _, _ = vae.encode(waveform_16k)  # cheap 16kHz encode
    audio_48k = vae.decode(z)            # full 48kHz output
```

## Source reference
- Upstream: `OpenBMB/VoxCPM` @ `main` / `13605c5a`
- Key files:
  - `src/voxcpm/modules/audiovae/audio_vae_v2.py:1-100+` — full asymmetric VAE with encoder/decoder blocks and ConvTranspose1d upsampling

## Notes
- The 3× upsampling stride in the decoder (`stride=3`) must be set carefully — kernel size should be `2*stride` and padding `stride//2` to avoid aliasing.
- Training requires a 48kHz ground-truth target even though encoding is 16kHz; ensure your dataset pipeline provides both.
- Do not apply a separate torch-audio or librosa resampler at inference — the decoder's upsampling is the resampler.
