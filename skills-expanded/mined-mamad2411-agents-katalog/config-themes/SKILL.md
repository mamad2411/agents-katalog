---
name: config-themes
description: Skill para implementar sistema de temas y personalización visual
---

# Skill: config-themes

## Propósito

Este skill genera un módulo de **Temas y Personalización Visual** que permite:

- Temas claros/oscuros dinámicos
- Colores personalizables por tenant
- Persistencia de preferencias
- Sistema de diseño unificado

---

## Variantes Disponibles

| Variante  | Descripción                                                 |
| --------- | ----------------------------------------------------------- |
| **basic** | Tema claro/oscuro con colores de marca                      |
| **full**  | Personalización completa por tenant + presets + exportación |

---

## Estructura de Archivos a Crear

```text
proyecto/
├── backend/
│   └── internal/
│       └── handlers/
│           └── settings.go (endpoints de tema)
└── frontend/
    └── lib/
        ├── core/
        │   └── theme/
        │       ├── app_theme.dart
        │       └── theme_provider.dart
        └── features/
            └── configuration/
                ├── data/
                │   └── models/
                │       └── theme_model.dart
                └── presentation/
                    └── widgets/
                        └── theme_settings_tab.dart
```

---

## Paso 1: Modelo de Tema

### Backend (Almacenado en tenant.settings o tabla separada)

```sql
-- En la tabla de tenants, el campo settings JSONB contiene:
{
  "theme": {
    "mode": "light",            -- "light", "dark", "system"
    "primary_color": "#1976D2",
    "secondary_color": "#FF9800",
    "tertiary_color": "#4CAF50",
    "font_family": "Inter",
    "border_radius": 8,
    "compact_mode": false
  }
}

-- O crear tabla dedicada:
CREATE TABLE public.theme_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES public.tenants(id) ON DELETE CASCADE UNIQUE,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    
    mode VARCHAR(20) DEFAULT 'system',  -- 'light', 'dark', 'system'
    primary_color VARCHAR(20) DEFAULT '#1976D2',
    secondary_color VARCHAR(20) DEFAULT '#FF9800',
    tertiary_color VARCHAR(20) DEFAULT '#4CAF50',
    
    font_family VARCHAR(50) DEFAULT 'Inter',
    border_radius INT DEFAULT 8,
    compact_mode BOOLEAN DEFAULT false,
    
    -- Presets personalizados
    custom_presets JSONB DEFAULT '[]',
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    -- Un registro por tenant O por usuario
    CONSTRAINT unique_tenant_theme UNIQUE (tenant_id),
    CONSTRAINT unique_user_theme UNIQUE (user_id)
);
```

---

## Paso 2: API Backend

### Endpoints

| Método | Ruta                        | Descripción                  |
| ------ | --------------------------- | ---------------------------- |
| GET    | /settings/theme             | Obtener tema actual          |
| PUT    | /settings/theme             | Actualizar tema              |
| GET    | /settings/theme/presets     | Listar presets disponibles   |
| POST   | /settings/theme/presets     | Guardar preset personalizado |
| DELETE | /settings/theme/presets/:id | Eliminar preset              |

### DTOs

```go
type ThemeSettings struct {
    Mode           string `json:"mode"`            // light, dark, system
    PrimaryColor   string `json:"primary_color"`
    SecondaryColor string `json:"secondary_color"`
    TertiaryColor  string `json:"tertiary_color,omitempty"`
    FontFamily     string `json:"font_family,omitempty"`
    BorderRadius   int    `json:"border_radius,omitempty"`
    CompactMode    bool   `json:"compact_mode,omitempty"`
}

type UpdateThemeRequest struct {
    PrimaryColor   string `json:"primary_color,omitempty"`
    SecondaryColor string `json:"secondary_color,omitempty"`
    TertiaryColor  string `json:"tertiary_color,omitempty"`
    LogoURL        string `json:"logo_url,omitempty"`
}

type ThemePreset struct {
    ID             string `json:"id"`
    Name           string `json:"name"`
    PrimaryColor   string `json:"primary_color"`
    SecondaryColor string `json:"secondary_color"`
    TertiaryColor  string `json:"tertiary_color"`
    IsDefault      bool   `json:"is_default,omitempty"`
}
```

---

## Paso 3: Modelo Flutter

