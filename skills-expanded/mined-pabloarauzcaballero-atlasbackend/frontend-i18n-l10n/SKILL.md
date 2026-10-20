---
name: frontend-i18n-l10n
description: Internacionalización y localización del frontend — marcar texto con i18n de Angular (`$localize`, atributo `i18n`), extraer con `ng extract-i18n`, plurales y selección por género con ICU, formato de fecha/número/moneda por locale, soporte RTL, y no concatenar strings traducibles. Usar al agregar cualquier texto visible, al preparar el producto para un segundo idioma o región, al formatear fechas/montos, o al revisar por qué una traducción quedó rota o antinatural.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# i18n / l10n — frontend

Internacionalizar es separar el texto y los formatos del código para que se traduzcan sin
tocar la lógica. Hacerlo desde el inicio cuesta poco; retrofitearlo cuesta muchísimo.

## 1. Marcar todo texto visible

- Ningún string visible al usuario va hardcodeado suelto en template o TS.
- En templates, el atributo `i18n` (con meaning/description opcional). En código, `$localize`.
- Dale contexto al traductor con `meaning|description@@id`: el mismo texto puede traducirse
  distinto según dónde aparezca.

```html
<h1 i18n="page title|Encabezado del directorio@@directoryTitle">Directorio de profesionales</h1>
<img [src]="avatar" i18n-alt alt="Foto de perfil" />
```

```typescript
const msg = $localize`:@@apptConfirmed:Tu cita fue confirmada`;
```

Extraé el catálogo con `ng extract-i18n --format=xlf2 --out-file=messages.xlf` y entregá ese
archivo a traducción; nunca traduzcas editando el código fuente.

## 2. No concatenar — usar placeholders e ICU

Concatenar rompe idiomas con otro orden de palabras o género. Usá interpolación con
placeholders nombrados y expresiones ICU para plurales y selección.

```html
<!-- ❌ concatenado: intraducible a idiomas con otro orden/género -->
<span>{{ count }} resultados encontrados</span>

<!-- ✅ ICU: el traductor controla cada forma -->
<span i18n>{count, plural, =0 {Sin resultados} =1 {1 resultado} other {{{count}} resultados}}</span>
<span i18n>{gender, select, female {Doctora} male {Doctor} other {Profesional}} disponible</span>
```

## 3. Formatear con la API de la plataforma, por locale

Fechas, números y moneda se formatean según el locale, no a mano. Usá los pipes de Angular
(`date`, `number`, `currency`, `percent`) o `Intl.*`. Registrá los datos de locale que uses.

```html
<td>{{ amount | currency:'BOB':'symbol':'1.2-2' }}</td>
<td>{{ createdAt | date:'medium' }}</td>
```

- Fechas: guardá y transportá en UTC/ISO; formateá en la zona del usuario en la vista.
- Números: separador decimal y de miles cambian por locale; nunca los pongas literales.
- No asumas el formato del país del desarrollador.

## 4. RTL (derecha-a-izquierda)

- Usá propiedades lógicas: `margin-inline-start`, `padding-inline`, `inset-inline`, `text-align: start`
  en vez de `left`/`right`. Así el layout se espeja solo cuando `dir="rtl"`.
- Iconos direccionales (flechas de "siguiente/atrás") deben espejarse; los no direccionales, no.
- Probá con `dir="rtl"` en el `<html>`.

## 5. SSR

Bajo SSR el texto se resuelve en el servidor; asegurate de que el locale correcto se aplique
en el render del servidor y no cambie al hidratar. Cada locale
suele ser su propio build/despliegue en el enfoque de compilación.

## Anti-patrones

- Texto visible hardcodeado sin marcar.
- Concatenar fragmentos traducibles (`'Hola ' + name + ', tenés ' + n + ' citas'`).
- Formatear fecha/número/moneda con `slice`/`replace` a mano.
- `left`/`right` fijos que rompen RTL.
- Traducir editando el código en vez del catálogo extraído.

## Checklist

- [ ] Todo string visible marcado con `i18n`/`$localize`, con id y contexto.
- [ ] Plurales y género con ICU; cero concatenación de traducibles.
- [ ] Fechas en UTC, formateadas por locale en la vista; números y moneda por pipe/`Intl`.
- [ ] Propiedades lógicas para que el layout soporte RTL; iconos direccionales espejables.
- [ ] Catálogo extraído con `ng extract-i18n`; traducción sobre el catálogo, no el código.
- [ ] Locale correcto bajo SSR sin cambio al hidratar.
