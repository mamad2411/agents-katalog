---
name: ui-design-a11y
description: |
  无障碍设计审查与修复能力。
  当用户说"无障碍"、"a11y"、"WCAG"、"键盘导航"、"屏幕阅读器"、"颜色对比度"、"ARIA"、"可访问性"、"辅助功能"、"盲人友好"时使用此技能。
  基于 WCAG 2.1 标准，检测图片 Alt 文本缺失、表单 Label 关联、键盘可访问性、颜色对比度不足、ARIA 属性误用等问题。
  提供修复代码示例：语义化标签、焦点管理、焦点陷阱、屏幕阅读器支持。输出合规性检查报告和修复建议。
disable-model-invocation: false
---

# Accessibility (A11y) Skill

## 技能描述
专注于 Web 无障碍标准 (WCAG) 的检查与修复。帮助开发者发现潜在的访问性问题并提供修复代码。

## 📝 代码示例

### 1. 图片无障碍

```tsx
// ✅ 正确的图片无障碍实现
function AccessibleImage({ src, alt, caption }: ImageProps) {
  return (
    <figure>
      <img
        src={src}
        alt={alt} // 描述性文字，装饰性图片使用 alt=""
        loading="lazy"
      />
      {caption && <figcaption>{caption}</figcaption>}
    </figure>
  );
}

// ❌ 避免
<img src="photo.jpg" /> // 缺少 alt
<img src="photo.jpg" alt="image" /> // 无意义的 alt
```

### 2. 表单无障碍

```tsx
// ✅ 正确的表单关联
function AccessibleForm() {
  return (
    <form>
      <div>
        <label htmlFor="email">邮箱地址</label>
        <input
          id="email"
          type="email"
          aria-describedby="email-hint"
          aria-required="true"
        />
        <span id="email-hint">我们会向此邮箱发送验证码</span>
      </div>

      <div>
        <label htmlFor="password">密码</label>
        <input
          id="password"
          type="password"
          aria-describedby="password-error"
          aria-invalid={hasError ? 'true' : 'false'}
        />
        {hasError && (
          <span id="password-error" role="alert">
            密码至少需要8个字符
          </span>
        )}
      </div>

      <button type="submit">登录</button>
    </form>
  );
}
```

### 3. 键盘导航

```tsx
// ✅ 可键盘操作的按钮
function AccessibleButton({ onClick, children }: ButtonProps) {
  return (
    <button
      onClick={onClick}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick();
        }
      }}
    >
      {children}
    </button>
  );
}

// ✅ 焦点管理样式
const focusStyles = css`
  &:focus-visible {
    outline: 3px solid #005fcc;
    outline-offset: 2px;
  }
`;
```

### 4. 模态框焦点陷阱

```tsx
// ✅ 模态框无障碍实现
function AccessibleModal({ isOpen, onClose, title, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousActiveElement = useRef<Element | null>(null);

  useEffect(() => {
    if (isOpen) {
      previousActiveElement.current = document.activeElement;
      modalRef.current?.focus();
      document.body.style.overflow = 'hidden';
    } else {
      previousActiveElement.current?.focus();
      document.body.style.overflow = '';
    }
  }, [isOpen]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') onClose();
  };

  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      ref={modalRef}
      tabIndex={-1}
      onKeyDown={handleKeyDown}
    >
      <div className="modal-backdrop" onClick={onClose} aria-hidden="true" />
      <div className="modal-content">
        <h2 id="modal-title">{title}</h2>
        {children}
        <button onClick={onClose} aria-label="关闭对话框">
          <CloseIcon />
        </button>
      </div>
    </div>
  );
}
```

### 5. 颜色对比度

```css
/* ✅ 符合 WCAG AA 标准的对比度 */
.text-primary {
  color: #1a1a1a; /* 与白色背景对比度 > 12:1 */
}

.text-secondary {
  color: #4a4a4a; /* 与白色背景对比度 > 7:1 */
}

/* ✅ 不只依赖颜色传达信息 */
.status-success {
  color: #0a8754;
}
.status-success::before {
  content: '✓ '; /* 同时使用图标 */
}

/* ✅ 聚焦状态清晰可见 */
:focus-visible {
  outline: 3px solid #005fcc;
  outline-offset: 2px;
}
```

### 6. ARIA 地标与语义化

```tsx
// ✅ 语义化页面结构
function AccessibleLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <header role="banner">
        <nav aria-label="主导航">
          <ul>
            <li><a href="/">首页</a></li>
            <li><a href="/about">关于</a></li>
          </ul>
        </nav>
      </header>

      <main role="main" id="main-content">
        <h1>页面标题</h1>
        {children}
      </main>

      <aside aria-label="侧边栏">
        {/* 侧边栏内容 */}
      </aside>

      <footer role="contentinfo">
        {/* 页脚内容 */}
      </footer>
    </>
  );
}
```

## ♿ 常用指令

### 1. 快速审查 (Audit)
```bash
/ui-design 审查这段代码的无障碍问题
# 关注点:
# - 语义化标签 (nav, main, aside)
# - ARIA 属性使用
# - 键盘可访问性 (tabindex, focus)
# - 图片 Alt 文本
```

### 2. 对比度检查 (Contrast)
```bash
/ui-design 检查这个配色的对比度是否符合 WCAG AA 标准
```

### 3. 修复建议 (Fix)
```bash
/ui-design 修复这个表单的 Label 关联和 ARIA 描述问题
/ui-design 为这个模态框添加 Focus Trap (焦点陷阱) 功能
```

## ✅ Self-Checklist (自查清单)

在提交代码前，请检查：
- [ ] 所有的 `<img>` 都有 `alt` 属性吗？
- [ ] 所有的表单输入框都有对应的 `<label>` 吗？
- [ ] 按钮是否有清晰的文字描述（避免仅图标）？
- [ ] 页面是否可以仅用键盘顺畅操作？
- [ ] 颜色对比度是否足够清晰？
