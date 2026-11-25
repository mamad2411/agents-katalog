---
name: gesture-patterns
description: "Gesture code for UIPanGestureRecognizer with velocity, custom UIGestureRecognizer subclasses, Compose gesture modifiers, Flutter fling animations, and haptic timing. Use when building drag, swipe, or fling interactions or deciding when to fire haptics."
---

# Gesture Patterns

## iOS: UIPanGestureRecognizer with Velocity

```swift
class DismissableCard: UIView {
    private lazy var panGesture: UIPanGestureRecognizer = {
        let gr = UIPanGestureRecognizer(target: self, action: #selector(handlePan))
        gr.delegate = self
        return gr
    }()

    private let feedbackGenerator = UIImpactFeedbackGenerator(style: .medium)
    private var initialCenter: CGPoint = .zero

    override func didMoveToSuperview() {
        super.didMoveToSuperview()
        addGestureRecognizer(panGesture)
        feedbackGenerator.prepare() // Warm up engine before interaction
    }

    @objc private func handlePan(_ gesture: UIPanGestureRecognizer) {
        let translation = gesture.translation(in: superview)
        let velocity = gesture.velocity(in: superview)

        switch gesture.state {
        case .began:
            initialCenter = center

        case .changed:
            center = CGPoint(
                x: initialCenter.x + translation.x,
                y: initialCenter.y + translation.y
            )
            // Fade based on horizontal displacement
            let progress = abs(translation.x) / (superview?.bounds.width ?? 1)
            alpha = 1 - progress * 0.5

        case .ended, .cancelled:
            let speed = sqrt(velocity.x * velocity.x + velocity.y * velocity.y)
            let threshold: CGFloat = 500

            if speed > threshold || abs(translation.x) > bounds.width * 0.4 {
                feedbackGenerator.impactOccurred()
                dismissCard(velocity: velocity)
            } else {
                snapBack()
            }

        default: break
        }
    }

    private func dismissCard(velocity: CGPoint) {
        let unitVector = CGPoint(
            x: velocity.x / max(abs(velocity.x), 1),
            y: velocity.y / max(abs(velocity.y), 1)
        )
        UIView.animate(withDuration: 0.3, delay: 0, options: .curveEaseOut) {
            self.center = CGPoint(
                x: self.center.x + unitVector.x * 400,
                y: self.center.y + unitVector.y * 400
            )
            self.alpha = 0
        } completion: { _ in self.removeFromSuperview() }
    }

    private func snapBack() {
        UIView.animate(withDuration: 0.4, delay: 0,
                       usingSpringWithDamping: 0.7, initialSpringVelocity: 0.5) {
            self.center = self.initialCenter
            self.alpha = 1
        }
    }
}

// Simultaneous recognition with scroll view
extension DismissableCard: UIGestureRecognizerDelegate {
    func gestureRecognizer(_ gestureRecognizer: UIGestureRecognizer,
                           shouldRecognizeSimultaneouslyWith other: UIGestureRecognizer) -> Bool {
        return other is UIPanGestureRecognizer
    }
}
```

---

## iOS: Custom UIGestureRecognizer

```swift
import UIKit.UIGestureRecognizerSubclass

class CircularSwipeGestureRecognizer: UIGestureRecognizer {
    private var startPoint: CGPoint = .zero
    private var currentAngle: CGFloat = 0

    var minimumAngle: CGFloat = .pi // 180 degrees minimum for recognition

    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent) {
        super.touchesBegan(touches, with: event)
        guard touches.count == 1 else { state = .failed; return }
        startPoint = touches.first!.location(in: view)
        state = .began
    }

    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent) {
        super.touchesMoved(touches, with: event)
        guard let touch = touches.first else { return }
        let current = touch.location(in: view)
        let center = CGPoint(x: view!.bounds.midX, y: view!.bounds.midY)

        let angle1 = atan2(startPoint.y - center.y, startPoint.x - center.x)
        let angle2 = atan2(current.y - center.y, current.x - center.x)
        currentAngle = angle2 - angle1
        state = .changed
    }

    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent) {
        super.touchesEnded(touches, with: event)
        state = abs(currentAngle) >= minimumAngle ? .ended : .failed
    }
}
```

