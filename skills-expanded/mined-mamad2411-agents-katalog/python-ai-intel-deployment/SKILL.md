---
name: python-ai-intel-deployment
description: "Deployment de modelos AI en hardware Intel. Cubre OpenVINO Model Server (OVMS), Docker con GPU Intel, Intel Tiber Developer Cloud, CI/CD para modelos, empaquetado de IR, edge serving, y monitoreo. Actívala para deployar modelos en producción, configurar servidores de inference, o usar la nube Intel."
disable-model-invocation: true
---

# Deployment on Intel Hardware

OpenVINO Model Server (OVMS) es el estándar para servir modelos en Intel. Docker con GPU passthrough para contenedores. Intel Tiber Cloud para prototipado gratis.

---

## Stack de deployment

| Herramienta | Propósito |
|------------|-----------|
| **OVMS** (OpenVINO Model Server) | Serving production con gRPC + REST |
| **Docker + Intel GPU** | Contenerización con acceso a GPU |
| **Intel Tiber Developer Cloud** | Sandbox gratis con JupyterLab + Intel HW |
| **Triton Inference Server** | Alternativa multi-framework con backend OpenVINO |
| **FastAPI + OpenVINO** | Serving liviano para prototipos |
| **GitHub Actions** | CI/CD con runners Intel |

---

## OpenVINO Model Server (OVMS)

### Docker run

```bash
# Pull image
docker pull openvino/model_server:latest

# Servir modelo IR
docker run -d \
  --name ovms \
  -v $(pwd)/models:/models \
  -p 9000:9000 \
  -p 8000:8000 \
  openvino/model_server:latest \
  --model_path /models/resnet50 \
  --model_name resnet \
  --port 9000 \
  --rest_port 8000 \
  --log_level INFO

# Con GPU Intel (Linux / WSL2)
docker run -d \
  --name ovms-gpu \
  --device /dev/dri \
  -v $(pwd)/models:/models \
  -p 9000:9000 \
  -p 8000:8000 \
  openvino/model_server:latest \
  --model_path /models/resnet50 \
  --model_name resnet \
  --target_device GPU \
  --port 9000 \
  --rest_port 8000

# Verificar
curl http://localhost:8000/v2/health/ready
curl http://localhost:8000/v2/models/resnet
```

### OVMS config.json

```json
{
  "model_config_list": [
    {
      "config": {
        "name": "resnet",
        "base_path": "/models/resnet50",
        "target_device": "CPU",
        "nireq": 4,
        "plugin_config": {
          "PERFORMANCE_HINT": "THROUGHPUT",
          "NUM_STREAMS": "AUTO"
        }
      }
    },
    {
      "config": {
        "name": "llama",
        "base_path": "/models/llama-3b-int4",
        "target_device": "GPU",
        "nireq": 1,
        "plugin_config": {
          "PERFORMANCE_HINT": "LATENCY"
        }
      }
    }
  ]
}
```

```bash
docker run -d \
  --device /dev/dri \
  -v $(pwd)/models:/models \
  -v $(pwd)/config.json:/config.json \
  -p 9000:9000 -p 8000:8000 \
  openvino/model_server:latest \
  --config_path /config.json
```

### Cliente Python para OVMS

```python
# ─── Cliente gRPC ───
import tritonclient.grpc as grpcclient
import numpy as np

client = grpcclient.InferenceServerClient("localhost:9000")

inputs = [grpcclient.InferInput("input", [1, 3, 224, 224], "FP32")]
inputs[0].set_data_from_numpy(np.random.randn(1, 3, 224, 224).astype(np.float32))

results = client.infer(model_name="resnet", inputs=inputs)
output = results.as_numpy("output")
print(output)

# ─── Cliente REST ───
import requests
import json

response = requests.post(
    "http://localhost:8000/v2/models/resnet/infer",
    json={
        "inputs": [{
            "name": "input",
            "shape": [1, 3, 224, 224],
            "datatype": "FP32",
            "data": np.random.randn(1, 3, 224, 224).flatten().tolist(),
        }],
    },
)
print(response.json())
```

---

## Docker con GPU Intel

### Dockerfile

```dockerfile
FROM python:3.14-slim

# Instalar oneAPI runtime (mínimo para GPU)
RUN apt-get update && apt-get install -y \
    intel-opencl-icd \
    intel-level-zero-gpu \
    libze1 \
    clinfo

# Instalar OpenVINO y dependencias
RUN pip install openvino nncf

# Copiar modelo y código
COPY models/ /app/models/
COPY src/ /app/src/

WORKDIR /app
CMD ["python", "src/serve.py"]
```

### docker-compose.yml

