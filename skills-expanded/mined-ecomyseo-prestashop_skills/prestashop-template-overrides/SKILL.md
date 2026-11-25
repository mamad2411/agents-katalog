---
name: prestashop-template-overrides
description: Skill para sobrescribir templates del Back Office y Front Office de PrestaShop 8/9 desde modulos.
---

# PrestaShop Template Overrides Skill (PS 8 / PS 9)

Este skill explica como un modulo puede sobrescribir templates core de Symfony sin modificar archivos del core.

## 1. Guia Tecnica

### Sobrescribir Templates Symfony (Back Office)

PrestaShop 8/9 usa Symfony 4.4/6.4. La sintaxis de referencia de templates es:

```
@PrestaShop/Admin/path/to/template.html.twig
```

> **IMPORTANTE**: NO usar la sintaxis legacy `PrestaShopBundle:Admin:template.html.twig` (Symfony 2/3). Esta **NO funciona** en PS 8/9.

Para sobrescribir un template del core desde un modulo, colocar el archivo en:
```
modules/mymodule/views/PrestaShop/Admin/[path]/[template].html.twig
```

Ejemplo: Para sobrescribir la vista de clientes:
```
mymodule/views/PrestaShop/Admin/Sell/Customer/index.html.twig
```

### Extension de Templates
En lugar de reemplazar el archivo completo, extender el template core y sobrescribir solo bloques especificos.

```twig
{# views/PrestaShop/Admin/Sell/Customer/index.html.twig #}
{% extends '@PrestaShop/Admin/Sell/Customer/index.html.twig' %}

{% block content %}
    <div class="alert alert-info">Hello from My Module!</div>
    {{ parent() }}
{% endblock %}
```

### Front Office (Smarty y Twig)
Para sobrescribir templates de front-office desde un modulo:

**Tema Classic (Smarty)**:
```
modules/mymodule/views/templates/front/*.tpl
```

**Tema Hummingbird (Twig, PS 8.1+/PS 9)**:
```
modules/mymodule/views/templates/front/*.html.twig
```

## 2. Guia de Desarrollo

### Convenciones
- Verificar siempre la ruta exacta del bundle core. En PS 8/9, todo esta bajo `PrestaShopBundle`.
- La ruta en tu modulo debe reflejar EXACTAMENTE la ruta en el core.

### Hooks en lugar de Overrides
Siempre que sea posible, usar hooks (`displayDashboardTop`, `displayAdminProductsExtra`) en lugar de sobrescribir templates para asegurar maxima compatibilidad con otros modulos.

### Diferencias PS 8 vs PS 9
| Aspecto | PS 8 (Sf 4.4) | PS 9 (Sf 6.4) |
|---------|---------------|---------------|
| Sintaxis Twig | `@PrestaShop/Admin/...` | `@PrestaShop/Admin/...` |
| Front-office Classic | Smarty (.tpl) | Smarty (.tpl) |
| Front-office Hummingbird | Twig (PS 8.1+) | Twig (por defecto) |

## 3. Guia de Usuario

### Requisitos
- Limpiar la cache despues de añadir un template override en **Parametros Avanzados > Rendimiento**.
- Si el override no tiene efecto, verificar que el modulo esta instalado y activado.

## Reglas y Buenas Practicas
- **Cambios Atomicos**: Solo sobrescribir los bloques necesarios.
- **Actualizaciones**: La estructura de templates core puede cambiar entre versiones. Verificar overrides en cada actualizacion.
- **Seguridad**: No eliminar bloques esenciales del core (tokens de formulario, campos de seguridad).
- **Traducciones en Twig**: Usar `{{ 'My text'|trans({}, 'Modules.Mymodule.Admin') }}`.
