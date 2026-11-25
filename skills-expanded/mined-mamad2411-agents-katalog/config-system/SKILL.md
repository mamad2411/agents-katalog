---
name: config-system
description: Skill para implementar módulo de configuración general del sistema
---

# Skill: config-system

## Propósito

Este skill genera un módulo de **Configuración del Sistema** que permite:

- Configuraciones globales (email, notificaciones, integraciones)
- Settings por tenant
- Variables de entorno en runtime
- Panel de administración de configuración

---

## Casos de Uso

- Configuración de SMTP para emails
- Tokens de APIs externas
- Límites del sistema (tamaño de archivos, timeouts)
- Feature flags
- Configuración de almacenamiento
- Información de la aplicación (versión, build)

---

## Estructura de Archivos a Crear

```text
proyecto/
├── backend/
│   ├── internal/
│   │   ├── database/
│   │   │   └── queries/
│   │   │       └── settings.sql
│   │   ├── handlers/
│   │   │   └── settings.go
│   │   └── config/
│   │       └── config.go
│   └── migrations/
│       └── 000025_create_system_settings.up.sql
└── frontend/
    └── lib/
        └── features/
            └── configuration/
                ├── data/
                │   └── models/
                │       └── system_settings_model.dart
                ├── services/
                │   └── system_settings_service.dart
                └── presentation/
                    └── widgets/
                        └── system_settings_tab.dart
```

---

## Paso 1: Schema de Base de Datos

```sql
-- Tabla de configuraciones del sistema
CREATE TABLE public.system_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Para configuración por tenant (NULL = global)
    tenant_id UUID REFERENCES public.tenants(id) ON DELETE CASCADE,
    
    -- Clave única del setting
    key VARCHAR(100) NOT NULL,
    
    -- Valor (almacenado como JSON para flexibilidad)
    value JSONB NOT NULL DEFAULT '{}',
    
    -- Tipo de dato para validación frontend
    value_type VARCHAR(20) DEFAULT 'string', -- string, number, boolean, json, secret
    
    -- Categoría/grupo del setting
    category VARCHAR(50) NOT NULL,
    
    -- Metadatos
    label VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Si es editable desde UI
    is_editable BOOLEAN DEFAULT true,
    
    -- Si requiere reiniciar el servidor
    requires_restart BOOLEAN DEFAULT false,
    
    -- Orden en UI
    display_order INT DEFAULT 0,
    
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    -- Unique por tenant+key
    CONSTRAINT unique_tenant_setting UNIQUE (tenant_id, key)
);

CREATE INDEX idx_settings_tenant ON public.system_settings(tenant_id);
CREATE INDEX idx_settings_category ON public.system_settings(category);
CREATE INDEX idx_settings_key ON public.system_settings(key);

-- Datos iniciales - Configuraciones globales
INSERT INTO public.system_settings 
    (tenant_id, key, value, value_type, category, label, description, display_order) 
VALUES
    -- Email/SMTP
    (NULL, 'smtp_host', '"localhost"', 'string', 'email', 
     'Servidor SMTP', 'Host del servidor de correo', 10),
    (NULL, 'smtp_port', '587', 'number', 'email', 
     'Puerto SMTP', 'Puerto del servidor SMTP', 20),
    (NULL, 'smtp_user', '""', 'string', 'email', 
     'Usuario SMTP', 'Usuario para autenticación SMTP', 30),
    (NULL, 'smtp_password', '""', 'secret', 'email', 
     'Contraseña SMTP', 'Contraseña del servidor SMTP', 40),
    (NULL, 'smtp_from_email', '"noreply@app.com"', 'string', 'email', 
     'Email Remitente', 'Dirección de correo para envíos', 50),
    (NULL, 'smtp_from_name', '"Sistema"', 'string', 'email', 
     'Nombre Remitente', 'Nombre que aparece en los correos', 60),
    
    -- Almacenamiento
    (NULL, 'storage_provider', '"local"', 'string', 'storage', 
     'Proveedor de Storage', 'local, s3, gcs, azure', 10),
    (NULL, 'storage_max_file_size', '10485760', 'number', 'storage', 
     'Tamaño Máximo de Archivo', 'En bytes (default: 10MB)', 20),
    (NULL, 'storage_allowed_extensions', '["jpg","jpeg","png","pdf","doc","docx"]', 'json', 'storage', 
     'Extensiones Permitidas', 'Lista de extensiones de archivo', 30),
    
    -- Seguridad
    (NULL, 'password_min_length', '8', 'number', 'security', 
     'Longitud Mínima de Contraseña', 'Caracteres mínimos', 10),
    (NULL, 'session_timeout_minutes', '30', 'number', 'security', 
     'Timeout de Sesión', 'Minutos de inactividad', 20),
    (NULL, 'max_login_attempts', '5', 'number', 'security', 
     'Intentos de Login', 'Antes de bloquear', 30),
    (NULL, 'enable_2fa', 'false', 'boolean', 'security', 
     'Autenticación 2FA', 'Habilitar autenticación de dos factores', 40),
    
    -- General
    (NULL, 'app_name', '"Mi Aplicación"', 'string', 'general', 
     'Nombre de la Aplicación', 'Nombre que aparece en el sistema', 10),
    (NULL, 'app_version', '"1.0.0"', 'string', 'general', 
     'Versión', 'Versión actual de la aplicación', 20),
    (NULL, 'maintenance_mode', 'false', 'boolean', 'general', 
     'Modo Mantenimiento', 'Bloquea acceso a usuarios normales', 30),
    (NULL, 'default_timezone', '"America/Mexico_City"', 'string', 'general', 
     'Zona Horaria', 'Zona horaria por defecto', 40),
    (NULL, 'default_language', '"es"', 'string', 'general', 
     'Idioma', 'Idioma por defecto (es, en)', 50),

    -- Notificaciones
    (NULL, 'enable_email_notifications', 'true', 'boolean', 'notifications', 
     'Emails de Notificación', 'Enviar notificaciones por email', 10),
    (NULL, 'enable_push_notifications', 'false', 'boolean', 'notifications', 
     'Push Notifications', 'Enviar notificaciones push', 20)
ON CONFLICT (tenant_id, key) DO NOTHING;
```

