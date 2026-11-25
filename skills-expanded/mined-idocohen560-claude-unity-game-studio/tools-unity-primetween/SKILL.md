---
name: tools-unity-primetween
description: PrimeTween high-performance tweening library patterns for animations, UI, and sequencing.
---

# PrimeTween

## Overview

PrimeTween is a high-performance tweening library for Unity with zero allocations and excellent performance. This skill covers common patterns for UI animations, gameplay effects, and sequencing.

## When to Use

- UI animations (fade, scale, move)
- Gameplay animations (damage numbers, pickups)
- Camera effects
- Value interpolation
- Complex animation sequences

## Basic Tweens

### Transform Tweens

```csharp
using PrimeTween;

public class TransformAnimator : MonoBehaviour
{
    public void MoveToPosition(Vector3 target, float duration)
    {
        Tween.Position(transform, target, duration);
    }
    
    public void MoveWithEase(Vector3 target, float duration, Ease ease)
    {
        Tween.Position(transform, target, duration, ease);
    }
    
    public void ScalePunch()
    {
        Tween.Scale(transform, 1.2f, 0.1f, Ease.OutQuad)
            .Chain(Tween.Scale(transform, 1f, 0.2f, Ease.OutElastic));
    }
    
    public void Rotate360(float duration)
    {
        Tween.Rotation(transform, Quaternion.Euler(0, 360, 0), duration)
            .SetRelative();
    }
    
    public void ShakePosition(float intensity, float duration)
    {
        Tween.ShakeLocalPosition(transform, intensity, duration);
    }
}
```

### UI Tweens

```csharp
public class UIAnimator : MonoBehaviour
{
    [SerializeField] private CanvasGroup _canvasGroup;
    [SerializeField] private RectTransform _rectTransform;
    
    public Tween FadeIn(float duration = 0.3f)
    {
        _canvasGroup.alpha = 0f;
        return Tween.Alpha(_canvasGroup, 1f, duration, Ease.OutQuad);
    }
    
    public Tween FadeOut(float duration = 0.2f)
    {
        return Tween.Alpha(_canvasGroup, 0f, duration, Ease.InQuad);
    }
    
    public Tween SlideIn(Vector2 fromOffset, float duration = 0.3f)
    {
        Vector2 targetPos = _rectTransform.anchoredPosition;
        _rectTransform.anchoredPosition = targetPos + fromOffset;
        return Tween.UIAnchoredPosition(_rectTransform, targetPos, duration, Ease.OutCubic);
    }
    
    public Tween PopIn(float duration = 0.4f)
    {
        _rectTransform.localScale = Vector3.zero;
        return Tween.Scale(_rectTransform, 1f, duration, Ease.OutBack);
    }
    
    public Tween PopOut(float duration = 0.2f)
    {
        return Tween.Scale(_rectTransform, 0f, duration, Ease.InBack);
    }
}
```

### Color Tweens

```csharp
public class ColorAnimator : MonoBehaviour
{
    [SerializeField] private SpriteRenderer _spriteRenderer;
    [SerializeField] private Image _image;
    
    public Tween FlashColor(Color flashColor, float duration = 0.2f)
    {
        Color originalColor = _spriteRenderer.color;
        return Tween.Color(_spriteRenderer, flashColor, duration / 2, Ease.OutQuad)
            .Chain(Tween.Color(_spriteRenderer, originalColor, duration / 2, Ease.InQuad));
    }
    
    public Tween FadeSprite(float targetAlpha, float duration)
    {
        return Tween.Alpha(_spriteRenderer, targetAlpha, duration);
    }
    
    public Tween FadeImage(float targetAlpha, float duration)
    {
        return Tween.Alpha(_image, targetAlpha, duration);
    }
}
```

## Sequences

### Basic Sequence

```csharp
public class SequenceAnimator : MonoBehaviour
{
    public Sequence PlayIntroSequence()
    {
        return Sequence.Create()
            .Chain(Tween.Scale(transform, 0f, 1f, 0.3f, Ease.OutBack))
            .Chain(Tween.Position(transform, Vector3.up * 2f, 0.5f, Ease.OutQuad))
            .Chain(Tween.Rotation(transform, Quaternion.Euler(0, 360, 0), 0.4f))
            .ChainDelay(0.2f)
            .Chain(Tween.Scale(transform, 1.2f, 0.1f))
            .Chain(Tween.Scale(transform, 1f, 0.2f, Ease.OutElastic));
    }
}
```

### Parallel Tweens in Sequence

