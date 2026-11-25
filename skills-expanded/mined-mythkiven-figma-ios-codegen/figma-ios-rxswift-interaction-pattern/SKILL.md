---
name: figma-ios-rxswift-interaction-pattern
description: >-
  项目中使用 RxSwift + RxCocoa 处理 UI 交互事件（按钮点击、手势等）的标准模式。
  Use when generating UI interaction code, button actions, or when user mentions RxSwift、RxCocoa、响应式。
---

# 交互模式（默认示例：target-action；Rx 仅当 host.interaction=rxswift）

> 以 `host.json` → `interaction` 为准。`target_action` 用下方「传统写法」；仅配置为 `rxswift` 时用 Rx 示例。  
> **不要**强制写 `import`；需要 Rx 时由生成代码按工程依赖自行引入。

## 传统写法（host.interaction = target_action，默认）

```swift
button.addTarget(self, action: #selector(onTap), for: .touchUpInside)

@objc private func onTap() {
    // ...
}
```

## Rx 写法（仅 host.interaction = rxswift）

依赖与 import 由宿主工程已具备时再使用，skill **不强制**写死：

## 标准写法

### 1. 在 ViewController 或 View 中声明 DisposeBag

```swift
import UIKit
import RxSwift
import RxCocoa

class AppDemoViewController: UIViewController {
    private let disposeBag = DisposeBag()
    
    // ...
}
```

### 2. 按钮点击事件

```swift
private func setupBindings() {
    submitButton.rx.tap
        .subscribe(onNext: { [weak self] in
            self?.handleSubmitTapped()
        })
        .disposed(by: disposeBag)
}
```

### 3. 手势事件

```swift
let tapGesture = UITapGestureRecognizer()
view.addGestureRecognizer(tapGesture)

tapGesture.rx.event
    .subscribe(onNext: { [weak self] _ in
        self?.handleTapped()
    })
    .disposed(by: disposeBag)
```

### 4. UITextField / UITextView 文本变化

```swift
textField.rx.text.orEmpty
    .subscribe(onNext: { [weak self] text in
        self?.handleTextChanged(text)
    })
    .disposed(by: disposeBag)
```

### 5. UIControl 通用事件

```swift
stepper.rx.controlEvent(.valueChanged)
    .subscribe(onNext: { [weak self] in
        self?.handleValueChanged()
    })
    .disposed(by: disposeBag)
```

## 与传统 target-action 的对比

### 传统写法（仍可用，但不推荐）
```swift
button.addTarget(self, action: #selector(handleTapped), for: .touchUpInside)

@objc private func handleTapped() {
    // ...
}
```

### RxSwift 写法（推荐）
```swift
button.rx.tap
    .subscribe(onNext: { [weak self] in
        self?.handleTapped()
    })
    .disposed(by: disposeBag)

private func handleTapped() {
    // ...
}
```

**优势**：
- 不需要 `@objc` 标记
- 事件绑定统一在 `setupBindings()` 中，清晰
- 支持链式操作（如防抖、合并多个事件等）

## 防抖与节流

### 防抖（debounce）- 避免频繁点击
```swift
button.rx.tap
    .debounce(.milliseconds(300), scheduler: MainScheduler.instance)
    .subscribe(onNext: { [weak self] in
        self?.handleSubmitTapped()
    })
    .disposed(by: disposeBag)
```

### 节流（throttle）- 限制频率
```swift
button.rx.tap
    .throttle(.seconds(1), scheduler: MainScheduler.instance)
    .subscribe(onNext: { [weak self] in
        self?.handleButtonTapped()
    })
    .disposed(by: disposeBag)
```

## 注意事项

1. **DisposeBag**：必须声明为实例属性，不要用局部变量（会导致订阅立即取消）
2. **[weak self]**：闭包中捕获 self 时始终用 `[weak self]`，避免循环引用
3. **线程**：UI 事件默认在主线程；若涉及后台任务，用 `.observeOn(MainScheduler.instance)` 切回主线程更新 UI

## 相关

- **总入口**：[figma-ios-playbook](../figma-ios-playbook/SKILL.md)
- **ViewController 基类 + 导航栏**：[figma-ios-navigation](../figma-ios-navigation/SKILL.md)
- **选中态交互逻辑**：[figma-ios-selection-interaction](../figma-ios-selection-interaction/SKILL.md)（使用本 Skill 的事件绑定模式实现选中态切换）