---

## Paso 2: Queries SQL (sqlc)

```sql
-- name: GetSettingByKey :one
SELECT * FROM public.system_settings
WHERE key = $1 
    AND (tenant_id = $2 OR (tenant_id IS NULL AND $2::uuid IS NULL));

-- name: GetSettingValue :one
SELECT value FROM public.system_settings
WHERE key = $1 
    AND (tenant_id = $2 OR (tenant_id IS NULL AND $2::uuid IS NULL));

-- name: ListSettingsByCategory :many
SELECT * FROM public.system_settings
WHERE category = $1
    AND (tenant_id = $2 OR (tenant_id IS NULL AND $2::uuid IS NULL))
ORDER BY display_order, key;

-- name: ListAllSettings :many
SELECT * FROM public.system_settings
WHERE (tenant_id = $1 OR (tenant_id IS NULL AND $1::uuid IS NULL))
ORDER BY category, display_order, key;

-- name: ListGlobalSettings :many
SELECT * FROM public.system_settings
WHERE tenant_id IS NULL
ORDER BY category, display_order, key;

-- name: ListSettingCategories :many
SELECT DISTINCT category FROM public.system_settings
ORDER BY category;

-- name: UpdateSetting :one
UPDATE public.system_settings
SET value = $3,
    updated_at = CURRENT_TIMESTAMP
WHERE key = $1
    AND (tenant_id = $2 OR (tenant_id IS NULL AND $2::uuid IS NULL))
RETURNING *;

-- name: CreateSetting :one
INSERT INTO public.system_settings (
    tenant_id, key, value, value_type, 
    category, label, description, is_editable, display_order
)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
RETURNING *;

-- name: DeleteSetting :exec
DELETE FROM public.system_settings
WHERE key = $1
    AND tenant_id = $2
    AND is_editable = true;

-- name: GetSettingsGroupedByCategory :many
SELECT 
    category,
    json_agg(
        json_build_object(
            'key', key,
            'value', value,
            'value_type', value_type,
            'label', label,
            'description', description,
            'is_editable', is_editable,
            'requires_restart', requires_restart
        ) ORDER BY display_order
    ) as settings
FROM public.system_settings
WHERE (tenant_id = $1 OR tenant_id IS NULL)
GROUP BY category
ORDER BY category;
```

---

## Paso 3: Handler Go (Backend)

### Endpoints REST

| Método | Ruta                     | Descripción                 |
|--------|--------------------------|-----------------------------|
| GET    | /settings                | Obtener todos los settings  |
| GET    | /settings/:key           | Obtener setting específico  |
| PUT    | /settings/:key           | Actualizar setting          |
| GET    | /settings/categories     | Listar categorías           |
| GET    | /settings/category/:name | Settings de una categoría   |
| POST   | /settings                | Crear setting (admin)       |
| DELETE | /settings/:key           | Eliminar setting (admin)    |