```csharp
public class ComplexAnimator : MonoBehaviour
{
    [SerializeField] private CanvasGroup _canvasGroup;
    [SerializeField] private RectTransform _rectTransform;
    
    public Sequence SlideAndFadeIn()
    {
        Vector2 startPos = _rectTransform.anchoredPosition + Vector2.down * 100f;
        _rectTransform.anchoredPosition = startPos;
        _canvasGroup.alpha = 0f;
        
        return Sequence.Create()
            .Group(Tween.UIAnchoredPosition(_rectTransform, 
                _rectTransform.anchoredPosition + Vector2.up * 100f, 0.4f, Ease.OutCubic))
            .Group(Tween.Alpha(_canvasGroup, 1f, 0.3f, Ease.OutQuad));
    }
    
    public Sequence SlideAndFadeOut()
    {
        return Sequence.Create()
            .Group(Tween.UIAnchoredPosition(_rectTransform, 
                _rectTransform.anchoredPosition + Vector2.down * 100f, 0.3f, Ease.InCubic))
            .Group(Tween.Alpha(_canvasGroup, 0f, 0.2f, Ease.InQuad));
    }
}
```

### Looping Sequences

```csharp
public class LoopingAnimator : MonoBehaviour
{
    private Sequence _idleSequence;
    
    public void StartIdleAnimation()
    {
        _idleSequence = Sequence.Create(cycles: -1) // -1 = infinite
            .Chain(Tween.Scale(transform, 1.05f, 1f, Ease.InOutSine))
            .Chain(Tween.Scale(transform, 1f, 1f, Ease.InOutSine));
    }
    
    public void StopIdleAnimation()
    {
        _idleSequence?.Stop();
        _idleSequence = null;
    }
    
    private void OnDisable()
    {
        StopIdleAnimation();
    }
}
```

## Value Tweens

### Custom Value Interpolation

```csharp
public class ValueTweener : MonoBehaviour
{
    private float _currentValue;
    
    public Tween TweenValue(float from, float to, float duration, Action<float> onUpdate)
    {
        _currentValue = from;
        return Tween.Custom(from, to, duration, value =>
        {
            _currentValue = value;
            onUpdate?.Invoke(value);
        });
    }
    
    public Tween TweenHealth(float targetHealth, float duration)
    {
        var healthBar = GetComponent<HealthBar>();
        float startHealth = healthBar.CurrentHealth;
        
        return Tween.Custom(startHealth, targetHealth, duration, value =>
        {
            healthBar.SetHealth(value);
        }, Ease.OutQuad);
    }
}
```

### Vector Interpolation

```csharp
public class VectorTweener : MonoBehaviour
{
    public Tween TweenVector3(Vector3 from, Vector3 to, float duration, Action<Vector3> onUpdate)
    {
        return Tween.Custom(from, to, duration, onUpdate);
    }
    
    public Tween TweenBetweenPoints(Transform target, Vector3 start, Vector3 end, float duration)
    {
        return Tween.Custom(start, end, duration, pos =>
        {
            target.position = pos;
        }, Ease.InOutQuad);
    }
}
```

## Callbacks

### Tween Callbacks

```csharp
public class CallbackAnimator : MonoBehaviour
{
    public void AnimateWithCallbacks()
    {
        Tween.Position(transform, Vector3.up * 5f, 1f)
            .OnStart(() => Debug.Log("Started"))
            .OnUpdate(progress => Debug.Log($"Progress: {progress:P0}"))
            .OnComplete(() => Debug.Log("Completed"));
    }
    
    public async UniTask AnimateAsync()
    {
        await Tween.Scale(transform, 2f, 0.5f);
        Debug.Log("Scale complete");
        
        await Tween.Position(transform, Vector3.forward * 10f, 1f);
        Debug.Log("Move complete");
    }
    
    public void AnimateWithCancellation(CancellationToken ct)
    {
        Tween.Position(transform, Vector3.up * 5f, 1f)
            .OnComplete(() =>
            {
                if (!ct.IsCancellationRequested)
                {
                    // Continue with next action
                }
            });
    }
}
```

## Common Patterns

### Damage Number Animation

```csharp
public class DamageNumberAnimator : MonoBehaviour
{
    [SerializeField] private TMP_Text _text;
    [SerializeField] private CanvasGroup _canvasGroup;
    [SerializeField] private RectTransform _rectTransform;
    
    public void PlayDamageAnimation(int damage, bool isCrit)
    {
        _text.text = damage.ToString();
        _canvasGroup.alpha = 1f;
        
        float scale = isCrit ? 1.5f : 1f;
        float duration = isCrit ? 1.2f : 0.8f;
        
        Sequence.Create()
            // Pop in
            .Chain(Tween.Scale(_rectTransform, 0f, scale * 1.2f, 0.1f, Ease.OutQuad))
            .Chain(Tween.Scale(_rectTransform, scale, 0.1f, Ease.OutElastic))
            // Float up
            .Group(Tween.UIAnchoredPositionY(_rectTransform, 
                _rectTransform.anchoredPosition.y + 100f, duration, Ease.OutQuad))
            // Fade out at end
            .Insert(duration * 0.6f, Tween.Alpha(_canvasGroup, 0f, duration * 0.4f))
            .OnComplete(() => gameObject.SetActive(false));
    }
}
```

