---
name: camera-media-patterns
description: "Camera code for AVCaptureSession, CameraX with ML Kit analysis, and the Flutter camera package, plus a HEIC versus JPEG decision matrix and the permission flow. Use when implementing photo or video capture or real-time frame processing."
---

# Camera Media Patterns

## iOS: AVCaptureSession Setup

```swift
import AVFoundation

class CameraManager: NSObject {
    let session = AVCaptureSession()
    private var photoOutput = AVCapturePhotoOutput()
    private let sessionQueue = DispatchQueue(label: "camera.session")

    func configure() {
        sessionQueue.async {
            self.session.beginConfiguration()
            self.session.sessionPreset = .photo

            // Find rear wide camera
            guard let device = AVCaptureDevice.default(
                .builtInWideAngleCamera, for: .video, position: .back
            ) else { return }

            do {
                let input = try AVCaptureDeviceInput(device: device)
                if self.session.canAddInput(input) {
                    self.session.addInput(input)
                }
            } catch { return }

            if self.session.canAddOutput(self.photoOutput) {
                self.session.addOutput(self.photoOutput)
                // Enable HEIC if available
                if self.photoOutput.availablePhotoCodecTypes.contains(.hevc) {
                    // Use HEIC in capturePhoto settings
                }
            }

            self.session.commitConfiguration()
            self.session.startRunning()
        }
    }
}
```

### Capture Photo with HEIC/JPEG
```swift
func capturePhoto() {
    let settings: AVCapturePhotoSettings

    if photoOutput.availablePhotoCodecTypes.contains(.hevc) {
        settings = AVCapturePhotoSettings(format: [AVVideoCodecKey: AVVideoCodecType.hevc])
    } else {
        settings = AVCapturePhotoSettings(format: [AVVideoCodecKey: AVVideoCodecType.jpeg])
    }

    settings.flashMode = .auto
    photoOutput.capturePhoto(with: settings, delegate: self)
}

// AVCapturePhotoCaptureDelegate
func photoOutput(_ output: AVCapturePhotoOutput,
                 didFinishProcessingPhoto photo: AVCapturePhoto, error: Error?) {
    guard let data = photo.fileDataRepresentation() else { return }
    let image = UIImage(data: data)
    // Save or process image
}
```

### Real-time Frame Processing (CoreImage)
```swift
extension CameraManager: AVCaptureVideoDataOutputSampleBufferDelegate {
    func captureOutput(_ output: AVCaptureOutput,
                       didOutput sampleBuffer: CMSampleBuffer,
                       from connection: AVCaptureConnection) {
        guard let pixelBuffer = CMSampleBufferGetImageBuffer(sampleBuffer) else { return }
        let ciImage = CIImage(cvPixelBuffer: pixelBuffer)

        // Apply filter
        let filter = CIFilter.colorControls()
        filter.inputImage = ciImage
        filter.saturation = 0 // Grayscale

        let output = filter.outputImage
        // Render to Metal texture or UIImage
    }
}
```

---

## Android: CameraX Setup

```kotlin
import androidx.camera.core.*
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.content.ContextCompat

class CameraFragment : Fragment() {

    private lateinit var imageCapture: ImageCapture

    fun startCamera(previewView: PreviewView) {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(requireContext())

        cameraProviderFuture.addListener({
            val cameraProvider = cameraProviderFuture.get()

            val preview = Preview.Builder().build().also {
                it.setSurfaceProvider(previewView.surfaceProvider)
            }

            imageCapture = ImageCapture.Builder()
                .setCaptureMode(ImageCapture.CAPTURE_MODE_MINIMIZE_LATENCY)
                .build()

            val imageAnalyzer = ImageAnalysis.Builder()
                .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                .build()
                .also {
                    it.setAnalyzer(ContextCompat.getMainExecutor(requireContext())) { imageProxy ->
                        analyzeImage(imageProxy)
                        imageProxy.close() // Always close to unblock camera pipeline
                    }
                }

            cameraProvider.unbindAll()
            cameraProvider.bindToLifecycle(
                viewLifecycleOwner,
                CameraSelector.DEFAULT_BACK_CAMERA,
                preview,
                imageCapture,
                imageAnalyzer
            )
        }, ContextCompat.getMainExecutor(requireContext()))
    }

    fun takePicture() {
        val outputOptions = ImageCapture.OutputFileOptions
            .Builder(createImageFile())
            .build()

        imageCapture.takePicture(
            outputOptions,
            ContextCompat.getMainExecutor(requireContext()),
            object : ImageCapture.OnImageSavedCallback {
                override fun onImageSaved(output: ImageCapture.OutputFileResults) {
                    val savedUri = output.savedUri
                    // Process saved image
                }
                override fun onError(exc: ImageCaptureException) {
                    Log.e("Camera", "Photo capture failed: ${exc.message}")
                }
            }
        )
    }
}
```

### ML Kit Vision Analysis
```kotlin
private fun analyzeImage(imageProxy: ImageProxy) {
    val mediaImage = imageProxy.image ?: return
    val inputImage = InputImage.fromMediaImage(mediaImage, imageProxy.imageInfo.rotationDegrees)

    val detector = FaceDetection.getClient()
    detector.process(inputImage)
        .addOnSuccessListener { faces ->
            faces.forEach { face ->
                val bounds = face.boundingBox
                // Draw overlay on bounds
            }
        }
        .addOnCompleteListener { imageProxy.close() }
}
```

---

## Flutter: Camera Package

```dart
import 'package:camera/camera.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  late Future<void> _initFuture;

  @override
  void initState() {
    super.initState();
    _initCamera();
  }

  Future<void> _initCamera() async {
    final cameras = await availableCameras();
    final backCamera = cameras.firstWhere(
      (c) => c.lensDirection == CameraLensDirection.back,
    );

    _controller = CameraController(
      backCamera,
      ResolutionPreset.high,
      enableAudio: false,
    );

    _initFuture = _controller.initialize();
  }

  Future<void> capturePhoto() async {
    await _initFuture;
    final XFile photo = await _controller.takePicture();
    // photo.path contains the file path
    // photo.readAsBytes() for in-memory processing
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<void>(
      future: _initFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.done) {
          return CameraPreview(_controller);
        }
        return const CircularProgressIndicator();
      },
    );
  }
}
```

---

## HEIC vs JPEG Decision Matrix

| Factor | HEIC | JPEG |
|--------|------|------|
| File size | ~50% smaller | Larger |
| Quality at same size | Higher | Lower |
| iOS compatibility | iOS 11+ | Universal |
| Android sharing | Requires transcoding | Direct share |
| Web upload | May need conversion | Native support |
| Recommendation | Intra-app only | Cross-platform sharing |

## Camera Permission Flow

```swift
// iOS — request before AVCaptureSession.startRunning()
AVCaptureDevice.requestAccess(for: .video) { granted in
    if granted {
        DispatchQueue.main.async { self.configure() }
    } else {
        // Show settings deep link: UIApplication.openSettingsURLString
    }
}
```

```kotlin
// Android — use Activity Result API
private val requestPermission =
    registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
        if (granted) startCamera()
        else showPermissionRationale()
    }

// Request on button tap or fragment start
requestPermission.launch(Manifest.permission.CAMERA)
```