```dart
/// Configuración de tema
class ThemeSettings {
  final ThemeMode mode;
  final Color primaryColor;
  final Color secondaryColor;
  final Color tertiaryColor;
  final String fontFamily;
  final double borderRadius;
  final bool compactMode;

  const ThemeSettings({
    this.mode = ThemeMode.system,
    this.primaryColor = const Color(0xFF1976D2),
    this.secondaryColor = const Color(0xFFFF9800),
    this.tertiaryColor = const Color(0xFF4CAF50),
    this.fontFamily = 'Inter',
    this.borderRadius = 8.0,
    this.compactMode = false,
  });

  factory ThemeSettings.fromJson(Map<String, dynamic> json) {
    return ThemeSettings(
      mode: _parsethemeMode(json['mode']),
      primaryColor: _parseColor(json['primary_color']) ?? const Color(0xFF1976D2),
      secondaryColor: _parseColor(json['secondary_color']) ?? const Color(0xFFFF9800),
      tertiaryColor: _parseColor(json['tertiary_color']) ?? const Color(0xFF4CAF50),
      fontFamily: json['font_family'] ?? 'Inter',
      borderRadius: (json['border_radius'] ?? 8).toDouble(),
      compactMode: json['compact_mode'] ?? false,
    );
  }

  Map<String, dynamic> toJson() => {
    'mode': mode.name,
    'primary_color': '#${primaryColor.value.toRadixString(16).padLeft(8, '0').substring(2)}',
    'secondary_color': '#${secondaryColor.value.toRadixString(16).padLeft(8, '0').substring(2)}',
    'tertiary_color': '#${tertiaryColor.value.toRadixString(16).padLeft(8, '0').substring(2)}',
    'font_family': fontFamily,
    'border_radius': borderRadius.toInt(),
    'compact_mode': compactMode,
  };

  ThemeSettings copyWith({
    ThemeMode? mode,
    Color? primaryColor,
    Color? secondaryColor,
    Color? tertiaryColor,
    String? fontFamily,
    double? borderRadius,
    bool? compactMode,
  }) {
    return ThemeSettings(
      mode: mode ?? this.mode,
      primaryColor: primaryColor ?? this.primaryColor,
      secondaryColor: secondaryColor ?? this.secondaryColor,
      tertiaryColor: tertiaryColor ?? this.tertiaryColor,
      fontFamily: fontFamily ?? this.fontFamily,
      borderRadius: borderRadius ?? this.borderRadius,
      compactMode: compactMode ?? this.compactMode,
    );
  }

  static ThemeMode _parsethemeMode(String? mode) {
    switch (mode) {
      case 'light': return ThemeMode.light;
      case 'dark': return ThemeMode.dark;
      default: return ThemeMode.system;
    }
  }

  static Color? _parseColor(String? hex) {
    if (hex == null || hex.isEmpty) return null;
    hex = hex.replaceFirst('#', '');
    if (hex.length == 6) hex = 'FF$hex';
    return Color(int.parse(hex, radix: 16));
  }
}

/// Preset de tema
class ThemePreset {
  final String id;
  final String name;
  final Color primaryColor;
  final Color secondaryColor;
  final Color tertiaryColor;
  final bool isDefault;

  const ThemePreset({
    required this.id,
    required this.name,
    required this.primaryColor,
    required this.secondaryColor,
    this.tertiaryColor = Colors.green,
    this.isDefault = false,
  });

  /// Presets predefinidos
  static List<ThemePreset> get defaultPresets => [
    ThemePreset(
      id: 'ocean',
      name: 'Océano',
      primaryColor: const Color(0xFF1976D2),
      secondaryColor: const Color(0xFF26C6DA),
      tertiaryColor: const Color(0xFF00897B),
    ),
    ThemePreset(
      id: 'forest',
      name: 'Bosque',
      primaryColor: const Color(0xFF2E7D32),
      secondaryColor: const Color(0xFF8BC34A),
      tertiaryColor: const Color(0xFF33691E),
    ),
    ThemePreset(
      id: 'sunset',
      name: 'Atardecer',
      primaryColor: const Color(0xFFE65100),
      secondaryColor: const Color(0xFFFFB300),
      tertiaryColor: const Color(0xFFD84315),
    ),
    ThemePreset(
      id: 'lavender',
      name: 'Lavanda',
      primaryColor: const Color(0xFF7B1FA2),
      secondaryColor: const Color(0xFFBA68C8),
      tertiaryColor: const Color(0xFF4A148C),
    ),
    ThemePreset(
      id: 'midnight',
      name: 'Medianoche',
      primaryColor: const Color(0xFF283593),
      secondaryColor: const Color(0xFF5C6BC0),
      tertiaryColor: const Color(0xFF1A237E),
    ),
    ThemePreset(
      id: 'rose',
      name: 'Rosa',
      primaryColor: const Color(0xFFC2185B),
      secondaryColor: const Color(0xFFF48FB1),
      tertiaryColor: const Color(0xFF880E4F),
    ),
  ];
}
```

---

## Paso 4: Theme Provider