### Button Press Animation

```csharp
public class ButtonAnimator : MonoBehaviour
{
    [SerializeField] private RectTransform _buttonRect;
    
    private Vector3 _originalScale;
    private Tween _currentTween;
    
    private void Awake()
    {
        _originalScale = _buttonRect.localScale;
    }
    
    public void OnPointerDown()
    {
        _currentTween?.Stop();
        _currentTween = Tween.Scale(_buttonRect, _originalScale * 0.9f, 0.1f, Ease.OutQuad);
    }
    
    public void OnPointerUp()
    {
        _currentTween?.Stop();
        _currentTween = Tween.Scale(_buttonRect, _originalScale, 0.15f, Ease.OutBack);
    }
    
    public void OnClick()
    {
        _currentTween?.Stop();
        _currentTween = Sequence.Create()
            .Chain(Tween.Scale(_buttonRect, _originalScale * 1.1f, 0.1f, Ease.OutQuad))
            .Chain(Tween.Scale(_buttonRect, _originalScale, 0.2f, Ease.OutElastic));
    }
}
```

### Screen Shake

```csharp
public class ScreenShaker : MonoBehaviour
{
    [SerializeField] private Transform _cameraTransform;
    
    private Vector3 _originalPosition;
    private Tween _shakeTween;
    
    private void Awake()
    {
        _originalPosition = _cameraTransform.localPosition;
    }
    
    public void Shake(float intensity = 0.5f, float duration = 0.3f)
    {
        _shakeTween?.Stop();
        _cameraTransform.localPosition = _originalPosition;
        
        _shakeTween = Tween.ShakeLocalPosition(_cameraTransform, intensity, duration)
            .OnComplete(() => _cameraTransform.localPosition = _originalPosition);
    }
    
    public void ImpactShake()
    {
        Shake(0.8f, 0.2f);
    }
    
    public void ContinuousShake(float intensity = 0.3f)
    {
        _shakeTween?.Stop();
        _shakeTween = Tween.ShakeLocalPosition(_cameraTransform, intensity, 99f, cycles: -1);
    }
    
    public void StopShake()
    {
        _shakeTween?.Stop();
        _cameraTransform.localPosition = _originalPosition;
    }
}
```

### Pickup Collection Animation

```csharp
public class PickupAnimator : MonoBehaviour
{
    public void AnimateCollection(Transform pickup, Transform target, Action onComplete)
    {
        Sequence.Create()
            // Initial bounce
            .Chain(Tween.Scale(pickup, 1.3f, 0.1f, Ease.OutQuad))
            .Chain(Tween.Scale(pickup, 1f, 0.1f))
            // Fly to target
            .Chain(Tween.Position(pickup, target.position, 0.4f, Ease.InQuad))
            .Group(Tween.Scale(pickup, 0f, 0.4f, Ease.InQuad))
            .OnComplete(() =>
            {
                onComplete?.Invoke();
                Destroy(pickup.gameObject);
            });
    }
}
```

## Performance Tips

### Pooling Tweens

```csharp
public class TweenPooling : MonoBehaviour
{
    // PrimeTween pools internally, but avoid creating many simultaneous tweens
    
    private Tween _reusableTween;
    
    public void UpdateValue(float target)
    {
        // Stop existing before creating new
        _reusableTween?.Stop();
        _reusableTween = Tween.Custom(
            getter: () => _currentValue,
            setter: v => _currentValue = v,
            endValue: target,
            duration: 0.3f
        );
    }
    
    private float _currentValue;
}
```

### Batch Operations

```csharp
public class BatchAnimator : MonoBehaviour
{
    [SerializeField] private Transform[] _items;
    
    public void AnimateAllItems()
    {
        // Create sequence for batching
        var sequence = Sequence.Create();
        
        for (int i = 0; i < _items.Length; i++)
        {
            float delay = i * 0.05f;
            
            sequence.Insert(delay, 
                Tween.Scale(_items[i], 0f, 1f, 0.3f, Ease.OutBack));
        }
    }
}
```

## Best Practices

1. **Stop tweens before creating new** - Prevent overlap
2. **Cache references** to tweens for stopping
3. **Use sequences** for complex animations
4. **Choose appropriate easing** for motion type
5. **Clean up in OnDisable** - Stop ongoing tweens
6. **Use async/await** for sequential logic
7. **Batch related animations** in sequences
8. **Profile tween count** - Keep reasonable limits
9. **Use Group for parallel** animations
10. **Test with time scale** changes

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tween not playing | Check if object is active |
| Overlapping animations | Stop previous tween first |
| Memory issues | Reduce simultaneous tweens |
| Unexpected position | Check relative vs absolute |
| Sequence not completing | Verify all tweens are valid |
| Callbacks not firing | Check if tween was stopped |
