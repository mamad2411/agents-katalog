---
name: piezas-graficas
description: Reglas del equipo de Marketing para piezas graficas premium sobre la marca FAAST - one-pager con el producto desglosado (un bloque por parte con mini-captura real, nombre, una linea de valor y cifra con nota), panfleto por parte, piezas para redes (LinkedIn, Instagram, banners, carruseles con una parte por lamina) e identidad de campana como acento sobre la marca, con jerarquia editorial que se lee en 3 segundos, grilla, tipografia, color, tratamiento de capturas, medidas exactas (A4, Carta, A5, 1200x627, 1080x1350, 1080x1080, 1080x1920), preparacion para imprenta (sangrado 3 mm, marcas de corte, fuentes embebidas, PDF), export desde HTML autocontenido con Playwright o Chrome headless, verificacion por export, uso del logo y de marcas de terceros, y los anti-patrones que hacen que una pieza se vea generica. Cargala antes de diseñar impresos o piezas de redes.
---

# Piezas graficas — editorial, de marca, parte por parte

## 1. Principios
1. **Se entiende en 3 segundos**: titular → imagen → partes → cifra → llamado.
2. **Una imagen dominante** (captura real o recurso de marca), no cinco medianas.
3. **Desglose**: el one-pager es el mapa del producto en una hoja; cada panfleto es UNA parte.
4. **Marca FAAST primero**; la identidad de campana es un acento (ver `marca-faast`).
5. **Menos es mas caro**: aire, 2 tipografias, un acento.

## 2. One-pager (A4 210x297 mm; Carta si el brief lo pide)
```
Cabecera: logo (zona de proteccion) · pais/fecha opcional
Titular (≤ 7 palabras, la propuesta de valor) · bajada (1 linea)
Grilla de partes (4-8 bloques): mini-captura real · nombre de la parte · 1 linea · cifra[nota]
Banda de prueba (opcional): 2-3 cifras de marca citadas o benchmark resumido con fuente
Llamado a la accion + contacto autorizado + QR probado
Notas al pie 7-8 pt: fuentes [F..] y supuestos [S..]
```
Margen seguro 10 mm; cuerpo minimo 9 pt; titular 32-48 pt.

## 3. Panfleto por parte (A4 o A5; diptico/triptico si se pide)
Portada: imagen principal de la parte + titular · Interior: que es y para quien, como funciona (3-4
pasos con capturas), que gana (cifra con nota), antes/despues · Contraportada: marca, otras partes
en una linea, contacto.

## 4. Redes
| Red | Formato | Reglas |
|---|---|---|
| LinkedIn | 1200x627 (enlace), 1080x1350 (vertical), carrusel PDF 1080x1350 | texto ≤ 20% de la imagen; titular legible en miniatura |
| Instagram | 1080x1080, 1080x1350, historia 1080x1920 | zona segura de historias: 250 px arriba y abajo |
| Banner | segun brief | peso ≤ 150 KB si es web |
Carrusel: lamina 1 gancho, una lamina por parte, ultima con marca y llamado. Exportar PNG 2x.

## 5. Identidad de campana
Acento derivado de la marca (un tono del verde de marca, un neutro de campana), un recurso grafico
(linea, reticula, tratamiento de luz sobre capturas), tipografia de display con licencia. Se
documenta en `identidad-campana.md` y la aprueba el director. Nunca un logo nuevo que compita con
el de FAAST.

