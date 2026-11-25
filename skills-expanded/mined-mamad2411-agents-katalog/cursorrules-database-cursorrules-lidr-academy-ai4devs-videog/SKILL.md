# Reglas de Cursor para Luz Roja, Luz Verde

## Patrones Críticos de Implementación
- El juego sigue un enfoque modular con sistemas claramente separados
- Se utiliza el patrón Estado para manejar los diferentes estados del juego
- El sistema de eventos se basa en el patrón Observador para comunicación entre módulos
- Las acciones del jugador siguen el patrón Comando para separar la entrada de su efecto

## Preferencias de Usuario y Flujo de Trabajo
- Desarrollo guiado por pruebas (TDD) utilizando RSpec
- Enfoque iterativo, comenzando con funcionalidades centrales
- Código limpio y modular con comentarios explicativos
- Énfasis en la jugabilidad sobre los gráficos avanzados

## Patrones Específicos del Proyecto
- Un solo botón como mecánica principal de juego
- Sistema de semáforo con luz roja/verde indicado por música
- Minijuego de equilibrio cuando el jugador se detiene
- Animaciones dramáticas para las eliminaciones
- Bots con IA que siguen las mismas reglas que los jugadores

## Desafíos Conocidos
- Equilibrio de la dificultad del minijuego de equilibrio
- Detección precisa de movimiento durante la luz roja
- Comportamiento de los bots para que sea desafiante pero justo
- Sincronización entre música y mecánicas de juego

## Evolución de Decisiones del Proyecto
- El juego se desarrollará con Ruby y RSpec para testing
- Se ha optado por un estilo visual minimalista con colores planos
- El diseño arquitectónico será modular para facilitar el desarrollo y mantenimiento
- La mecánica central del juego se basará en un único botón

## Patrones de Uso de Herramientas
- Git para control de versiones
- RSpec para tests automatizados
- Desarrollo iterativo con ciclos de implementación-prueba

Este archivo se actualizará conforme el proyecto evolucione y se descubran nuevos patrones o preferencias importantes.

# Registro de Prompts.
Guarda todos los Prompts en orden cronologico en el archivo `prompts.md`
Ej:
numero de prompt: 1
prompt: "Quiero que la Horientacion sea hacia el lado que el personaje parta a la izquierda y se mueva a la derecha.sz
La barra espacio no esta moviendo el personaje"

numero de prompt: 2
