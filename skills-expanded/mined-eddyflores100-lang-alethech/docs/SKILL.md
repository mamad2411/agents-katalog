# Alethech: instalar, guardar y continuar

La skill convierte el núcleo criptográfico en un flujo de memoria de trabajo.
No pide APIs, cuentas ni servidores. El primer guardado crea automáticamente un
archivo cifrado y una credencial local. La extensión/visor existente sigue siendo
la opción para chats web sin ejecución de scripts.

## Instalar la skill

```bash
npx skills add eddyflores100-lang/alethech --skill alethech --global
```

El instalador permite seleccionar agentes compatibles. También puedes copiar la
carpeta completa `.agents/skills/alethech` al directorio de skills que documente tu
agente. Copiar solo SKILL.md pierde los scripts necesarios. El agente necesita
Python 3.10+ y permiso para ejecutar archivos; ninguna skill puede otorgarle por sí
sola permisos o soporte que su plataforma no ofrezca.

La primera ejecución prepara un entorno Python privado si falta el paquete del
protocolo; descarga `alethech==0.9.5` una vez. Después los flujos operan sin red.
No instala modelos, no modifica Python global ni configura MCP. Si ya usas un
entorno compatible con Alethech, lo aprovecha. Para instalaciones sin red prepara
ese entorno previamente y usa `ALETHECH_NO_BOOTSTRAP=1`.

## Uso cotidiano en lenguaje natural

- «Alethech, guarda lo que decidimos y lo que falta de este proyecto».
- «Continúa el proyecto Faro desde mi memoria».
- «Lleva esta memoria a otro agente».
- «Guarda una copia cifrada en mi carpeta de OneDrive».

El agente selecciona el espacio de proyecto y guarda un resumen factual con meta,
cambios verificados, decisiones, restricciones, preguntas abiertas y próximos
pasos. Repetir el mismo último checkpoint no duplica el historial. Al retomar,
verifica el archivo completo y entrega solo las entradas que caben en su presupuesto
de contexto, con sus IDs firmados y número de entradas omitidas.

Esto automatiza el flujo cuando el agente ejecuta la skill; no instala un vigilante
universal de conversaciones. No lee memorias internas ni chats no cargados.

## Transporte a otro dispositivo o IA

Pide exportar la memoria. En una terminal local se elige una contraseña de al menos
12 caracteres mediante entrada oculta. El helper entrega un `.aleth` y guarda el
código de recuperación en otro archivo privado; informa las rutas sin imprimir
ningún secreto. Arrastra, copia a USB o comparte el `.aleth`. En el nuevo agente,
importa en un espacio vacío e introduce la contraseña localmente una vez.

No escribas la contraseña en el chat. En un entorno no interactivo el usuario
puede preparar un archivo de contraseña privado y facilitar solo su ruta
`--credential-file`. La skill no pide leer su contenido en la conversación.

Si el destino es un chat sin scripts, abre el `.aleth` con la extensión o el
[visor offline](CHAT_CAPTURE_FLOW.md), desbloquéalo y comparte el contexto elegido.
Un adjunto cifrado por sí solo no da al modelo la capacidad de descifrarlo.

## Nube opcional, sin APIs

Selecciona una carpeta local que tu aplicación de nube ya sincronice. El comando
`cloud` solicita una contraseña portátil una vez; en guardados posteriores copia
únicamente `<proyecto>.aleth`. Las claves locales quedan fuera. Alethech confirma
la copia local, no que el proveedor ya la haya subido.

Si cambia la revisión de la carpeta sincronizada, el helper conserva ambos trabajos:
guarda el nuevo trabajo local y reporta conflicto sin sobreescribir la otra revisión.
Importa la otra en un espacio distinto para inspeccionarla y reconciliar decisiones.
No existe un merge automático ni bloqueo distribuido entre equipos. Usa un escritor
por espacio sincronizado a la vez. Las copias de nube se abren con su contraseña;
un código de recuperación de un export distinto no sirve para esa copia.

## Seguridad y controles reales

- Memoria persistida cifrada; directorios temporales privados para abrir/verificar/firmar.
- Credenciales fuera de argumentos, contexto y copias de nube; permisos 0600/0700
  en POSIX. En Windows usa un directorio privado del usuario y sus ACL.
- Lock local, primer guardado publicado como una unidad completa, recuperación de escrituras
  interrumpidas tras verificar el historial y checkpoint local contra rollback.
- Aislamiento por proyecto y detección de patrones comunes de secretos.
- Contexto marcado como datos no confiables: una firma válida no autoriza órdenes.
- Búsqueda lexical TF-IDF forzada; ningún modelo opcional se descarga por recall.

No protege frente a software o agentes con los mismos permisos del usuario. Los
archivos temporales se eliminan normalmente, sin promesa de borrado seguro. El
checkpoint no detecta rollback si también se restaura su estado local antiguo. La
primera importación establece una nueva referencia; verifica un HEAD conocido por
separado cuando necesites continuidad respecto de otro equipo.

La implementación y pruebas viven en `.agents/skills/alethech` y
`tests/test_passport_skill.py` / `tests/test_passport_runner.py`.
Consulta [comparación de alternativas](COMPETITIVE_MEMORY_REVIEW.md) para el
posicionamiento y [flujo de captura](CHAT_CAPTURE_FLOW.md) para navegador.
