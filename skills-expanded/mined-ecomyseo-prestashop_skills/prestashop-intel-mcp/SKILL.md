---
name: prestashop-intel-mcp
description: Utiliza un servidor MCP local para indexar módulos de PrestaShop. Mantiene una caché JSON en "Json MCP modules" para evitar re-escaneos y optimizar el análisis de hooks y clases.
---

# PrestaShop Intel MCP (Model Context Protocol)

Este skill permite conectar con un servidor MCP que actúa como "bibliotecario" de módulos. Optimiza el análisis guardando la estructura en archivos JSON persistentes.

## 🚀 Cómo activar este MCP

### Configuración del Servidor Local
Asegúrate de que el servidor esté configurado en Antigravity:
```json
"mcpServers": {
  "prestashop-intel-local": {
    "command": "node",
    "args": ["<ruta>/mcp-prestashop-intel-local/dist/index.js"]
  }
}
```

---

## 🛠️ Protocolo de Escaneo Obligatorio (JSON Cache)

**PARA CADA INTERACCIÓN CON UN MÓDULO, LA IA DEBE SEGUIR ESTE FLUJO:**

1.  **Verificar Existencia del JSON**:
    *   Ruta: `<carpeta de trabajo>\Json MCP modules\[nombre_modulo].json`.
2.  **Si NO existe**:
    *   Ejecutar `mcp_prestashop-intel-local_scan_module_structure` indicando la ruta del módulo.
    *   Guardar el resultado JSON en la ruta mencionada arriba.
3.  **Si EXISTE**:
    *   Leer el JSON con `view_file` para obtener el mapa de hooks, clases y controladores.
    *   **Validar Enriquecimiento**: Si el JSON solo tiene la lista de hooks pero no el bloque `logic_analysis`, la IA debe generarlo analizando los métodos principales.
4.  **Sincronización y Mejora**:
    *   Si se añaden nuevos ficheros o hooks al código, el JSON **debe ser regenerado**.
    *   **Análisis Continuo**: Cada vez que se use `get_method_code` para resolver una tarea, los hallazgos clave deben añadirse al campo `logic_analysis` del JSON para que la IA en la siguiente sesión "sepa" cómo funciona sin releer el código.

---

## 🧠 Enriquecimiento Inteligente (IA Boost)

Para que el JSON sea 100% efectivo para la IA, debe incluir:
- **`logic_analysis`**: Descripción verbal de qué hace cada hook clave (Header, ValidateOrder, FooterProduct, etc.).
- **`technical_details`**: Lista de tablas de DB usadas, prefijos de configuración, APIs externas conectadas y modos de consentimiento.
- **`js_events_map`**: Si el módulo usa JS dinámico, mapear qué script lanza qué evento del DataLayer.

---

## 🔍 Herramientas Disponibles

- **`scan_module_structure`**: Genera el mapa completo del módulo.
- **`get_method_code`**: Obtiene el contenido de un hook sin abrir el archivo entero.
- **`find_config_keys`**: Extrae todas las opciones guardadas en la base de datos de PrestaShop.
- **`analyze_object_model`**: Extrae la definición de la base de datos (`static $definition`) de una clase ObjectModel.
- **`scan_translations`**: Busca todas las cadenas de traducción usando `l()` y **`trans()`** (Modern System) tanto en PHP como en TPL.
- **`map_assets`**: Identifica todos los archivos JS y CSS registrados.
- **`extract_smarty_vars`**: Mapea variables asignadas en PHP y su uso en plantillas TPL.

---

## 📂 Reglas de Oro
- **Cero Redundancia**: No pidas a la IA que "lea todo el módulo" si el JSON de estructura ya está disponible.
- **Uso de Modern Translations**: Siempre priorizar la identificación y generación de traducciones con el sistema `trans()` si el módulo indica `isUsingNewTranslationSystem() => true`.
- **Rutas Absolutas**: Usa siempre rutas completas para el acceso a ficheros y guardado de JSONs.
- **Actualización Proactiva**: Al terminar una tarea que modifique la estructura (añadir hooks/clases), el archivo JSON de caché **debe ser actualizado**.
- **Sanitización Obligatoria**: Al analizar ObjectModels, verificar siempre que los campos tengan validación y sanitización `pSQL`.
