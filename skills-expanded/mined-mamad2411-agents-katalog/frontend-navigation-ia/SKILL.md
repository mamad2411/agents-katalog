---
name: frontend-navigation-ia
description: Navegación y arquitectura de información de la web — jerarquía de rutas, nav lateral/superior, breadcrumbs, estado activo, deep linking y URL como estado, menús que cambian por rol, y la regla de que ocultar una opción en el menú no autoriza nada. Usar al diseñar la estructura de navegación de un producto o sección, al agregar una ruta o un ítem de menú, al armar el nav de un rol nuevo (doctor, paciente, admin), o al revisar por qué los usuarios "no encuentran" una función.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Navegación y arquitectura de información

La IA (arquitectura de información) es cómo se organiza y se encuentra todo. Si el usuario no
encuentra una función, para él no existe. La navegación es el mapa de ese modelo.

## 1. Jerarquía de rutas

- Estructurá las rutas según el modelo mental del usuario, no según cómo está partido el backend.
- Rutas lazy por sección, con guardas de acceso.
- Profundidad moderada: si el usuario necesita 5 clics para una tarea frecuente, la IA está mal.
- Agrupá por tarea/rol, no por tipo técnico de pantalla.

## 2. Patrón de navegación

- **Nav lateral** para apps con muchas secciones (herramienta densa); **nav superior** para
  productos con pocas secciones o públicos.
- Marcá el **ítem activo** de forma inequívoca (no solo un color tenue): el usuario debe saber
  siempre dónde está.
- En móvil, colapsá a un patrón adecuado (drawer / bottom nav) sin esconder lo crítico.
- Secciones agrupadas y colapsables si son muchas; recordá el estado del grupo.

## 3. Breadcrumbs y orientación

- Breadcrumbs en jerarquías profundas (Directorio › Cardiología › Dr. X): muestran dónde está
  y permiten subir de nivel.
- Título de página coherente con el ítem de nav y con el `<title>` del documento.
- Un "volver" que respeta el historial, no uno que te manda siempre al inicio.

## 4. URL como estado y deep linking

- La URL refleja el estado navegable: filtros, tab activa, página/cursor, id del recurso. Así
  el usuario puede compartir el enlace, recargar y usar atrás/adelante del navegador.
- Estado efímero de UI (un dropdown abierto) no va en la URL; estado navegable, sí.
- Deep links a recursos concretos deben funcionar al pegarlos en frío (con el guard resolviendo auth).

## 5. Menús por rol — pero la autorización es del backend

- Distintos roles ven distintos menús (doctor, paciente, admin): mostrá solo lo que aplica a su rol.
- **Ocultar un ítem del menú NO es autorización.** El usuario puede escribir la URL a mano.
  Toda ruta protegida necesita su guard, y el endpoint detrás valida permiso y ownership
  (ver `authz-access-control`). Nunca "está seguro porque no hay botón".
- El guard y el menú deben derivar de la misma fuente de roles/permisos para no divergir.

```typescript
// ✅ el guard protege la ruta; el menú solo la muestra u oculta — el backend igual valida
export const canManageBilling: CanActivateFn = () => inject(Session).can('billing:manage');
```

## 6. Encontrabilidad

- Ofrecé búsqueda global si el producto tiene mucho contenido/secciones.
- Etiquetas de menú con el vocabulario del usuario, no con jerga interna ni nombres de módulos técnicos.
- Estados vacíos con enlaces a la acción relevante (ver `frontend-ux-states`).

## Anti-patrones

- Navegación que copia la estructura de módulos del backend.
- Ítem activo indistinguible; el usuario no sabe dónde está.
- Filtros/tab que no viven en la URL: recargar pierde el contexto, no se puede compartir.
- Confiar en el menú oculto como control de acceso.
- Menú y guard con listas de roles distintas que se desincronizan.

## Checklist

- [ ] Rutas organizadas por el modelo del usuario; tareas frecuentes a pocos clics.
- [ ] Ítem activo inequívoco; patrón de nav adecuado y usable en móvil.
- [ ] Breadcrumbs en jerarquías profundas; títulos coherentes.
- [ ] Filtros/tab/cursor en la URL; deep links funcionan en frío.
- [ ] Menú por rol, pero cada ruta con guard y cada endpoint validando permiso.
- [ ] Menú y guard derivan de la misma fuente de permisos.
