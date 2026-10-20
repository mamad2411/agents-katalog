
# Protocolo de Herramientas MCP
- Utiliza sequential-thinking obligatoriamente antes de proponer refactorizaciones complejas, cambios en el bucle principal o matemáticas de colisiones.
- Consulta context7 para validar cualquier API de librerías externas antes de escribir código nuevo.
- Registra hitos arquitectónicos y contratos de interfaz en memory-graph para mantener coherencia entre sesiones.
- Emplea SQLite (/data/nexus_engine.db) cuando se requiera persistir metadatos, escenas o configuraciones del motor.
