---

## name: medical-imaging
description: >
  Expert medical imaging assistant for researchers and students. Use this skill whenever the user needs:
  understanding imaging modalities, image acquisition, reconstruction algorithms, analysis techniques, deep learning 
  applications, or any rigorous academic treatment of medical imaging. Covers X-ray, CT, MRI, PET, ultrasound, 
  and emerging modalities with computational analysis approaches.
license: MIT
compatibility: opencode
metadata:
  audience: medical-students
  category: medicine

# Medical Imaging — Academic Research Assistant

Covers: **X-Ray & CT · MRI · PET · Ultrasound · Image Processing · Deep Learning · Quantitative Imaging · Radiation Safety**

---

## Imaging Modalities

### X-Ray Imaging

|Property|Value|
|---------|-----|
|Physics|X-ray attenuation|
|Resolution|50-200 μm|
|Acquisition time|ms|
|Radiation dose|0.1 mSv (chest)|
|Contrast|Soft tissue: poor; Bone: excellent|

```
X-ray Attenuation (Beer-Lambert Law):
I = I₀ · e^(-μx)

Where:
- I = transmitted intensity
- I₀ = incident intensity
- μ = linear attenuation coefficient
- x = path length
```

### Computed Tomography (CT)

|Property|Value|
|---------|-----|
|Physics|X-ray attenuation, fan-beam reconstruction|
|Resolution|0.5-1 mm|
|Acquisition time|0.3-2 s|
|Radiation dose|5-10 mSv (routine)|
|Contrast|Excellent soft tissue with IV contrast|

```python
class CTReconstruction:
    """Simplified CT reconstruction concepts"""
    
    def filtered_backprojection(self, sinogram, filter_type='ram-lak'):
        """
        Analytical reconstruction from projections
        Steps: Filter projections → Backproject
        """
        # Filter (convolution with reconstruction kernel)
        filtered = self.apply_filter(sinogram, filter_type)
        
        # Backprojection
        image = self.backproject(filtered)
        
        return image
    
    def iterative_reconstruction(self, projections, iterations=10):
        """
        Iterative reconstruction (OS-SART, SIRT)
        Advantages: Lower noise, can incorporate priors
        """
        estimate = self.initialize_image()
        
        for _ in range(iterations):
            # Forward project current estimate
            forward_proj = self.forward_project(estimate)
            
            # Calculate correction
            error = projections - forward_proj
            correction = self.backproject(error)
            
            # Update estimate
            estimate += self.relaxation * correction
        
        return estimate
```

### Magnetic Resonance Imaging (MRI)

|Property|Value|
|---------|-----|
|Physics|Nuclear magnetic resonance|
|Resolution|1-2 mm (clinical), μm (research)|
|Acquisition time|min (anatomical), hr (functional)|
|Radiation dose|0 mSv (no ionizing radiation)|
|Contrast|Excellent soft tissue, multi-parametric|

```python
class MRIContrast:
    """MRI contrast mechanisms"""
    
    T1_WEIGHTING = {
        "TR": "Repetition time (short < 1000 ms)",
        "TE": "Echo time (short < 30 ms)",
        "application": "Anatomy, T1 gadolinium enhancement"
    }
    
    T2_WEIGHTING = {
        "TR": "Long (> 2000 ms)",
        "TE": "Long (> 80 ms)",
        "application": "Pathology, edema, fluid"
    }
    
    FLAIR = {
        "description": "Fluid Attenuated Inversion Recovery",
        "suppresses": "CSF signal",
        "application": "White matter lesions, tumors"
    }
    
    DIFFUSION = {
        "sequence": "DWI - echo planar",
        "b-values": "0, 500, 1000 s/mm²",
        "application": "Stroke (restricted diffusion), tumors"
    }
    
    FUNCTIONAL_MRI = {
        "technique": "BOLD (Blood Oxygen Level Dependent)",
        "principle": "Hemodynamic response to neural activity",
        "temporal_resolution": "1-3 seconds",
        "spatial_resolution": "2-3 mm"
    }
```