### Handler

```go
type SystemSettingsHandler struct {
    db          *pgxpool.Pool
    queries     *database.Queries
    configCache sync.Map // Cache local
}

func NewSystemSettingsHandler(db *pgxpool.Pool, queries *database.Queries) *SystemSettingsHandler {
    return &SystemSettingsHandler{
        db:      db,
        queries: queries,
    }
}

// GetSetting obtiene un setting por clave
func (h *SystemSettingsHandler) GetSetting(c *gin.Context) {
    key := c.Param("key")
    tenantID := middleware.GetTenantIDOptional(c)
    
    // Intentar obtener del cache
    if cached, ok := h.configCache.Load(h.cacheKey(tenantID, key)); ok {
        c.JSON(200, cached)
        return
    }
    
    setting, err := h.queries.GetSettingByKey(c, database.GetSettingByKeyParams{
        Key:      key,
        TenantID: toPgUUIDNullable(tenantID),
    })
    if err != nil {
        c.JSON(404, gin.H{"error": "setting not found"})
        return
    }
    
    // Guardar en cache
    response := h.toResponse(setting)
    h.configCache.Store(h.cacheKey(tenantID, key), response)
    
    c.JSON(200, response)
}

// UpdateSetting actualiza un setting
func (h *SystemSettingsHandler) UpdateSetting(c *gin.Context) {
    key := c.Param("key")
    tenantID := middleware.GetTenantID(c)
    
    var req UpdateSettingRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
    
    // Verificar que existe y es editable
    existing, err := h.queries.GetSettingByKey(c, database.GetSettingByKeyParams{
        Key:      key,
        TenantID: toPgUUIDNullable(tenantID),
    })
    if err != nil {
        c.JSON(404, gin.H{"error": "setting not found"})
        return
    }
    
    if !existing.IsEditable {
        c.JSON(403, gin.H{"error": "setting is not editable"})
        return
    }
    
    // Validar tipo de valor
    valueJSON, err := json.Marshal(req.Value)
    if err != nil {
        c.JSON(400, gin.H{"error": "invalid value format"})
        return
    }
    
    setting, err := h.queries.UpdateSetting(c, database.UpdateSettingParams{
        Key:      key,
        TenantID: toPgUUIDNullable(tenantID),
        Value:    valueJSON,
    })
    if err != nil {
        c.JSON(500, gin.H{"error": "failed to update setting"})
        return
    }
    
    // Invalidar cache
    h.configCache.Delete(h.cacheKey(tenantID, key))
    
    response := h.toResponse(setting)
    c.JSON(200, response)
}

// GetAllSettings obtiene todos los settings agrupados por categoría
func (h *SystemSettingsHandler) GetAllSettings(c *gin.Context) {
    tenantID := middleware.GetTenantIDOptional(c)
    
    grouped, err := h.queries.GetSettingsGroupedByCategory(c, toPgUUIDNullable(tenantID))
    if err != nil {
        c.JSON(500, gin.H{"error": "failed to get settings"})
        return
    }
    
    c.JSON(200, grouped)
}

// Helper para obtener valor de config
func (h *SystemSettingsHandler) GetConfigValue(ctx context.Context, key string, tenantID *string) (interface{}, error) {
    setting, err := h.queries.GetSettingValue(ctx, database.GetSettingValueParams{
        Key:      key,
        TenantID: toPgUUIDNullable(tenantID),
    })
    if err != nil {
        return nil, err
    }
    
    var value interface{}
    json.Unmarshal(setting, &value)
    return value, nil
}

func (h *SystemSettingsHandler) cacheKey(tenantID, key string) string {
    return fmt.Sprintf("%s:%s", tenantID, key)
}
```

---

## Paso 4: DTOs (Go)

```go
type SettingResponse struct {
    Key             string      `json:"key"`
    Value           interface{} `json:"value"`
    ValueType       string      `json:"value_type"`
    Category        string      `json:"category"`
    Label           string      `json:"label"`
    Description     *string     `json:"description,omitempty"`
    IsEditable      bool        `json:"is_editable"`
    RequiresRestart bool        `json:"requires_restart"`
}

type UpdateSettingRequest struct {
    Value interface{} `json:"value" binding:"required"`
}

type CreateSettingRequest struct {
    Key         string      `json:"key" binding:"required"`
    Value       interface{} `json:"value" binding:"required"`
    ValueType   string      `json:"value_type,omitempty"`
    Category    string      `json:"category" binding:"required"`
    Label       string      `json:"label" binding:"required"`
    Description string      `json:"description,omitempty"`
    IsEditable  bool        `json:"is_editable,omitempty"`
}

type SettingCategory struct {
    Name     string            `json:"name"`
    Settings []SettingResponse `json:"settings"`
}
```