```yaml
version: "3.8"
services:
  ovms:
    image: openvino/model_server:latest
    ports:
      - "9000:9000"
      - "8000:8000"
    devices:
      - /dev/dri:/dev/dri
    volumes:
      - ./models:/models
      - ./config.json:/config.json
    command: --config_path /config.json
    restart: unless-stopped

  app:
    build: .
    ports:
      - "8080:8080"
    devices:
      - /dev/dri:/dev/dri
    depends_on:
      - ovms
```

### GPU passthrough en WSL2

```bash
# WSL2: habilitar GPU Intel
# 1. Instalar drivers Intel GPU en Windows
# 2. En WSL2:
sudo apt update
sudo apt install intel-opencl-icd intel-level-zero-gpu

# 3. Verificar
clinfo | grep "Device Name"
# → Intel(R) Arc(TM) Graphics

# 4. Docker con --device /dev/dri funciona en WSL2
docker run --device /dev/dri ...
```

---

## FastAPI + OpenVINO (prototipos)

```python
from fastapi import FastAPI
from pydantic import BaseModel
import openvino as ov
import numpy as np

app = FastAPI(title="Inference API")

# ─── Startup: cargar modelo ───
core = ov.Core()
compiled = core.compile_model("model.xml", "CPU")

class InferenceRequest(BaseModel):
    data: list[float]
    shape: list[int]

@app.post("/predict")
async def predict(req: InferenceRequest):
    tensor = np.array(req.data, dtype=np.float32).reshape(req.shape)
    result = compiled({"input": tensor})
    output = result["output"].flatten().tolist()
    return {"prediction": output}

# ─── Uvicorn ───
# uv run uvicorn serve:app --host 0.0.0.0 --port 8080
```

---

## Intel Tiber Developer Cloud

```bash
# Acceso gratis a JupyterLab con todo el stack Intel preinstalado
# URL: https://console.cloud.intel.com

# Instalar CLI
uv add devcloud

# Conectar
devcloud login
devcloud jupyter launch --instance-size medium

# Subir modelo
devcloud upload model.xml model.bin

# Ejecutar job remoto con hardware Intel
devcloud job submit \
  --instance gpu.arc \
  -- python inference.py \
  --model model.xml \
  --device GPU
```

### JupyterLab en Tiber Cloud

```python
# Código corre en hardware Intel real (Xeon, Arc, Gaudi)
import openvino as ov
import torch

core = ov.Core()
print("Dispositivos:", core.available_devices)
# → ["CPU", "GPU"]  # GPU = Intel Data Center GPU

print("XPU:", torch.xpu.is_available())
# → True (si elegiste instancia GPU)

# Sin costo para prototipado
```

---

## CI/CD para modelos

### GitHub Actions con Intel runners

```yaml
# .github/workflows/validate-model.yml
name: Validate Model
on:
  pull_request:
    paths: ["models/**"]

jobs:
  validate:
    runs-on: ubuntu-latest
    container:
      image: openvino/ubuntu22_runtime:2026.2.0
    steps:
      - uses: actions/checkout@v4

      - name: Validate IR model
        run: |
          python -c "
          import openvino as ov
          core = ov.Core()
          model = core.read_model('models/model.xml')
          print('Inputs:', [i.name for i in model.inputs])
          print('Outputs:', [o.name for o in model.outputs])
          "

      - name: Benchmark
        run: |
          benchmark_app -m models/model.xml -d CPU -niter 100

      - name: Accuracy check
        run: |
          python tests/test_accuracy.py
```

---

## Edge deployment (Core Ultra)

```python
# ─── Empaquetar para edge ───
import openvino as ov
import shutil
from pathlib import Path

def package_for_edge(model_xml: str, output_dir: str, target: str = "AUTO"):
    """Empaqueta modelo y dependencias para edge deployment."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Copiar modelo IR
    shutil.copy(model_xml, out)
    shutil.copy(model_xml.replace(".xml", ".bin"), out)

    # Generar config
    config = {
        "model": Path(model_xml).name,
        "target_device": target,  # AUTO elige NPU si está disponible
        "performance_hint": "LATENCY",
    }
    import json
    with open(out / "config.json", "w") as f:
        json.dump(config, f)

    return out

package_for_edge("mobilenet_npu.xml", "./edge_package/", target="AUTO:NPU,CPU")
```

---

## Checklist Deployment

- [ ] Modelo en formato IR (`.xml` + `.bin`), cuantizado
- [ ] OVMS para producción (gRPC + REST, multi-modelo)
- [ ] Docker con `--device /dev/dri` para acceso a GPU Intel
- [ ] `PERFORMANCE_HINT` configurado (`THROUGHPUT` para serving, `LATENCY` para edge)
- [ ] Health check (`/v2/health/ready`) monitoreado
- [ ] `config.json` versionado con el modelo
- [ ] CI valida que el IR compila y no degrada precisión
- [ ] Edge package incluido `config.json` con `AUTO:NPU,CPU`
- [ ] Intel Tiber Cloud para staging/testing sin hardware propio
- [ ] Sin secretos ni API keys en el container
