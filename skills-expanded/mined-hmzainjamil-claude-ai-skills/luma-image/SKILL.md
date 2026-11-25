# Luma Image/Video Generation Skill
## Triggers: luma, dream machine, luma ai, luma video, luma image, uni-1
## API: https://agents.lumalabs.ai/v1/generations (LUMA_API_KEY env)
## Status: Key configured — needs credits at lumalabs.ai/billing

### Quick generate
```python
import requests, os, time
KEY = os.environ["LUMA_API_KEY"]
def luma_generate(prompt, model="uni-1", aspect="16:9"):
    r = requests.post("https://agents.lumalabs.ai/v1/generations",
        headers={"Authorization": f"Bearer {KEY}"},
        json={"model": model, "prompt": prompt, "aspect_ratio": aspect})
    job = r.json()
    job_id = job.get("id")
    # Poll until done
    for _ in range(40):
        time.sleep(8)
        s = requests.get(f"https://agents.lumalabs.ai/v1/generations/{job_id}",
            headers={"Authorization": f"Bearer {KEY}"}).json()
        if s.get("state") == "completed":
            return s["assets"]["video"] or s["assets"]["image"]
        if s.get("state") == "failed":
            raise Exception(s.get("failure_reason"))
    raise TimeoutError("Luma generation timed out")
```
### Models: uni-1 (image+video), photon (image), ray-2 (video)
### Output: saved to ~/Downloads/luma-output/