```dart
class ThemeProvider extends ChangeNotifier {
  ThemeSettings _settings = const ThemeSettings();
  bool _isLoading = false;

  ThemeSettings get settings => _settings;
  bool get isLoading => _isLoading;

  ThemeMode get themeMode => _settings.mode;
  Color get primaryColor => _settings.primaryColor;
  Color get secondaryColor => _settings.secondaryColor;

  ThemeProvider() {
    _loadFromStorage();
  }

  /// Cargar configuración guardada
  Future<void> _loadFromStorage() async {
    final prefs = await SharedPreferences.getInstance();
    final json = prefs.getString('theme_settings');
    if (json != null) {
      _settings = ThemeSettings.fromJson(jsonDecode(json));
      notifyListeners();
    }
  }

  /// Sincronizar desde datos del tenant
  void syncFromTenant({
    String? primaryColor,
    String? secondaryColor,
    String? tertiaryColor,
  }) {
    _settings = _settings.copyWith(
      primaryColor: ThemeSettings._parseColor(primaryColor) ?? _settings.primaryColor,
      secondaryColor: ThemeSettings._parseColor(secondaryColor) ?? _settings.secondaryColor,
      tertiaryColor: ThemeSettings._parseColor(tertiaryColor) ?? _settings.tertiaryColor,
    );
    notifyListeners();
    _saveToStorage();
  }

  /// Cambiar modo de tema
  void setThemeMode(ThemeMode mode) {
    _settings = _settings.copyWith(mode: mode);
    notifyListeners();
    _saveToStorage();
  }

  /// Actualizar colores
  void updateColors({
    Color? primary,
    Color? secondary,
    Color? tertiary,
  }) {
    _settings = _settings.copyWith(
      primaryColor: primary,
      secondaryColor: secondary,
      tertiaryColor: tertiary,
    );
    notifyListeners();
    _saveToStorage();
  }

  /// Aplicar preset
  void applyPreset(ThemePreset preset) {
    _settings = _settings.copyWith(
      primaryColor: preset.primaryColor,
      secondaryColor: preset.secondaryColor,
      tertiaryColor: preset.tertiaryColor,
    );
    notifyListeners();
    _saveToStorage();
  }

  /// Guardar en storage local
  Future<void> _saveToStorage() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('theme_settings', jsonEncode(_settings.toJson()));
  }

  /// Construir ThemeData de Flutter
  ThemeData buildTheme({required Brightness brightness}) {
    final colorScheme = ColorScheme.fromSeed(
      seedColor: _settings.primaryColor,
      secondary: _settings.secondaryColor,
      tertiary: _settings.tertiaryColor,
      brightness: brightness,
    );

    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      fontFamily: _settings.fontFamily,
      
      // Bordes redondeados consistentes
      cardTheme: CardTheme(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(_settings.borderRadius),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(_settings.borderRadius),
        ),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(_settings.borderRadius),
          ),
        ),
      ),
      
      // Modo compacto
      visualDensity: _settings.compactMode 
          ? VisualDensity.compact 
          : VisualDensity.standard,
    );
  }

  ThemeData get lightTheme => buildTheme(brightness: Brightness.light);
  ThemeData get darkTheme => buildTheme(brightness: Brightness.dark);
}
```

---

## Paso 5: App Theme Base

```dart
// lib/core/theme/app_theme.dart

class AppTheme {
  // Singleton para acceso global
  static ThemeProvider? _provider;
  
  static void initialize(ThemeProvider provider) {
    _provider = provider;
  }

  static ThemeData get light => _provider?.lightTheme ?? _defaultLight;
  static ThemeData get dark => _provider?.darkTheme ?? _defaultDark;
  static ThemeMode get mode => _provider?.themeMode ?? ThemeMode.system;

  // Temas por defecto
  static final _defaultLight = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF1976D2),
      brightness: Brightness.light,
    ),
  );

  static final _defaultDark = ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: const Color(0xFF1976D2),
      brightness: Brightness.dark,
    ),
  );

  // Constantes de diseño
  static const double spacing = 8.0;
  static const double spacingSmall = 4.0;
  static const double spacingMedium = 16.0;
  static const double spacingLarge = 24.0;
  static const double spacingXLarge = 32.0;

  static const double radiusSmall = 4.0;
  static const double radiusMedium = 8.0;
  static const double radiusLarge = 16.0;
  static const double radiusXLarge = 24.0;

  // Sombras consistentes
  static List<BoxShadow> get shadowSmall => [
    BoxShadow(
      color: Colors.black.withValues(alpha: 0.05),
      blurRadius: 4,
      offset: const Offset(0, 2),
    ),
  ];

  static List<BoxShadow> get shadowMedium => [
    BoxShadow(
      color: Colors.black.withValues(alpha: 0.1),
      blurRadius: 8,
      offset: const Offset(0, 4),
    ),
  ];

  static List<BoxShadow> get shadowLarge => [
    BoxShadow(
      color: Colors.black.withValues(alpha: 0.15),
      blurRadius: 16,
      offset: const Offset(0, 8),
    ),
  ];
}
```