### Positron Emission Tomography (PET)

|Property|Value|
|---------|-----|
|Physics|Radioactive decay, annihilation photons|
|Resolution|4-5 mm|
|Acquisition time|10-30 min|
|Radiation dose|2-5 mSv (FDG)|
|Contrast|Functional/molecular (not anatomical)|

---

## Image Processing

### Basic Image Operations

```python
import numpy as np

class MedicalImageProcessing:
    """Medical image processing utilities"""
    
    def normalize_intensity(self, image, method='minmax'):
        """Normalize image intensities"""
        if method == 'minmax':
            imin, imax = image.min(), image.max()
            if imax - imin > 0:
                return (image - imin) / (imax - imin)
            return image
        
        elif method == 'zscore':
            return (image - image.mean()) / image.std()
        
        elif method == 'percentile':
            p1, p99 = np.percentile(image, (1, 99))
            return np.clip((image - p1) / (p99 - p1), 0, 1)
    
    def gaussian_smoothing(self, image, sigma=1.0):
        """Apply Gaussian smoothing"""
        from scipy.ndimage import gaussian_filter
        return gaussian_filter(image, sigma)
    
    def intensity_windowing(self, image, window_level):
        """
        Window/level adjustment for CT
        window: window width (contrast)
        level: window center (brightness)
        """
        window, level = window_level
        lower = level - window / 2
        upper = level + window / 2
        return np.clip((image - lower) / (upper - lower), 0, 1)
    
    # Common CT window settings
    COMMON_WINDOWS = {
        "brain": (80, 40),
        "soft_tissue": (400, 50),
        "lung": (1500, -600),
        "bone": (2000, 400),
        "liver": (150, 30)
    }
```

### Image Segmentation

```python
class SegmentationMethods:
    """Medical image segmentation approaches"""
    
    def threshold_segmentation(self, image, threshold):
        """Simple threshold-based segmentation"""
        return (image > threshold).astype(np.uint8)
    
    def otsu_threshold(self, image):
        """Automatic threshold using Otsu's method"""
        from scipy import ndimage
        
        # Compute histogram
        hist, bins = np.histogram(image.flatten(), bins=256)
        
        # Normalize
        hist = hist.astype(float) / hist.sum()
        
        # Find threshold
        threshold = 0
        max_variance = 0
        
        for t in range(1, 256):
            w0 = hist[:t].sum()
            w1 = hist[t:].sum()
            
            if w0 == 0 or w1 == 0:
                continue
            
            mu0 = np.sum(np.arange(t) * hist[:t]) / w0
            mu1 = np.sum(np.arange(t, 256) * hist[t:]) / w1
            
            variance = w0 * w1 * (mu0 - mu1) ** 2
            
            if variance > max_variance:
                max_variance = variance
                threshold = t
        
        return threshold
    
    def region_growing(self, image, seed, threshold):
        """Region growing segmentation"""
        import queue
        
        mask = np.zeros_like(image, dtype=bool)
        q = queue.Queue()
        q.put(seed)
        mask[seed] = True
        
        while not q.empty():
            x, y = q.get()
            
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    
                    if (0 <= nx < image.shape[0] and 
                        0 <= ny < image.shape[1] and
                        not mask[nx, ny] and
                        abs(image[nx, ny] - image[seed]) < threshold):
                        
                        mask[nx, ny] = True
                        q.put((nx, ny))
        
        return mask.astype(np.uint8)
```

### Morphological Operations

|Operation|Effect|
|----------|------|
|Erosion|Shrinks objects, removes small structures|
|Dilation|Expands objects, fills small holes|
|Opening|Erosion then dilation, removes small objects|
|Closing|Dilation then erosion, fills small holes|

---

## Deep Learning in Medical Imaging

### Common Network Architectures

