# Testing de Accesibilidad

Criterios WCAG 2.1 nivel AA para casos de prueba de accesibilidad.

## Checklist por tipo de elemento

### Imágenes
- Toda `<img>` informativa tiene atributo `alt` descriptivo
- Imágenes decorativas tienen `alt=""` o `role="presentation"`

### Formularios
- Todo input tiene `<label>` asociado via `for/id` o `aria-label`
- Errores de validación son anunciados con `aria-live` o `role="alert"`
- Campos requeridos indicados con `aria-required="true"` y visualmente

### Navegación por teclado
- Todo elemento interactivo es alcanzable con Tab
- No hay "trampas de teclado"
- El orden de foco sigue la lectura visual izquierda→derecha, arriba→abajo

### Contraste
- Texto normal: ratio mínimo 4.5:1
- Texto grande (≥18pt o ≥14pt bold): ratio mínimo 3:1
- Iconos y bordes informativos: ratio mínimo 3:1

### ARIA
- No usar ARIA donde hay elemento HTML semántico equivalente
- `aria-label` en elementos sin texto visible (botones con sólo icono)
- No duplicar información visible en aria-label

## Tags para casos de accesibilidad
- `@a11y` en todos los casos de prueba de accesibilidad
- `@wcag-AA` para cobertura mínima del nivel AA