---

## Paso 6: Widget de Configuración

```dart
class ThemeSettingsTab extends StatelessWidget {
  const ThemeSettingsTab({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<ThemeProvider>(
      builder: (context, themeProvider, child) {
        return SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Sección: Modo de tema
              _SectionCard(
                title: 'Modo de Tema',
                child: _ThemeModeSelector(
                  currentMode: themeProvider.themeMode,
                  onChanged: themeProvider.setThemeMode,
                ),
              ),

              const SizedBox(height: 16),

              // Sección: Presets
              _SectionCard(
                title: 'Paletas de Colores',
                child: _PresetGrid(
                  presets: ThemePreset.defaultPresets,
                  currentPrimary: themeProvider.primaryColor,
                  onPresetSelected: themeProvider.applyPreset,
                ),
              ),

              const SizedBox(height: 16),

              // Sección: Colores personalizados
              _SectionCard(
                title: 'Personalizar Colores',
                child: Column(
                  children: [
                    _ColorPickerTile(
                      label: 'Color Primario',
                      color: themeProvider.primaryColor,
                      onColorChanged: (color) => themeProvider.updateColors(primary: color),
                    ),
                    const Divider(),
                    _ColorPickerTile(
                      label: 'Color Secundario',
                      color: themeProvider.secondaryColor,
                      onColorChanged: (color) => themeProvider.updateColors(secondary: color),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 16),

              // Preview
              _SectionCard(
                title: 'Vista Previa',
                child: _ThemePreview(),
              ),
            ],
          ),
        );
      },
    );
  }
}

class _ThemeModeSelector extends StatelessWidget {
  final ThemeMode currentMode;
  final ValueChanged<ThemeMode> onChanged;

  const _ThemeModeSelector({
    required this.currentMode,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return SegmentedButton<ThemeMode>(
      segments: const [
        ButtonSegment(
          value: ThemeMode.light,
          icon: Icon(Icons.light_mode),
          label: Text('Claro'),
        ),
        ButtonSegment(
          value: ThemeMode.system,
          icon: Icon(Icons.settings_suggest),
          label: Text('Sistema'),
        ),
        ButtonSegment(
          value: ThemeMode.dark,
          icon: Icon(Icons.dark_mode),
          label: Text('Oscuro'),
        ),
      ],
      selected: {currentMode},
      onSelectionChanged: (selection) => onChanged(selection.first),
    );
  }
}

class _PresetGrid extends StatelessWidget {
  final List<ThemePreset> presets;
  final Color currentPrimary;
  final ValueChanged<ThemePreset> onPresetSelected;

  const _PresetGrid({
    required this.presets,
    required this.currentPrimary,
    required this.onPresetSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Wrap(
      spacing: 12,
      runSpacing: 12,
      children: presets.map((preset) {
        final isSelected = preset.primaryColor == currentPrimary;
        return GestureDetector(
          onTap: () => onPresetSelected(preset),
          child: Container(
            width: 80,
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              border: Border.all(
                color: isSelected 
                    ? Theme.of(context).colorScheme.primary 
                    : Colors.grey.shade300,
                width: isSelected ? 2 : 1,
              ),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _ColorDot(color: preset.primaryColor),
                    _ColorDot(color: preset.secondaryColor),
                    _ColorDot(color: preset.tertiaryColor),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  preset.name,
                  style: const TextStyle(fontSize: 12),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
          ),
        );
      }).toList(),
    );
  }
}

class _ColorDot extends StatelessWidget {
  final Color color;

  const _ColorDot({required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 16,
      height: 16,
      margin: const EdgeInsets.symmetric(horizontal: 2),
      decoration: BoxDecoration(
        color: color,
        shape: BoxShape.circle,
        border: Border.all(color: Colors.white, width: 1),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.2),
            blurRadius: 2,
          ),
        ],
      ),
    );
  }
}
```

---

## Uso en MaterialApp

```dart
// main.dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<ThemeProvider>(
      builder: (context, themeProvider, child) {
        return MaterialApp(
          title: 'Mi App',
          theme: themeProvider.lightTheme,
          darkTheme: themeProvider.darkTheme,
          themeMode: themeProvider.themeMode,
          home: const HomePage(),
        );
      },
    );
  }
}
```

---

## Dependencias Recomendadas

```yaml
# pubspec.yaml
dependencies:
  shared_preferences: ^2.2.0
  flex_color_picker: ^3.3.0  # Para selector de color visual
  provider: ^6.0.0
```