---

## Android: Jetpack Compose Gestures

```kotlin
// Drag with velocity tracking
@Composable
fun DraggableCard() {
    var offsetX by remember { mutableStateOf(0f) }
    var offsetY by remember { mutableStateOf(0f) }
    val hapticFeedback = LocalHapticFeedback.current

    Box(
        modifier = Modifier
            .offset { IntOffset(offsetX.roundToInt(), offsetY.roundToInt()) }
            .pointerInput(Unit) {
                detectDragGestures(
                    onDragStart = { _ ->
                        hapticFeedback.performHapticFeedback(HapticFeedbackType.LongPress)
                    },
                    onDrag = { change, dragAmount ->
                        change.consume()
                        offsetX += dragAmount.x
                        offsetY += dragAmount.y
                    },
                    onDragEnd = {
                        // Snap back with spring animation
                        // Use Animatable for physics-based return
                    }
                )
            }
    ) {
        CardContent()
    }
}

// Pinch-to-zoom with scale gesture
@Composable
fun ZoomableImage(imageUrl: String) {
    var scale by remember { mutableStateOf(1f) }
    var offset by remember { mutableStateOf(Offset.Zero) }

    Image(
        painter = rememberAsyncImagePainter(imageUrl),
        contentDescription = null,
        modifier = Modifier
            .graphicsLayer(
                scaleX = scale,
                scaleY = scale,
                translationX = offset.x,
                translationY = offset.y
            )
            .pointerInput(Unit) {
                detectTransformGestures { _, pan, zoom, _ ->
                    scale = (scale * zoom).coerceIn(0.5f, 5f)
                    offset = Offset(
                        offset.x + pan.x * scale,
                        offset.y + pan.y * scale
                    )
                }
            }
    )
}
```

---

## Flutter: Gesture Velocity + Fling Animation

```dart
class SwipeableCard extends StatefulWidget {
  const SwipeableCard({super.key});

  @override
  State<SwipeableCard> createState() => _SwipeableCardState();
}

class _SwipeableCardState extends State<SwipeableCard>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  Offset _position = Offset.zero;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: const Duration(milliseconds: 300));
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onPanUpdate: (details) {
        setState(() => _position += details.delta);
      },
      onPanEnd: (details) async {
        final velocity = details.velocity.pixelsPerSecond;
        final speed = velocity.distance;

        if (speed > 600 || _position.dx.abs() > 150) {
          // Fling off screen
          await HapticFeedback.mediumImpact();
          // Animate to off-screen and notify parent
        } else {
          // Spring back to center
          final animation = Tween<Offset>(
            begin: _position,
            end: Offset.zero,
          ).animate(CurvedAnimation(parent: _controller, curve: Curves.elasticOut));

          animation.addListener(() => setState(() => _position = animation.value));
          _controller.forward(from: 0);
        }
      },
      child: Transform.translate(
        offset: _position,
        child: const CardWidget(),
      ),
    );
  }
}
```

---

## Haptic Timing Patterns

| Action | iOS | Android | Flutter |
|--------|-----|---------|---------|
| Button press | `.light` impact | `KEYBOARD_TAP` | `lightImpact()` |
| Long press start | `.medium` impact | `LONG_PRESS` | `mediumImpact()` |
| Item selection | `UISelectionFeedbackGenerator` | `CLOCK_TICK` | `selectionClick()` |
| Confirm/Submit | `.heavy` impact | `CONFIRM` | `heavyImpact()` |
| Error/Failure | `.error` notification | `REJECT` | `vibrate()` |
| Success | `.success` notification | `CONFIRM` | `lightImpact()` |
| Swipe-to-dismiss | `.medium` at threshold | `CLOCK_TICK` at threshold | `mediumImpact()` |
