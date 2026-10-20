# Next Steps

Analyze the current project state and recommend the next concrete actions.

## Instructions

1. First run `/status` mentally or check key files to understand current state.

2. Based on the current phase, provide:

### If Starting Fresh (no Phase 1)
```
Recommended: Run /start-phase-1 to launch parallel workers

This will create:
- Frontend with MapLibre + time slider
- OSM data download and tile generation scripts
- Docker setup for local development
```

### If Phase 1 Complete
```
Verify Phase 1:
- docker-compose up (or python -m http.server in frontend/)
- Open http://localhost:8080
- Confirm map loads and time slider works

If working → Run /start-phase-2
If issues → List specific problems to fix
```

### If Phase 2 Complete  
```
Verify synthetic data:
- Check data/synthetic/images/ has 1000+ images
- Visually inspect a few samples
- Verify mask alignment

If good → Run /start-phase-3
If issues → Improve style variety or aging effects
```

### If Phase 3 Complete
```
Critical decision point!

1. Download ONE real historical map tile from Kartverket
2. Run inference: python ml/predict.py --input real_tile.png
3. Evaluate IoU manually

If IoU > 0.5 → Run /start-phase-4
If IoU < 0.3 → Need to improve synthetic training
```

### If Phase 4 Complete
```
Verify extractions:
- Load data/extracted/*.geojson in QGIS
- Check features align with original maps
- Assess quality

If acceptable → Run /start-phase-5
If poor → More annotations needed, re-fine-tune
```

### If Phase 5 Complete
```
You're done! 🎉

Final checks:
- Test deployed URL
- Try on mobile
- Share with others for feedback
```

Provide specific, actionable recommendations based on current state.
