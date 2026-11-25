---
name: Code Review
description: Checklist de revisión de código para el debugger y el orquestador — corrección, casos borde, tests y seguridad básica, con hallazgos por severidad.
---

## Proceso

1. Lee el diff completo (`git diff` / cambios indicados) antes de opinar; entiende la intención del cambio.
2. Revisa el código circundante: un cambio correcto en un contexto roto sigue siendo un problema.
3. Aplica el checklist en orden y anota hallazgos con `archivo:línea`.
4. Cierra con veredicto explícito: `APROBADO` o `CAMBIOS REQUERIDOS` (con lista de los bloqueantes).

## Checklist

- **Corrección**: ¿la lógica hace lo que dice la spec/tarea? ¿maneja los casos borde (vacío, nulo, límites, concurrencia)?
- **Errores**: ¿se validan entradas? ¿los errores se propagan con contexto, sin tragar excepciones?
- **Tests**: ¿hay tests de la lógica nueva y de los casos borde? ¿el test de regresión existe si es un fix?
- **Seguridad rápida**: inyección, autorización en endpoints nuevos, secretos expuestos, rutas de ficheros sin sanear.
- **Consistencia**: sigue los patrones, nombres y estructura del código existente.
- **Alcance**: ¿el diff solo toca lo pedido? Marca como P2 cualquier refactor no solicitado que se coló.
- **Datos**: migraciones con rollback, compatibilidad hacia atrás, índices para consultas nuevas.

## Severidades

- **P0**: bug que rompe producción o agujero de seguridad crítico — bloqueante.
- **P1**: bug probable o fallo de seguridad real — bloqueante antes de mergear.
- **P2**: deuda importante, test faltante clave, refactor no solicitado — corregir ya.
- **P3**: mejora recomendada, naming, duplicación menor.
- **P4**: cosmético, opcional.

## Formato del informe

```
## Revisión: <tarea>
Hallazgos:
- [P1] archivo:línea — descripción + sugerencia concreta
...
Veredicto: APROBADO | CAMBIOS REQUERIDOS (bloqueantes: ...)
```
