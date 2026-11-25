---
name: prestashop_validator
description: Local version of the PrestaShop Validator tool to check module structure, security, and standards.
---

# PrestaShop Validator (Global Skill)

This skill allows you to run a complete validation of a PrestaShop module directly on the user's file system, replicating the checks performed by the official validator.prestashop.com.

## Capability
- **Structure Check**: Verifies existence of `config.xml`, `logo.png`, and recursive `index.php`.
- **Security Check**: Scans for forbidden functions (`eval`, `dump`, `var_dump`, etc.).
- **Standards Check**: Verifies License Headers, `_PS_VERSION_` security tokens.
- **Auto-Fix**: Can automatically create missing `index.php` files and insert missing security tokens or disable `strict_types`.

## Usage

### 1. Validate a Module
To validate a module located at a specific path:

```bash
php "<skills>/prestashop-validator/validator.php" --path="Z:/path/to/your/module"
```

### Context Awareness
If the user asks to validate **"the current module"**, **"this folder"**, or **"here"**:
1. **Identify the module path**: Look at the user's **currently open files** or the **active workspace URI**.
   - Example: If the user is editing `z:/modules/my_module/my_module.php`, the path is `z:/modules/my_module`.
2. **Execute**: Run the command using that determined absolute path.

### 2. Validate and Fix
To validate and automatically apply fixes (missing index.php, missing security tokens):

```bash
php "<skills>/prestashop-validator/validator.php" --path="Z:/path/to/your/module" --fix
```

## When to use
Use this skill whenever:
- The user asks to "validate" the module.
- Before finishing a task to ensure the module is clean.
- When the user mentions "PrestaShop Validator" or "Standard compliance".

## ⚠️ VALIDACIÓN ADICIONAL (PHP 7.4 & AJAX)
Además de los checks estructurales, el validador debe asegurar:
1. **AJAX Security**: Los controladores AJAX DEBEN sobrescribir `checkAccess()` y `checkToken()` para retornar `true`.
2. **PHP 7.4 Compatibility**: Prohibir el uso de `::class` en objetos dinámicos. En su lugar, usar `get_class()`.
3. **Escapado Contextual**: Verificar que `\Context::getContext()` use el backslash inicial en clases de lógica.
4. **AJAX Persistence (Batería Completa)**: Los scripts deben suscribirse a `updateProduct`, `updatedProduct` y `updatedCart` con delay reactivo. Ver `prestashop-ajax-lifecycle`.

## Location
This global skill is permanently installed at:
`<skills>\prestashop-validator\`
