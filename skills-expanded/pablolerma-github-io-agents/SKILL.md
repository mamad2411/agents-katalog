# AGENTS.md

Guía para agentes de IA que trabajen en este repositorio.

## Tecnología

- **Jekyll 3.9** con el plugin `github-pages`
- **Ruby 3.2.0** gestionado con rbenv (versión en `.ruby-version`)
- Publicado en **GitHub Pages** desde la rama `main`

## Setup

```bash
./setup.sh                          # instala dependencias
bundle exec jekyll serve --watch    # servidor local en localhost:4000
```

## Convenciones

- Los posts van en `_posts/` con el formato `YYYY-MM-DD-titulo.md`
- El front matter mínimo de un post es `layout`, `title` y `date`
- Los estilos están en `_sass/` — no modificar CSS directamente en `css/`

## Dependencias

Gestionadas con Bundler. Para actualizar:

```bash
bundle update
```

Verificar siempre que la web se renderiza correctamente tras actualizar dependencias.

## Seguridad

- Las vulnerabilidades de dependencias se detectan vía GitHub Dependabot
- Ante cualquier alerta, actualizar con `bundle update` y verificar visualmente