---

## Paso 5: Modelo Flutter

```dart
class SystemSetting {
  final String key;
  final dynamic value;
  final String valueType; // string, number, boolean, json, secret
  final String category;
  final String label;
  final String? description;
  final bool isEditable;
  final bool requiresRestart;

  SystemSetting({
    required this.key,
    required this.value,
    required this.valueType,
    required this.category,
    required this.label,
    this.description,
    this.isEditable = true,
    this.requiresRestart = false,
  });

  /// Valor como String
  String get stringValue => value?.toString() ?? '';

  /// Valor como bool
  bool get boolValue {
    if (value is bool) return value;
    if (value is String) return value.toLowerCase() == 'true';
    return false;
  }

  /// Valor como int
  int get intValue {
    if (value is int) return value;
    if (value is num) return value.toInt();
    if (value is String) return int.tryParse(value) ?? 0;
    return 0;
  }

  /// Es un campo secreto (password, api key)
  bool get isSecret => valueType == 'secret';

  factory SystemSetting.fromJson(Map<String, dynamic> json) => SystemSetting(
    key: json['key'],
    value: json['value'],
    valueType: json['value_type'] ?? 'string',
    category: json['category'],
    label: json['label'],
    description: json['description'],
    isEditable: json['is_editable'] ?? true,
    requiresRestart: json['requires_restart'] ?? false,
  );
}

class SettingCategory {
  final String name;
  final String displayName;
  final IconData icon;
  final List<SystemSetting> settings;

  SettingCategory({
    required this.name,
    required this.displayName,
    required this.icon,
    required this.settings,
  });

  static IconData getIconForCategory(String category) {
    switch (category) {
      case 'email': return Icons.email;
      case 'storage': return Icons.storage;
      case 'security': return Icons.security;
      case 'general': return Icons.settings;
      case 'notifications': return Icons.notifications;
      case 'integration': return Icons.extension;
      default: return Icons.tune;
    }
  }

  static String getDisplayName(String category) {
    switch (category) {
      case 'email': return 'Email / SMTP';
      case 'storage': return 'Almacenamiento';
      case 'security': return 'Seguridad';
      case 'general': return 'General';
      case 'notifications': return 'Notificaciones';
      case 'integration': return 'Integraciones';
      default: return category;
    }
  }
}
```

---

## Paso 6: Widget de Configuración

