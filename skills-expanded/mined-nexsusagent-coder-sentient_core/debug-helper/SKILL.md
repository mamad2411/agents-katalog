# Debug Helper Skill

SENTIENT'nın AI destekli hata ayıklama yeteneği.

## Özellikler

Bu skill, lisa-agentic'in reflection pattern'inden ve OpenHarness'ın hata çözümleme mantığından adapte edilmiştir.

### Desteklenen Hata Türleri

| Tür | Açıklama | Örnek |
|-----|----------|-------|
| **Compile** | Derleme hataları | `cannot find value`, `type mismatch` |
| **Runtime** | Çalışma zamanı hataları | `panic!`, `unwrap on None` |
| **Logic** | Mantık hataları | Yanlış sonuç, sonsuz döngü |
| **Memory** | Bellek hataları | `use after free`, leak |
| **Network** | Ağ hataları | Timeout, connection refused |

### Süreç

```
┌────────────────────────────────────────┐
│  1. Error Analysis                     │
│     └─> Stack trace parse              │
│     └─> Error pattern match            │
├────────────────────────────────────────┤
│  2. Root Cause Detection               │
│     └─> Code context analysis          │
│     └─> Historical pattern lookup      │
├────────────────────────────────────────┤
│  3. Fix Generation                     │
│     └─> AI-powered suggestion          │
│     └─> Confidence scoring             │
├────────────────────────────────────────┤
│  4. Validation                         │
│     └─> Syntax check                   │
│     └─> Type check                     │
└────────────────────────────────────────┘
```

### Kullanım

```bash
# Compile hatası
sentient skill run debug-helper \
  --error-type compile \
  --error-message "cannot find value \`x\` in this scope"

# Runtime hatası
sentient skill run debug-helper \
  --error-type runtime \
  --error-message "thread 'main' panicked at 'called unwrap on None'"
```

### Örnek Çıktı

```json
{
  "root_cause": "Variable `x` is defined inside a block scope and not accessible outside",
  "fix_suggestion": "Move `x` declaration outside the block or return it from the block",
  "code_patch": "let x = ...; // Move outside block",
  "confidence": 92
}
```

---
*SENTIENT - The She-Wolf That Guards Your Empire*
