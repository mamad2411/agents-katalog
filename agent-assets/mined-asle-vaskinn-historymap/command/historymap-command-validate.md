# Validate Current Phase

Check the status and validate the current phase of the Trondheim Historical Map project.

## Instructions

1. First, read HISTORICAL_MAP_PROJECT_PLAN.md to understand the project structure.

2. Determine which phase is currently active by checking:
   - Does frontend/ exist and work? (Phase 1)
   - Does data/synthetic/ have training data? (Phase 2)
   - Does models/checkpoints/ have trained models? (Phase 3)
   - Does data/kartverket/ have real historical maps? (Phase 4)
   - Does data/final/ have merged data? (Phase 5)

3. Run the appropriate validation:

### Phase 1 Validation
- [ ] `docker-compose up` starts successfully (or static server works)
- [ ] Map loads centered on Trondheim (63.43°N, 10.39°E)
- [ ] Can zoom and pan
- [ ] Time slider visible and draggable
- [ ] No console errors

### Phase 2 Validation
- [ ] At least 3 distinct historical styles exist
- [ ] Rendered maps look plausibly "old"
- [ ] Masks align perfectly with images
- [ ] All 5 classes represented in masks
- [ ] Can generate 1000 pairs without errors

### Phase 3 Validation
- [ ] Training starts without errors
- [ ] Loss decreases over epochs
- [ ] Validation metrics logged
- [ ] Checkpoint saved
- [ ] Inference works on new image
- [ ] Vectorization produces valid GeoJSON

### Phase 4 Validation
- [ ] Can download historical maps
- [ ] Georeferencing produces aligned output
- [ ] Tiles generated at correct size
- [ ] Fine-tuning improves metrics
- [ ] Extracted GeoJSON loads correctly

### Phase 5 Validation
- [ ] All eras visible in viewer
- [ ] Time slider correctly filters features
- [ ] Performance acceptable
- [ ] Works on mobile
- [ ] Deployed and accessible

Report the current phase status and any issues found.
