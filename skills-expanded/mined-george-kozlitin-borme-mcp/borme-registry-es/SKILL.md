---
name: borme-registry-es
description: Responde preguntas sobre sociedades y empresas españolas a partir del Boletín Oficial del Registro Mercantil (BORME) mediante el servidor MCP de BORME en mcp.bormeapi.com. Úsela cuando el usuario quiera consultar o comprobar una empresa española o pregunte por su historia, constitución, nombramientos y ceses (administrador, apoderado, consejero), concurso de acreedores (quiebra), disolución, liquidación o extinción, cambios de domicilio social o de denominación, ampliaciones o reducciones de capital, fusiones, si sigue activa, un NIF o CIF, quién es titular de una marca o un nombre comercial, o qué se publicó en el BORME un día concreto o en una provincia. También en inglés (Spanish company registry, director appointments, insolvency, tax ID, trademark owner).
---

# BORME - el Boletín Oficial del Registro Mercantil

El servidor MCP `borme` contiene los anuncios de sociedades de la sección A del
BORME desde 2009, convertidos en eventos tipados, y ofrece además consultas por
NIF y por marca. Esta skill indica qué herramienta llamar, cómo encadenarlas y
cómo presentar lo que devuelven. La descripción y el esquema de parámetros de
cada herramienta explican sus parámetros; léalos también.

## Conexión

El endpoint alojado es `https://mcp.bormeapi.com/mcp` (transporte Streamable
HTTP). Funciona sin clave con el plan gratuito. Con clave, envíela en la
cabecera `X-API-Key`:

- Claude Code:
  `claude mcp add --transport http --scope user --header "X-API-Key: SU_CLAVE" borme https://mcp.bormeapi.com/mcp`
- Clientes que se configuran con JSON (el `mcp.json` de Cursor y similares):
  `{"mcpServers": {"borme": {"url": "https://mcp.bormeapi.com/mcp", "headers": {"X-API-Key": "SU_CLAVE"}}}}`
- Asistentes con conectores personalizados que inician sesión mediante OAuth
  (Claude.ai, ChatGPT, Copilot): `https://mcp.bormeapi.com/mcp/oauth`. El
  usuario inicia sesión con su cuenta de BORME API y se aplica el plan de esa
  cuenta; no hay que pegar ninguna clave.

Claves: https://bormeapi.com/es/account. Planes y precios:
https://bormeapi.com/es#precios. Configuración de cada cliente:
https://bormeapi.com/es/mcp.

Si las herramientas de `borme` no están disponibles en esta sesión, diga que el
servidor MCP de BORME no está conectado, facilite al usuario las líneas
anteriores y no responda de memoria.

## Qué incluye cada plan

- **Sin clave (free):** `search_events`, `company_history` y `daily_digest`
  sobre los últimos 7 días; `search_companies` (primeros 5 resultados);
  `list_act_types` y `registry_stats`. 50 llamadas al día por dirección IP.
- **basic:** los últimos 365 días, más `company_by_nif`, `brand_owner` y
  `company_brands`.
- **pro:** todo lo de basic, con todo el histórico desde 2009.
- **risk:** todo lo de pro, más `recent_signals`.

Si la respuesta trae `plan_window`, se aplicó la ventana del plan
(`company_history` lo incluye en todas las respuestas de los planes free y
basic). Dígaselo al usuario una vez, en una frase, e indíquele qué cubre el
resto: una clave para los últimos 365 días (basic) y pro para todo el
histórico. No repita la llamada con fechas anteriores -el servidor las recorta
igual- ni tome un resultado vacío como prueba de que antes no pasó nada.

Un rechazo que nombra un plan, o que indica que los anuncios de la sociedad
quedan fuera de la ventana, no es un fallo del servidor: transmita su mensaje,
indique qué plan lo cubre y no reintente.

## Qué herramienta usar

