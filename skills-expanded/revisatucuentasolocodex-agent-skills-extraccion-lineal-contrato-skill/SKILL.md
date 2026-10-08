---
name: extrusion-lineal-contrato-salud
description: Transformar un contrato de salud en una secuencia verificable de líneas, preservando orden, estructura y texto exacto sin interpretación.
---

# Extracción Lineal de Contratos de Salud (v1.0)

## Objetivo
Transformar un contrato de salud en una secuencia verificable de líneas, preservando:
- Orden original
- Estructura de tablas
- Cabeceras activas
- Texto exacto observado

⚠️ **Esta skill NO interpreta, NO limpia y NO canoniza.**

## 🛑 REGLAS ABSOLUTAS (NO NEGOCIABLES)

### 1. Principio de Fidelidad Literal
- El texto debe copiarse tal como aparece, sin resumir ni corregir.
- No reemplazar símbolos, no “limpiar” porcentajes, no inferir unidades.

### 2. Prohibido Pensar Semánticamente
- ❌ NO decidir si algo es cobertura.
- ❌ NO decidir si algo es tope.
- ❌ NO clasificar ámbito.
- ❌ NO eliminar “ruido”.
*Todo eso ocurre después, en otra skill.*

## Modelo de Salida (ÚNICO)

```json
{
  "metadata": {
    "origen": "contrato_pdf",
    "fuente": "string | desconocido",
    "paginas_total": number
  },
  "lineas": [
    {
      "pagina": number,
      "indice_linea": number,
      "tipo": "titulo" | "cabecera_tabla" | "fila_tabla" | "texto_libre",
      "cabecera_activa": [
        "string"
      ],
      "celdas": [
        {
          "indice_columna": number,
          "texto": string
        }
      ],
      "texto_plano": string
    }
  ]
}
```

## Instrucciones de Procesamiento

1. **Leer página por página**, de arriba hacia abajo.
2. **Si detectas una tabla**:
   - Registrar primero la fila de cabeceras como `cabecera_tabla`.
   - Mantener esa cabecera como `cabecera_activa` hasta que la tabla termine.
   - Cada fila de tabla:
     - Se registra como una sola línea.
     - Cada celda va en `celdas[]`.
3. **Texto fuera de tablas**:
   - Usar `texto_plano`.

**NO OMITIR NADA**
- Aunque parezca irrelevante.
- Aunque sea solo “%”.
- Aunque sea “Nota (*)”.

## Validación Mental Obligatoria

Antes de responder, verifica:
1. ¿El número de líneas es razonable para la extensión del PDF?
2. ¿Puedo reconstruir visualmente la tabla original solo con este JSON?
3. ¿Un auditor humano podría decir “sí, esto es lo que vi en el contrato”?

**Si la respuesta es no, el output es inválido.**

## Output
Retornar **SOLO** el objeto JSON válido.
- Sin explicaciones.
- Sin markdown.
- Sin comentarios.