## 6. Color, tipografia y capturas
- Color: neutros + acento de marca; contraste AA; el verde del isotipo (#71af26) no se usa como
  texto pequeño sobre blanco (no cumple AA).
- Tipografia: las confirmadas en el kit (el sitio usa Lato y Open Sauce One); embebidas en el PDF.
- Capturas: reales, 2x, recorte limpio, radio suave, sombra difusa; prototipos rotulados.

## 7. Imprenta
PDF con sangrado 3 mm, marcas de corte, fuentes embebidas, imagenes ≥ 300 ppp al tamaño final,
negro de texto 100% K si la imprenta lo pide (consultar), sin elementos importantes a menos de 5 mm
del corte. Version digital aparte (sin sangrado, RGB, liviana).

## 8. Construccion y export
- HTML/CSS autocontenido por pieza (`@page { size: A4; margin: 0 }`; tipografias embebidas).
- PDF: Playwright (`page.pdf` con `printBackground: true`) o Chrome headless `--print-to-pdf`.
- PNG: `browser_resize` a la medida exacta + `browser_take_screenshot` (2x para redes).
- Skills si existen: `high-end-visual-design`, `impeccable`, `minimalist-ui`, `design-taste-frontend`,
  `brandkit` (tableros de identidad de campana), `dataviz`, `pdf`.

## 9. Verificacion por export
Texto que no desborda · contraste AA · cuerpo minimo · tildes, eñes, ¿ ¡ · cifras con nota · QR y
enlaces probados · medida exacta · sangrado correcto · sin informacion interna · logo correcto.

## 10. Logo y marcas de terceros
El logo oficial no se redibuja, recolorea, deforma ni se le agregan efectos; si solo existe la
version provisional, se anota. Logos de clientes o competidores: solo con autorizacion registrada,
nunca como propios.

## 11. Anti-patrones
Plantillas de Canva/Word · iconos de stock en circulos de colores · fotos cliche · mapas decorativos
· degradados arcoiris · sombras duras · 5 tipografias · texto justificado con rios · muro de texto ·
mas de 8 bloques · mockups genericos de dashboards · pantallas imaginadas · cifras sin fuente.

## 12. Reticulas de referencia
| Pieza | Columnas | Filas (modulos) | Margen | Medianil | Linea base |
|---|---|---|---|---|---|
| One-pager A4 | 12 | 8 | 12-15 mm | 4-5 mm | 12 pt |
| Panfleto A5 | 6 | 6 | 10 mm | 4 mm | 12 pt |
| Triptico (por panel) | 4 | 6 | 8 mm | 3 mm | 11 pt |
| Post 1080 px | 6 | 6 | 64-80 px | 24 px | 8 px |
| Historia 1080x1920 | 6 | 10 | 80 px lateral, 250 px arriba/abajo | 24 px | 8 px |
Todo bloque cae en la reticula; la excepcion (una imagen a sangre) es intencional y una sola por pieza.

## 13. Preimpresion paso a paso
1. Construir a tamaño final + 3 mm de sangrado por lado; textos y logo dentro del area segura (5 mm).
2. Imagenes a ≥ 300 ppp al tamaño final; capturas 2x si van grandes.
3. Exportar PDF con fondos y fuentes embebidas.
4. Pedir a la imprenta su norma (PDF/X-1a o PDF/X-4, perfil FOGRA39 o GRACoL, sangrado, marcas).
5. Convertir a CMYK si lo exige (Ghostscript:
   `gs -o salida-cmyk.pdf -sDEVICE=pdfwrite -sColorConversionStrategy=CMYK -sProcessColorModel=DeviceCMYK entrada.pdf`)
   o entregar RGB si la imprenta convierte con su perfil (preguntar).
6. Negro de texto 100% K; cobertura total ≤ 300% salvo indicacion.
7. Verificar: `pdffonts` (todas embebidas), `pdfimages -list` (ppp), `pdfinfo` (tamaño con sangrado).
8. Prueba de color (impresa o digital calibrada) del verde de marca antes del tiraje.

## 14. Ejemplos de estructura
**One-pager A4 (12 × 8)**: fila 1 logo y pais/fecha · filas 1-2 titular y bajada · filas 3-6 grilla 3 × 2
de partes (mini-captura, numero y nombre, una linea, cifra con nota) · fila 7 banda de prueba · fila 8
llamado, contacto y QR · pie con notas.
**Panfleto de una parte (triptico)**: portada con la parte → interior: que es y para quien · como
funciona (3 pasos con capturas) · antes/despues y que gana → contraportada: otras partes, contacto, QR.
**Carrusel LinkedIn (1080 × 1350)**: 1 gancho → 2..n una parte por lamina → ultima llamado y sitio.

## 15. Tipografia por medio
| Rol | Impreso | Redes (1080 px) |
|---|---|---|
| Titular | 36-48 pt | 72-96 px |
| Nombre de parte | 12-14 pt | 40-56 px |
| Cuerpo | 9-10,5 pt | 28-34 px (minimo 24) |
| Cifra | 20-28 pt | 96-160 px |
| Nota | 7-8 pt | 20-22 px |

## 16. QR y enlaces
QR ≥ 2 × 2 cm impreso (≥ 240 px en redes), zona de silencio de 4 modulos, alto contraste, enlace corto y
estable (sitio o agenda), probado con 2 telefonos; el enlace escrito al lado por si el QR no se lee.

## 17. Checklist de la pieza
- [ ] Desglose respetado (un bloque por parte / una parte por panfleto o lamina).
- [ ] Reticula y jerarquia: se entiende en 3 segundos; ≤ 2 familias; ≤ 4 tamaños.
- [ ] Capturas reales con origen; ≥ 300 ppp en impreso.
- [ ] Cifras con nota; sin informacion interna ni datos de clientes.
- [ ] Logo oficial sin alterar; marcas de terceros solo con autorizacion.
- [ ] Preimpresion completa (si aplica) y version digital liviana.
- [ ] Medidas de redes verificadas con fuente y fecha.

## 18. Derivar la identidad de campana (metodo)
1. Partir del kit: acento de marca (verde del isotipo), texto #151515, neutros.
2. Elegir UN recurso grafico que exprese el concepto de la campana (p. ej. "parte por parte" →
   numeracion 01-0n y una linea que une cada parte con su cifra).
3. Derivar tintes del acento para fondos (medir contraste con el texto: ≥ 4,5:1).
4. Definir el tratamiento de capturas (fondo estudio, radio, sombra) comun a deck, video e impresos.
5. Documentar en `identidad-campana.md` con lo permitido y lo prohibido; aprobacion del director.
La identidad se comparte con el disenador-presentaciones y el director-motion para que las tres
familias de piezas se vean de la misma campana.

## 19. Anti-patrones por pieza
| Pieza | Se ve barato cuando… | Se corrige con… |
|---|---|---|
| One-pager | muro de texto, 10 bloques, iconos de stock | 4-8 partes, una linea cada una, mini-capturas reales |
| Panfleto | mezcla varias partes, sin imagen dominante | una parte, captura grande, como funciona en 3 pasos |
| Carrusel | cada lamina con un estilo distinto, texto chico | reticula fija, una parte por lamina, cuerpo ≥ 28 px |
| Banner | titular largo, logo enorme, CTA invisible | ≤ 6 palabras, logo en su tamaño, CTA con contraste |
| Roll-up / feria | todo el folleto en vertical | una idea legible a 3 m, titular ≥ 150 pt |

## 20. Entrega
Por pieza: version digital (RGB, liviana) + version imprenta (si aplica) + preview PNG + `VERIFICACION.md`.
La aprobada pasa a `entregables/` con el nombre final que fija el director.