- **«¿Cuántos datos hay? ¿Están al día?»** → `registry_stats`. Llámela antes
  de fiarse de un filtro de fechas para un periodo poco habitual.
- **Un nombre de sociedad** → primero `search_companies` y, después,
  `company_history` con el slug de la sociedad a la que se refiere el usuario.
  Una coincidencia `fuzzy` es una pista, no una identificación; dígalo.
- **La historia de una sociedad** → `company_history`. Pase el slug; si solo
  tiene el nombre, use antes `search_companies`. Si `company_history` recibe un
  nombre y devuelve una lista de slugs candidatos, muéstrela y deje que el
  usuario elija; no escoja usted.
- **Eventos de muchas sociedades** (por fecha, provincia, tipo de acto o parte
  del nombre) → `search_events`.
- **«¿Qué se publicó en el BORME el día X?»** → `daily_digest`.
- **Un NIF o CIF** → `company_by_nif` y, después, `company_history` con el slug
  devuelto.
- **Una marca o un nombre comercial** distinto de la denominación social →
  `brand_owner` y, después, `company_history` con el slug.
- **Con qué nombres comerciales opera una sociedad o bajo qué marcas vende** →
  `company_brands` con el slug.
- **Las últimas señales de riesgo** (declaraciones de concurso, sociedades
  fénix, ceses masivos de cargos, sociedades incluidas en el listado de
  deudores de la AEAT) → `recent_signals`. Devuelve una muestra, como máximo
  10 filas de los últimos 7 días de publicación: no la presente nunca como una
  lista completa.

## Filtros que funcionan a la primera

- **Los tipos de acto son enumerados.** Llame una vez a `list_act_types` y use
  sus valores `act_type` (`INCORPORATION`, `APPOINTMENTS`, `TERMINATIONS`,
  `INSOLVENCY_DECLARATION`…). No invente enumerados a partir del texto en
  español.
- **Concursos:** filtre por `INSOLVENCY_DECLARATION` e `INSOLVENCY_STATUS`. Un
  anuncio de `INSOLVENCY_STATUS` (*Situación concursal*) puede recoger
  cualquier fase del procedimiento, entre ellas la solicitud de declaración,
  la declaración de concurso, el nombramiento de la administración concursal,
  la apertura de la fase de liquidación y la conclusión del concurso: lea
  `payload` antes de decir que una sociedad fue declarada en concurso; si no,
  llámelo anuncio concursal. Las antiguas suspensiones de pagos y quiebras
  que el Registro aún recoge son `SUSPENSION_OF_PAYMENTS` y
  `BANKRUPTCY_LEGACY`.
- **Las provincias** se escriben como las imprime el BORME, sin importar
  tildes ni mayúsculas: `MADRID`, `CADIZ`. En los nombres dobles vale
  cualquiera de las dos formas (`VALENCIA` o `VALÈNCIA`), y también las
  variantes castellanas y los exónimos ingleses habituales (`VIZCAYA`,
  `GERONA`, `SEVILLE`).
- **Las fechas** van en formato `YYYY-MM-DD` y son el día de publicación en el
  BORME, no el día en que la sociedad tomó el acuerdo. La fecha de inscripción
  registral está en `registral.reg_date`.
- **La búsqueda por nombre** necesita al menos tres letras o cifras. Una
  palabra muy común coincide con miles de sociedades; entonces
  `company_name_match` avisa de que la respuesta es parcial. Acote la búsqueda
  con una provincia o un rango de fechas.
- **En `search_events`, `count` es el número de eventos de esta respuesta, no
  un total.** La herramienta devuelve los `limit` eventos más recientes (50
  por defecto, 200 como máximo) y no tiene `offset`. Si `count` es igual a
  `limit`, hay más: para contar un periodo, divida el rango de fechas (día a
  día si hace falta) hasta que cada llamada devuelva menos de `limit`, y sume.
  Los totales nacionales por tipo de acto de un día están en `daily_digest`.
