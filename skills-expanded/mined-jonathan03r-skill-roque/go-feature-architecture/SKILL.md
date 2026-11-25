---
name: go-feature-architecture
description: Implementa proyectos y funcionalidades Go organizados por módulos, con baja complejidad, helpers reutilizables documentados y exports C directos para DLL de Excel.
---

# Arquitectura Go por funcionalidades

Aplica estas reglas al crear o modificar código Go, en especial DLL Go usadas desde Excel/VBA.

## Arquitectura

Usa un **monolito modular organizado por funcionalidades**. Cada funcionalidad mantiene su comportamiento en su paquete; no dividas el producto en servicios independientes sin una necesidad indicada.

Flujo habitual de DLL:

```text
Excel/VBA → DLL C (exports) → interfaz de aplicación → paquete de funcionalidad → integraciones externas/archivos
```

- La carpeta de exports es adaptador C: convierte argumentos, delega y devuelve la respuesta.
- La interfaz conecta cada export con la función de la funcionalidad correspondiente.
- La funcionalidad concentra sus reglas y coordina dependencias necesarias.
- Usa paquetes o interfaces adicionales solo cuando simplifiquen una dependencia real, una integración o su sustitución. No impongas capas vacías ni una Clean Architecture completa por defecto.

## Antes de cambiar código

1. Lee todos los `AGENTS.md` aplicables al repositorio.
2. Lee `docs/REUTILIZABLES.md` y busca en el código antes de crear helpers.
3. Inspecciona funcionalidades y contratos cercanos. Para DLL, identifica el repositorio de referencia indicado por el usuario y vuelve a revisar su estructura y formato en cada tarea.
4. Confirma el comportamiento solicitado. No agregues validaciones, ramas, opciones ni funciones de negocio que el usuario no haya pedido.

## Organización por funcionalidad

- Agrupa el código por capacidad del negocio, con nombres claros y responsabilidades relacionadas.
- Dentro de cada funcionalidad, separa archivos cuando separen responsabilidades reales: contrato/modelos, integración, almacenamiento, coordinación.
- Mantén carpetas pequeñas. Como guía, procura alrededor de 5–7 archivos Go por paquete; si crece, divide por responsabilidades. Evita un archivo por cada función trivial.
- Mantén baja la complejidad ciclomática: funciones cortas y directas, retornos tempranos y poca anidación. No extraigas funciones mecánicamente solo para bajar una métrica.
- No mezcles lógica de una funcionalidad en otra ni dupliques comportamiento equivalente.

## Funciones reutilizables

- Busca en `docs/REUTILIZABLES.md` y en el código antes de crear una función reutilizable.
- Si sirve a más de una funcionalidad, ubícala en un paquete común adecuado y registra en `docs/REUTILIZABLES.md`: firma Go exacta, paquete/ruta, propósito, contrato de entrada/salida, efectos y límites.
- La lógica exclusiva de una funcionalidad permanece dentro de ese módulo y no se registra como helper general.
- Actualiza el catálogo al cambiar o eliminar una función compartida. La siguiente IA debe leer ese catálogo antes de crear helpers.

## Exports para DLL de Excel

- Inspecciona el repositorio de referencia indicado por el usuario. Sigue su estilo vigente, más las reglas específicas de abajo.
- En la carpeta/paquete de exports solo pueden estar funciones exportables y cada una debe tener su directiva `//export Nombre`. Si una función no es exportable, ubícala fuera de esa carpeta: dejarla allí es un mapeo incorrecto. Helpers de C, parsing y memoria van en paquete auxiliar.
- Cada export debe ser simple y directo: adaptar entrada, delegar a la interfaz de aplicación, adaptar salida. Sin validaciones, condiciones alternativas, reintentos, IO, acceso a BD ni reglas de negocio en el cuerpo exportado.
- Una función exportada por operación, en archivo nombrado por funcionalidad u operación. Agrupa exports relacionados; evita subcarpetas o archivos innecesarios.
- Documenta el contrato en español con `//****//` como delimitadores. Explica propósito, entrada, salida y contrato de memoria que Excel necesita.
- Pon `//export NombreExacto` inmediatamente antes de la declaración Go.
- Conserva nombres, firma C, JSON, propiedad de memoria y contrato VBA existente salvo instrucción expresa del usuario.
- Mantén `main.go` mínimo, solo lo requerido para `-buildmode=c-shared`.

Formato de export:

```go
//go:build windows

package main

/*
#include <stdlib.h>
*/
import "C"

import "ruta/al/paquete/interfazdll"

//****//
// PrimaxOperacion describe en español qué hace la función.
// Entrada: JSON definido por el contrato.
// Salida: resultado acordado con Excel/VBA.
//****//
//export PrimaxOperacion
func PrimaxOperacion(input *C.char) *C.char {
	return C.CString(string(interfazdll.Operacion([]byte(C.GoString(input)))))
}
```

El ejemplo muestra el formato directo. No agregues funciones auxiliares sin `//export` al paquete/carpeta de exports; si hace falta un helper compartido, ubícalo fuera.

## Al completar

- Cambia solo lo necesario para cumplir la funcionalidad acordada.
- Actualiza catálogo reutilizable y contratos públicos afectados.
- Informa archivos cambiados y distingue revisión, compilación Go, generación/copia de DLL y validación real desde Excel.

## Formato para pedir una funcionalidad

```text
Funcionalidad: <qué debe hacer>
Entrada: <JSON, argumentos o datos>
Salida: <contrato esperado>
Reglas: <reglas confirmadas y casos límite>
Export DLL: <nombre exacto o “por definir”>
Excel/VBA: <invocación o “por definir”>
```

Se pueden omitir campos desconocidos. Inspecciona el repositorio e infiere decisiones técnicas rutinarias. Pregunta si falta una regla que cambie el comportamiento visible.
