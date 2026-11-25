---
name: mobile-perf-patterns
description: "Performance fixes: iOS image downsampling and launch timing, Android StrictMode, DiffUtil, and Glide, Flutter rebuild detection, RepaintBoundary, and compute(), plus a frame budget reference. Use when fixing memory, launch, or rendering problems."
---

# Mobile Performance Patterns

## iOS: Image Downsampling (Memory Win)

```swift
// Bad: loads full pixel buffer into memory
let image = UIImage(contentsOfFile: path)
imageView.image = image

// Good: downsample to display size using ImageIO
func downsample(imageAt url: URL, to pointSize: CGSize, scale: CGFloat = UIScreen.main.scale) -> UIImage? {
    let imageSourceOptions = [kCGImageSourceShouldCache: false] as CFDictionary
    guard let source = CGImageSourceCreateWithURL(url as CFURL, imageSourceOptions) else { return nil }

    let maxDimension = max(pointSize.width, pointSize.height) * scale
    let downsampleOptions = [
        kCGImageSourceCreateThumbnailFromImageAlways: true,
        kCGImageSourceShouldCacheImmediately: true,
        kCGImageSourceCreateThumbnailWithTransform: true,
        kCGImageSourceThumbnailMaxPixelSize: maxDimension
    ] as CFDictionary

    guard let thumbnail = CGImageSourceCreateThumbnailAtIndex(source, 0, downsampleOptions) else { return nil }
    return UIImage(cgImage: thumbnail)
}

// Usage: always downsample to the display size
let thumbnailSize = CGSize(width: 200, height: 200) // actual display size
if let image = downsample(imageAt: imageURL, to: thumbnailSize) {
    imageView.image = image
}
```

---

## iOS: Launch Time Measurement

```swift
// Measure app launch with os_log signposts
import os.log

let signposter = OSSignposter(subsystem: "com.myapp", category: "Launch")

// In AppDelegate.application(_:willFinishLaunchingWithOptions:)
let launchInterval = signposter.beginInterval("AppLaunch")

// In first ViewController.viewDidAppear
signposter.endInterval("AppLaunch", launchInterval)

// View in Instruments > os_signpost lane
```

### Defer Heavy Initialization
```swift
func application(_ application: UIApplication,
                 didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    // Only critical work here — affects first frame
    setupRootViewController()

    // Defer non-critical initialization
    DispatchQueue.main.async {
        self.setupAnalytics()
        self.setupCrashReporting()
        self.prefetchUserData()
    }

    return true
}
```

---

## Android: Strict Mode (Find Main Thread Violations)

```kotlin
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()

        if (BuildConfig.DEBUG) {
            StrictMode.setThreadPolicy(
                StrictMode.ThreadPolicy.Builder()
                    .detectDiskReads()
                    .detectDiskWrites()
                    .detectNetwork()  // Main thread network calls
                    .penaltyLog()     // Log to Logcat
                    // .penaltyDeath() // Crash app — use to force fix
                    .build()
            )
            StrictMode.setVmPolicy(
                StrictMode.VmPolicy.Builder()
                    .detectLeakedSqlLiteObjects()
                    .detectLeakedClosableObjects()
                    .penaltyLog()
                    .build()
            )
        }
    }
}
```

### RecyclerView with DiffUtil
```kotlin
class ProductAdapter : ListAdapter<Product, ProductViewHolder>(ProductDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ProductViewHolder {
        val binding = ItemProductBinding.inflate(
            LayoutInflater.from(parent.context), parent, false
        )
        return ProductViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ProductViewHolder, position: Int) {
        holder.bind(getItem(position))
    }
}

class ProductDiffCallback : DiffUtil.ItemCallback<Product>() {
    override fun areItemsTheSame(old: Product, new: Product) = old.id == new.id
    override fun areContentsTheSame(old: Product, new: Product) = old == new
}

// Update list — DiffUtil calculates diff on background thread, animates changes
adapter.submitList(products) // Only redraws changed items
```

### Android: Glide for Efficient Image Loading
```kotlin
Glide.with(context)
    .load(imageUrl)
    .override(200, 200)           // Decode at display size, not full resolution
    .diskCacheStrategy(DiskCacheStrategy.RESOURCE) // Cache decoded bitmap
    .placeholder(R.drawable.placeholder)
    .into(imageView)
```

---

## Flutter: Identifying Excessive Rebuilds

```dart
// Enable rebuild counter in debug mode
void main() {
  debugPrintRebuildDirtyWidgets = true; // prints to console
  runApp(const MyApp());
}
```

### RepaintBoundary for Expensive Widgets
```dart
// Bad: expensive chart repaints when any parent rebuilds
Column(
  children: [
    UserProfile(user: user),      // changes frequently
    ExpensiveChart(data: data),    // rarely changes
  ],
)

// Good: isolate expensive widget in RepaintBoundary
Column(
  children: [
    UserProfile(user: user),
    RepaintBoundary(              // Chart repaints independently
      child: ExpensiveChart(data: data),
    ),
  ],
)
```

### ListView.builder with itemExtent
```dart
// Bad: Flutter measures each item height individually
ListView(
  children: products.map((p) => ProductCard(product: p)).toList(),
)

// Good: fixed extent skips intrinsic size measurement
ListView.builder(
  itemExtent: 80.0,           // All items same height — huge performance win
  itemCount: products.length,
  itemBuilder: (context, index) => ProductCard(product: products[index]),
)
```

### compute() for Heavy JSON Parsing
```dart
// Bad: parses large JSON on UI thread — causes jank
final products = parseProducts(jsonString); // Heavy sync operation

// Good: background isolate
final products = await compute(parseProducts, jsonString);

List<Product> parseProducts(String jsonString) {
  final List<dynamic> json = jsonDecode(jsonString);
  return json.map((j) => Product.fromJson(j)).toList();
}
```

---

## Frame Budget Reference

| Display | Frame budget | Acceptable render time |
|---------|-------------|----------------------|
| 60 Hz | 16.67ms | < 12ms (leaves headroom) |
| 90 Hz | 11.11ms | < 9ms |
| 120 Hz (ProMotion) | 8.33ms | < 6ms |

Frame drop symptoms: choppy scroll, animation stutter, "jank" feeling. Target 95th percentile frame time within budget.