```python
class MedicalImageNetworks:
    """Deep learning architectures for medical imaging"""
    
    UNET_ARCHITECTURE = {
        "type": "U-Net (encoder-decoder)",
        "components": [
            "Encoder: contracting path (feature extraction)",
            "Bottleneck: lowest resolution features",
            "Decoder: expanding path (upsampling)",
            "Skip connections: preserve spatial information"
        ],
        "application": "Segmentation (tumors, organs, lesions)",
        "input": "2D/3D medical images",
        "output": "Probability mask"
    }
    
    RESNET_ARCHITECTURE = {
        "type": "ResNet (residual networks)",
        "key_innovation": "Skip connections (residual blocks)",
        "benefit": "Enables training very deep networks",
        "application": "Classification, detection",
        "variants": ["ResNet-50", "ResNet-101", "ResNet-152"]
    }
    
    DETECTION_ARCHITECTURES = {
        "two_stage": ["Faster R-CNN", "Mask R-CNN"],
        "single_stage": ["YOLO", "SSD", "RetinaNet"],
        "application": "Lesion detection, organ localization"
    }
```

### Data Augmentation

```python
class MedicalImageAugmentation:
    """Domain-specific augmentations for medical images"""
    
    # Geometric transformations
    GEOMETRIC = [
        "Random rotation (limited angle)",
        "Random scaling",
        "Random flipping",
        "Elastic deformation (for soft tissue)",
        "Random crop/patch extraction"
    ]
    
    # Intensity transformations
    INTENSITY = [
        "Random brightness",
        "Random contrast",
        "Random noise (Gaussian, Poisson)",
        "Random gamma correction",
        "Histogram equalization"
    ]
    
    # Medical-specific
    MEDICAL_SPECIFIC = [
        "Simulate imaging artifacts",
        "Motion blur simulation",
        "Bias field simulation (MRI)",
        "Partial volume simulation",
        "Contrast variation (CT, MRI)"
    ]
```

---

## Quantitative Imaging

### Radiomics Features

|Category|Features|
|---------|--------|
|Shape|Volume, surface area, sphericity, compactness|
|First-order|Mean, std, skewness, kurtosis, energy, entropy|
|Texture (GLCM)|Contrast, correlation, energy, homogeneity|
|Texture (GLRLM)|Run emphasis, gray level emphasis|
|Wavelet|Decomposed texture at multiple scales|

### Biomarkers

|Modality|Biomarker|Application|
|--------|---------|-----------|
|CT|Emphysema percentage|Lung disease|
|CT|Lung nodule volume doubling time|Cancer|
|MRI|T1/T2 relaxation times|Tissue characterization|
|PET|SUVmax, SUVmean|Tumor FDG uptake|
|DWI|ADC value|Stroke, tumors|
|DCE-MRI|Ktrans, Ve, Vp|Perfusion, permeability|

---

## Radiation Safety

### Dose Metrics

|Metric|Unit|Definition|
|------|-----|----------|
|Absorbed dose|Gray (Gy)|Energy deposited per kg|
|Equivalent dose|Sievert (Sv)|Absorbed dose × radiation weighting|
|Effective dose|Sievert (Sv)|Equivalent dose × tissue weighting|

### Typical Doses

|Study|Dose (mSv)|Equivalent background|
|-----|----------|---------------------|
|Chest X-ray|0.1|10 days|
|CT Head|2|8 months|
|CT Chest|7|2 years|
|CT Abdomen/Pelvis|10|3 years|
|PET/CT|25|8 years|
|Mammography|0.4|6 weeks|

---

## Common Errors to Avoid

1. **Ignoring partial volume effects** — Small structures appear larger/dimmer
2. **Inadequate normalization** — Batch effects across scanners
3. **Overfitting deep learning models** — Small datasets, heavy augmentation
4. **Not considering imaging artifacts** — Motion, beam hardening, aliasing
5. **Confusing resolution with pixel spacing** — Matrix size vs. physical size
6. **Ignoring contrast timing** — Arterial, venous, delayed phases
7. **Insufficient training data** — Medical imaging needs thousands of samples
8. **Not validating on external data** — Scanner/protocol specific models

