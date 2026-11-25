---
name: flutter-theming
description: Tema y diseño visual de la app Flutter — `ThemeData` con Material 3, `ColorScheme.fromSeed`, tokens de color y tipografía, modo claro/oscuro, contraste WCAG AA, paridad con el design system web, y responsive por breakpoints con `MediaQuery`/`LayoutBuilder`. Usar al definir o revisar el tema de la app, al agregar un color o un estilo de texto, al implementar modo oscuro, o al alinear la app móvil con la identidad visual del producto web.
---

# Tema y diseño — Flutter

Un solo `ThemeData` por modo (claro y oscuro). Los widgets consumen el tema con
`Theme.of(context)`; **nunca** colores ni tamaños literales dispersos por el árbol. Es el
equivalente móvil de los tokens de `frontend-design-system`: alineá nombres y valores con él.

## 1. ColorScheme y Material 3

- Material 3 es el default vigente (`useMaterial3: true` ya no hace falta declararlo en versiones
  actuales; verificá en la versión del proyecto). Trabajá siempre sobre `ColorScheme`.
- Derivá el esquema de un color de marca con `ColorScheme.fromSeed`, y ajustá los roles que la
  identidad exija:

```dart
final light = ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: brandSeed, brightness: Brightness.light),
  textTheme: appTextTheme,
);
final dark = ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: brandSeed, brightness: Brightness.dark),
  textTheme: appTextTheme,
);
MaterialApp(theme: light, darkTheme: dark, themeMode: ThemeMode.system, ...);
```

- Usá los **roles** del esquema (`primary`, `onPrimary`, `surface`, `onSurface`, `error`,
  `outline`…), no `Colors.blue`. El par `X`/`onX` garantiza contraste del contenido sobre el fondo.

## 2. Tokens y `ThemeExtension`

- Para tokens que no entran en `ColorScheme`/`TextTheme` (superficies de marca, radios, espaciados,
  colores semánticos extra), definí un `ThemeExtension` propio en vez de constantes globales sueltas.
- Espaciado en una escala fija (4/8) expuesta como tokens; radios y elevaciones consistentes.

## 3. Tipografía

- Definí un `TextTheme` con la jerarquía (display/headline/title/body/label) y consumilo con
  `Theme.of(context).textTheme.titleLarge`. No `TextStyle(fontSize: 17)` a mano en cada pantalla.
- Alineá familias y escala con la web (ver `typography-systems`). Cargá fuentes vía `pubspec`
  (o `google_fonts`, verificá el paquete). Respetá `MediaQuery.textScaler`: no fijes tamaños que
  se rompan al agrandar el texto del sistema.
- Números tabulares para tablas/dinero (`fontFeatures: [FontFeature.tabularFigures()]`).

## 4. Modo claro/oscuro

- Ambos modos son de primera clase: probá cada pantalla en los dos. El oscuro no es invertir
  colores; usá superficies elevadas correctas (M3 sube el tono con la elevación).
- No hardcodees blanco/negro: `onSurface`/`surface` se adaptan solos.
- Respetá `ThemeMode.system` salvo que el producto ofrezca conmutador propio.

## 5. Contraste WCAG AA

- Texto normal **4.5:1**, texto grande y componentes/íconos **3:1** (mismos umbrales que web).
- Verificá los pares reales sobre el color de fondo. En Dart, la luminancia sale de
  `Color.computeLuminance()`; el ratio de contraste es `(Lmax + 0.05) / (Lmin + 0.05)`.
- Automatizalo: un test que recorra los pares del tema y falle si un par baja del umbral es la
  mejor red (ver `flutter-testing`). No confíes solo en el ojo.

## 6. Responsive

- Adaptá por ancho disponible con `LayoutBuilder`, y usá `MediaQuery` para safe areas, orientación
  y `textScaler`. Breakpoints guiados por contenido, no por dispositivo.
- Móvil vs tablet: reflujo de una a dos columnas, listas maestro-detalle en pantalla ancha.
- No asumas tamaño de pantalla fijo ni pixeles físicos: trabajá en dp lógicos.

## Anti-patrones
- `Colors.*` o hex literales fuera del tema.
- `TextStyle` con `fontSize` a mano repartidos por las pantallas.
- Modo oscuro "arreglado" con `if (isDark)` disperso en los widgets.
- Blanco/negro fijos que rompen contraste en un modo.

## Checklist
- [ ] Un `ThemeData` por modo; los widgets leen del tema, sin literales.
- [ ] Colores por rol del `ColorScheme` (par `X`/`onX`), no por nombre de color.
- [ ] Tokens extra en `ThemeExtension`; espaciado/tipografía en escala alineada con la web.
- [ ] Probado en claro y oscuro y con fuente del sistema agrandada.
- [ ] Contraste AA verificado sobre los pares reales (idealmente por test).
- [ ] Layout adaptado por `LayoutBuilder`/`MediaQuery`, no por dispositivo fijo.
