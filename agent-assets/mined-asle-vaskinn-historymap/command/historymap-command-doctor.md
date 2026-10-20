# Doctor - Project Health Check

Run a comprehensive health check on the Trondheim Historical Map project.

## Instructions

Check the following aspects of the project setup:

### 1. Dependencies
- [ ] Python 3.11+ available: `python3 --version`
- [ ] Required Python packages installed (check for torch, segmentation-models-pytorch, rasterio, shapely)
- [ ] Node.js available (optional, for development)
- [ ] Docker available: `docker --version`

### 2. Directory Structure
- [ ] `frontend/` exists with index.html, app.js, style.css
- [ ] `ml/` exists with train.py, predict.py, vectorize.py, config.yaml
- [ ] `scripts/` exists with utility scripts
- [ ] `data/` directory exists

### 3. Data Files
- [ ] Check for PMTiles in `frontend/data/` or `data/`
- [ ] Check for trained models in `models/checkpoints/`
- [ ] Check for GeoJSON data files

### 4. Configuration
- [ ] `ml/config.yaml` is valid YAML
- [ ] Frontend references correct data paths

### 5. Services
- [ ] Test if development server can start
- [ ] Verify Docker containers can build

Report all findings with status (OK/WARNING/ERROR) and suggested fixes for any issues found.