- `company_history` pagina con `offset` y devuelve `next_offset`.

## Presentarlo con fidelidad

- **Los datos registrales se citan tal como se publicaron.** Denominaciones
  sociales, nombres de personas, domicilios y `act_type_raw` / `role_raw` van
  tal como los imprimió el BORME. Traduzca al idioma del usuario lo que los
  rodea: tipos de acto, cargos y apoderamientos (`PROXY_HOLDER` es un
  *apoderado*), estados y encabezados. Si el usuario escribe en español, tome
  la etiqueta de cada tipo de acto del campo `spanish` de `list_act_types` y
  desarrolle las abreviaturas de cargo como las usa el Registro
  (`Adm. Solid.` → administrador solidario), en lugar de retraducir los
  enumerados ingleses.
- **El BORME publica cambios, no la situación actual.** Antes de decir quién
  ocupa hoy un cargo, compruebe en los eventos posteriores si hay un cese o un
  nuevo nombramiento para ese cargo, y diga «según los anuncios del BORME
  hasta <fecha del último evento>». Con una ventana de plan, advierta que el
  nombramiento puede ser anterior a ella.
- **Que un NIF no aparezca significa «aún no vinculado»**, no «esta sociedad
  no existe»: el BORME no tiene un campo de NIF y la correspondencia solo
  cubre parte de las sociedades. La excepción es el motivo
  `nif_check_character_failed`: ese identificador no supera el cálculo del
  carácter de control oficial y nunca se asignó. Dígalo y transmita el
  identificador con el carácter de control válido
  (`corrected_check_character`, que supone que el error está en el último
  carácter) y las sociedades de `did_you_mean`, si las hay; no presente
  ninguno como el NIF de la sociedad.
- **`nif_caveat`** significa que la letra inicial del NIF (la del tipo de
  entidad) no concuerda con la forma jurídica que figura en la denominación.
  Muestre el aviso; no presente la correspondencia como definitiva.
- **`ambiguous: true`** significa que hay varias sociedades candidatas.
  Enumérelas y pregunte al usuario a cuál se refiere.
- **Una marca no es un nombre.** En `brand_owner` y `company_brands`, un
  `commercial_name` es otro nombre de la empresa; una `trademark` es algo que
  vende. No diga nunca que una sociedad «se llama» como una de sus marcas. Las
  marcas se vinculan a las sociedades por el nombre del titular (la OEPM no
  publica NIF): presente una coincidencia como un indicio sólido, no como un
  dato registral confirmado.
- **Las señales de riesgo son alertas, no conclusiones.** Diga que una
  sociedad «ha sido marcada como posible sociedad fénix» o que «figuraba en el
  listado de deudores de la AEAT de <año>», nunca que «es» una sociedad fénix
  o que «debe» impuestos; cite los actos en que se basa la alerta y sus
  fechas.
- **Las cifras de `registry_stats` proceden de la última instantánea horaria;
  si no hay ninguna disponible, se utilizan estimaciones del planificador de
  PostgreSQL.** La respuesta no indica cuál de estas fuentes se ha utilizado ni
  incluye la fecha y hora de la instantánea. Explique estas limitaciones al
  presentar las cifras; no las describa como recuentos en tiempo real ni les
  atribuya una fecha y hora concretas.
- Indique la fecha de publicación en el BORME y el `borme_id` de cada evento
  que cite, para que el usuario pueda localizar el anuncio.

## Lo que este servidor no tiene

- Cuentas anuales y balances: el BORME publica actos registrales, no
  cuentas.
- Los anuncios de la sección C del BORME (anuncios y avisos legales, como
  convocatorias de junta o anuncios de fusión).
- Empresarios individuales (*autónomos*) y sociedades que nunca aparecieron
  en la sección A.
- Anuncios publicados antes de 2009.

Dígalo en lugar de suponer, y no rellene el hueco con lo que recuerde.
