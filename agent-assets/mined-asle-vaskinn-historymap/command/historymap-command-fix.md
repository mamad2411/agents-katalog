# Fix Issues

Diagnose and fix problems in the current phase.

## Usage
Describe the issue you're encountering, and this command will help diagnose and fix it.

## Common Issues by Phase

### Phase 1 Issues

**Map doesn't load**
- Check browser console for errors
- Verify PMTiles file exists and path is correct
- Check CORS headers if using http server
- Ensure pmtiles protocol is registered

**Time slider doesn't filter**
- Verify features have start_date/end_date properties
- Check filter expression in MapLibre style
- Most OSM features don't have dates - this is expected initially

**Docker won't start**
- Check ports aren't in use: `lsof -i :8080`
- Verify docker-compose.yml syntax
- Check file paths are correct

### Phase 2 Issues

**Styles don't render correctly**
- Validate JSON syntax
- Check source layer names match OSM schema
- Verify zoom level ranges

**Aging effects look wrong**
- Adjust intensity parameters
- Check texture overlay blend mode
- Verify image dimensions match

**Masks don't align**
- Ensure same random seed for both render and mask
- Check coordinate transformations are identical
- Verify tile boundaries match

### Phase 3 Issues

**Training crashes**
- Check GPU memory - reduce batch size
- Verify dataset paths correct
- Check for corrupted images in dataset

**Loss not decreasing**
- Learning rate may be too high/low
- Check data augmentation isn't too aggressive
- Verify labels are correct (0-4 range)

**Poor inference results**
- Domain gap too large - improve synthetic styles
- Model overfitting - add regularization
- Check input preprocessing matches training

### Phase 4 Issues

**Can't download Kartverket maps**
- Check API endpoints are current
- May need to browse kartkatalog.geonorge.no manually
- Try different map series

**Georeferencing inaccurate**
- Need ground control points
- Check source/target CRS are correct
- Historical maps may have significant distortion

### Phase 5 Issues

**Performance slow**
- Reduce PMTiles zoom levels
- Simplify geometries
- Check for duplicate features

**Features disappear at zoom levels**
- Check minzoom/maxzoom in style
- Verify PMTiles contains all zoom levels

Describe your specific issue for targeted help.
