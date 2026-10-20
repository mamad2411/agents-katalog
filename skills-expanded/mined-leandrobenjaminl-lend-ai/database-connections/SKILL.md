---
name: database-connections
description: >
  Conexiones a bases de datos con SQLAlchemy — PostgreSQL, MySQL, SQLite.
  Lectura/escritura de tablas con Pandas y manejo de sesiones.
  Trigger: Cuando necesitás conectarte a una base de datos, ejecutar queries, o leer/escribir tablas con Pandas.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T2-fast
---

# Skill: database-connections

Conexiones a bases de datos. Conectate bien o no te conectes.

## Trigger

- Necesitás leer datos de PostgreSQL, MySQL, SQLite
- Querés escribir resultados de un análisis a una DB
- Tenés que configurar la conexión desde cero
- El string de conexión no funciona y hay que debuggearlo

## Workflow LEND

```
1. ANALIZAR
   ├── Motor: PostgreSQL, MySQL, SQLite, SQL Server
   ├── ¿Local o remoto? ¿hay VPN? ¿credenciales?
   ├── ¿Lectura, escritura, o ambas?
   └── Volumen: ¿cuántas filas? (para elegir chunking o no)

2. OFRECER (Menú del Senior)
   ├── A) SQLAlchemy + Pandas — read_sql + to_sql, la más versátil
   ├── B) SQLite directo — sqlite3 nativo, cero config, para datos locales
   └── C) DuckDB — SQL engine embebido, ideal para análisis sobre archivos

3. ELEGIR → confirmación

4. HACER
   ├── Crear engine: create_engine("postgresql://user:pass@host/db")
   ├── Probar conexión: engine.connect() con try/except
   ├── Leer: pd.read_sql("SELECT * FROM tabla", engine)
   ├── Escribir: df.to_sql("tabla", engine, if_exists="replace", index=False)
   ├── Siempre cerrar: engine.dispose() al terminar
   ├── Secrets: NUNCA hardcodear credenciales. Usar .env o variables de entorno
   └── SSL/TLS si es remoto — parámetros adicionales en el connection string

5. VERIFICAR
   ├── La conexión funciona (probar con una query simple)
   ├── Las credenciales no están en el código
   └── El tipo de datos se mapea correctamente entre Pandas y DB
```

## Patrones

- **SQLAlchemy siempre**: es el estándar. Maneja PostgreSQL, MySQL, SQLite con la misma API.
- **Connection pooling**: SQLAlchemy lo maneja automático, no creés conexiones nuevas cada vez.
- **Chunking**: `pd.read_sql(..., chunksize=10000)` para tablas grandes.
- **Secrets**: .env + python-dotenv. Nunca credenciales en el código.
- **SSL**: conexiones remotas requieren SSL. `sslmode=require` en PostgreSQL.

## Anti-patrones

- ❌ Hardcodear credenciales en el código — .env o variables de entorno siempre
- ❌ No cerrar conexiones — `engine.dispose()` o se acumulan
- ❌ Leer tablas enteras sin WHERE — si la tabla tiene 10M filas, morís
- ❌ to_sql con index=True — crea una columna `index` al pedo
- ❌ No verificar tipos — lo que Pandas lee puede no mapear bien al schema de la DB