```dart
class SystemSettingsTab extends StatefulWidget {
  const SystemSettingsTab({super.key});

  @override
  State<SystemSettingsTab> createState() => _SystemSettingsTabState();
}

class _SystemSettingsTabState extends State<SystemSettingsTab> {
  final SettingsService _settingsService = getIt<SettingsService>();
  
  List<SettingCategory> _categories = [];
  bool _isLoading = true;
  String? _error;
  String _selectedCategory = 'general';

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    setState(() => _isLoading = true);

    try {
      final categories = await _settingsService.getSettingsGrouped();
      setState(() {
        _categories = categories;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_error != null) {
      return Center(child: Text('Error: $_error'));
    }

    return Row(
      children: [
        // Sidebar de categorías
        SizedBox(
          width: 250,
          child: Card(
            child: ListView(
              children: _categories.map((cat) {
                final isSelected = cat.name == _selectedCategory;
                return ListTile(
                  leading: Icon(cat.icon),
                  title: Text(cat.displayName),
                  selected: isSelected,
                  onTap: () => setState(() => _selectedCategory = cat.name),
                );
              }).toList(),
            ),
          ),
        ),

        const SizedBox(width: 16),

        // Panel de settings
        Expanded(
          child: Card(
            child: _buildSettingsPanel(),
          ),
        ),
      ],
    );
  }

  Widget _buildSettingsPanel() {
    final category = _categories.firstWhere(
      (c) => c.name == _selectedCategory,
      orElse: () => _categories.first,
    );

    return ListView.separated(
      padding: const EdgeInsets.all(16),
      itemCount: category.settings.length,
      separatorBuilder: (_, __) => const Divider(),
      itemBuilder: (context, index) {
        final setting = category.settings[index];
        return _SettingTile(
          setting: setting,
          onChanged: (value) => _updateSetting(setting.key, value),
        );
      },
    );
  }

  Future<void> _updateSetting(String key, dynamic value) async {
    try {
      await _settingsService.updateSetting(key, value);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Configuración guardada')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e'), backgroundColor: Colors.red),
      );
    }
  }
}

class _SettingTile extends StatelessWidget {
  final SystemSetting setting;
  final ValueChanged<dynamic> onChanged;

  const _SettingTile({
    required this.setting,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Label y descripción
          Expanded(
            flex: 2,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(
                      setting.label,
                      style: const TextStyle(fontWeight: FontWeight.w600),
                    ),
                    if (setting.requiresRestart)
                      const Padding(
                        padding: EdgeInsets.only(left: 8),
                        child: Chip(
                          label: Text('Requiere reinicio'),
                          backgroundColor: Colors.orange,
                          labelStyle: TextStyle(fontSize: 10),
                          padding: EdgeInsets.zero,
                        ),
                      ),
                  ],
                ),
                if (setting.description != null)
                  Text(
                    setting.description!,
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.grey.shade600,
                    ),
                  ),
              ],
            ),
          ),

          const SizedBox(width: 16),

          // Control de edición
          Expanded(
            flex: 1,
            child: _buildControl(),
          ),
        ],
      ),
    );
  }

  Widget _buildControl() {
    if (!setting.isEditable) {
      return Text(
        setting.stringValue,
        style: const TextStyle(color: Colors.grey),
      );
    }

    switch (setting.valueType) {
      case 'boolean':
        return Switch(
          value: setting.boolValue,
          onChanged: onChanged,
        );

      case 'number':
        return TextFormField(
          initialValue: setting.stringValue,
          keyboardType: TextInputType.number,
          decoration: const InputDecoration(
            isDense: true,
            border: OutlineInputBorder(),
          ),
          onFieldSubmitted: (value) => onChanged(int.tryParse(value) ?? 0),
        );

      case 'secret':
        return TextFormField(
          initialValue: setting.stringValue,
          obscureText: true,
          decoration: const InputDecoration(
            isDense: true,
            border: OutlineInputBorder(),
            suffixIcon: Icon(Icons.visibility_off),
          ),
          onFieldSubmitted: onChanged,
        );

      default:
        return TextFormField(
          initialValue: setting.stringValue,
          decoration: const InputDecoration(
            isDense: true,
            border: OutlineInputBorder(),
          ),
          onFieldSubmitted: onChanged,
        );
    }
  }
}
```

---

## Helper para Acceso Rápido a Configuración

```go
// config/config.go
package config

import (
    "context"
    "sync"
    "yourproject/internal/database"
)

var (
    queries *database.Queries
    cache   sync.Map
)

// Initialize configura el acceso a settings
func Initialize(q *database.Queries) {
    queries = q
}

// Get obtiene un setting por clave
func Get(ctx context.Context, key string) (interface{}, error) {
    if cached, ok := cache.Load(key); ok {
        return cached, nil
    }
    
    value, err := queries.GetSettingValue(ctx, database.GetSettingValueParams{
        Key: key,
    })
    if err != nil {
        return nil, err
    }
    
    var result interface{}
    json.Unmarshal(value, &result)
    cache.Store(key, result)
    
    return result, nil
}

// GetString obtiene un setting como string
func GetString(ctx context.Context, key, defaultValue string) string {
    val, err := Get(ctx, key)
    if err != nil || val == nil {
        return defaultValue
    }
    if s, ok := val.(string); ok {
        return s
    }
    return defaultValue
}

// GetInt obtiene un setting como int
func GetInt(ctx context.Context, key string, defaultValue int) int {
    val, err := Get(ctx, key)
    if err != nil || val == nil {
        return defaultValue
    }
    if f, ok := val.(float64); ok {
        return int(f)
    }
    return defaultValue
}

// GetBool obtiene un setting como bool
func GetBool(ctx context.Context, key string, defaultValue bool) bool {
    val, err := Get(ctx, key)
    if err != nil || val == nil {
        return defaultValue
    }
    if b, ok := val.(bool); ok {
        return b
    }
    return defaultValue
}

// InvalidateCache limpia el cache
func InvalidateCache() {
    cache = sync.Map{}
}
```

---

## Ejemplo de Uso del Helper

```go
// En cualquier parte del código
maxFileSize := config.GetInt(ctx, "storage_max_file_size", 10485760)
smtpHost := config.GetString(ctx, "smtp_host", "localhost")
maintenanceMode := config.GetBool(ctx, "maintenance_mode", false)

if maintenanceMode {
    c.JSON(503, gin.H{"error": "System under maintenance"})
    return
}
```
