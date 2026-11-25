---
name: Blog a Google Slides
description: Convierte entradas de blog en presentaciones visuales sorprendentes para Google Slides
---

# Blog a Google Slides

Esta habilidad transforma entradas de blog en presentaciones profesionales y visualmente impactantes para Google Slides. El resultado incluye un script de Google Apps Script listo para ejecutar que genera automáticamente las diapositivas.

## Requisitos Previos

- Cuenta de Google con acceso a Google Slides
- Acceso a Google Apps Script (script.google.com)
- URL o contenido de la entrada de blog

## Proceso de Transformación

### Paso 1: Analizar el Contenido del Blog

Lee y analiza la entrada de blog identificando:

| Elemento | Uso en la Presentación |
|----------|----------------------|
| Título principal | Diapositiva de portada |
| Subtítulos/H2 | Diapositivas de sección |
| Párrafos clave | Puntos de contenido |
| Listas | Bullets visuales |
| Citas destacadas | Diapositivas de cita |
| Datos/estadísticas | Diapositivas de impacto visual |
| Conclusiones | Diapositiva de cierre |

### Paso 2: Estructurar la Presentación

Crea una estructura que siga este flujo:

1. **Portada** - Título impactante + subtítulo
2. **Agenda/Índice** - Temas a cubrir (opcional)
3. **Introducción** - Contexto y gancho
4. **Secciones de contenido** - Una por cada H2 del blog
5. **Datos destacados** - Estadísticas o citas importantes
6. **Conclusión** - Resumen de puntos clave
7. **Llamada a la acción** - Siguiente paso para el lector
8. **Cierre** - Agradecimiento y contacto

### Paso 3: Diseñar el Estilo Visual

> [!IMPORTANT]
> Las presentaciones deben ser **visualmente sorprendentes**. Aplica estos principios:

#### Paleta de Colores

Sugiere una paleta coherente basada en el tema del blog:

```javascript
const PALETAS = {
  tecnologia: {
    primario: '#1a73e8',    // Azul Google
    secundario: '#34a853',   // Verde éxito
    acento: '#ea4335',       // Rojo atención
    fondo: '#f8f9fa',        // Gris claro
    texto: '#202124'         // Negro suave
  },
  negocios: {
    primario: '#1e3a5f',    // Azul corporativo
    secundario: '#c9a227',   // Dorado
    acento: '#e74c3c',       // Rojo
    fondo: '#ffffff',
    texto: '#2c3e50'
  },
  creativo: {
    primario: '#6c5ce7',    // Púrpura vibrante
    secundario: '#00cec9',   // Turquesa
    acento: '#fd79a8',       // Rosa
    fondo: '#dfe6e9',
    texto: '#2d3436'
  },
  salud: {
    primario: '#00b894',    // Verde menta
    secundario: '#0984e3',   // Azul cielo
    acento: '#fdcb6e',       // Amarillo suave
    fondo: '#ffffff',
    texto: '#2d3436'
  }
};
```

#### Tipografía Recomendada

- **Títulos**: Montserrat Bold, Poppins Bold, o Playfair Display
- **Cuerpo**: Open Sans, Roboto, o Lato
- **Tamaño título**: 44-60pt
- **Tamaño subtítulo**: 28-36pt
- **Tamaño cuerpo**: 18-24pt

#### Principios de Diseño

1. **Regla del 6x6**: Máximo 6 puntos por diapositiva, máximo 6 palabras por punto
2. **Espacio en blanco**: Deja respirar el contenido (40% vacío mínimo)
3. **Una idea por diapositiva**: No sobrecargues
4. **Contraste alto**: Asegura legibilidad
5. **Imágenes de calidad**: Usa fotos profesionales o iconos vectoriales

### Paso 4: Generar el Script de Google Apps Script

Genera un script completo que el usuario pueda ejecutar en Google Apps Script:

```javascript
/**
 * Script generado por la habilidad Blog a Slides
 * Ejecuta la función crearPresentacion() para generar las diapositivas
 */

function crearPresentacion() {
  // Crear nueva presentación
  const presentacion = SlidesApp.create('Título de la Presentación');
  
  // Configurar dimensiones (16:9)
  const slides = presentacion.getSlides();
  
  // Eliminar diapositiva en blanco inicial
  if (slides.length > 0) {
    slides[0].remove();
  }
  
  // Definir colores del tema
  const COLORES = {
    primario: '#1a73e8',
    secundario: '#34a853',
    fondo: '#ffffff',
    texto: '#202124'
  };
  
  // === DIAPOSITIVA 1: PORTADA ===
  agregarPortada(presentacion, COLORES);
  
  // === DIAPOSITIVAS DE CONTENIDO ===
  // [Agregar según el análisis del blog]
  
  // === DIAPOSITIVA FINAL ===
  agregarCierre(presentacion, COLORES);
  
  Logger.log('Presentación creada: ' + presentacion.getUrl());
  return presentacion.getUrl();
}

function agregarPortada(presentacion, colores) {
  const slide = presentacion.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  
  // Fondo con gradiente o color sólido
  slide.getBackground().setSolidFill(colores.primario);
  
  // Título principal
  const titulo = slide.insertTextBox('TÍTULO IMPACTANTE');
  titulo.setTop(200).setLeft(50).setWidth(620).setHeight(100);
  titulo.getText().getTextStyle()
    .setFontFamily('Montserrat')
    .setFontSize(48)
    .setBold(true)
    .setForegroundColor('#ffffff');
  titulo.getText().getParagraphStyle().setParagraphAlignment(SlidesApp.ParagraphAlignment.CENTER);
  
  // Subtítulo
  const subtitulo = slide.insertTextBox('Subtítulo descriptivo');
  subtitulo.setTop(320).setLeft(50).setWidth(620).setHeight(60);
  subtitulo.getText().getTextStyle()
    .setFontFamily('Open Sans')
    .setFontSize(24)
    .setForegroundColor('#e8eaed');
  subtitulo.getText().getParagraphStyle().setParagraphAlignment(SlidesApp.ParagraphAlignment.CENTER);
}

function agregarDiapositiva(presentacion, titulo, puntos, colores) {
  const slide = presentacion.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  slide.getBackground().setSolidFill(colores.fondo);
  
  // Título de sección
  const tituloBox = slide.insertTextBox(titulo);
  tituloBox.setTop(40).setLeft(50).setWidth(620).setHeight(60);
  tituloBox.getText().getTextStyle()
    .setFontFamily('Montserrat')
    .setFontSize(36)
    .setBold(true)
    .setForegroundColor(colores.primario);
  
  // Puntos de contenido
  let yPos = 130;
  puntos.forEach((punto, index) => {
    const puntoBox = slide.insertTextBox('• ' + punto);
    puntoBox.setTop(yPos).setLeft(70).setWidth(580).setHeight(50);
    puntoBox.getText().getTextStyle()
      .setFontFamily('Open Sans')
      .setFontSize(20)
      .setForegroundColor(colores.texto);
    yPos += 55;
  });
}

function agregarCita(presentacion, cita, autor, colores) {
  const slide = presentacion.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  slide.getBackground().setSolidFill(colores.secundario);
  
  // Cita grande centrada
  const citaBox = slide.insertTextBox('"' + cita + '"');
  citaBox.setTop(150).setLeft(60).setWidth(600).setHeight(150);
  citaBox.getText().getTextStyle()
    .setFontFamily('Playfair Display')
    .setFontSize(32)
    .setItalic(true)
    .setForegroundColor('#ffffff');
  citaBox.getText().getParagraphStyle().setParagraphAlignment(SlidesApp.ParagraphAlignment.CENTER);
  
  // Autor
  const autorBox = slide.insertTextBox('— ' + autor);
  autorBox.setTop(320).setLeft(60).setWidth(600).setHeight(40);
  autorBox.getText().getTextStyle()
    .setFontFamily('Open Sans')
    .setFontSize(18)
    .setForegroundColor('#e8eaed');
  autorBox.getText().getParagraphStyle().setParagraphAlignment(SlidesApp.ParagraphAlignment.CENTER);
}

function agregarCierre(presentacion, colores) {
  const slide = presentacion.appendSlide(SlidesApp.PredefinedLayout.BLANK);
  slide.getBackground().setSolidFill(colores.primario);
  
  const gracias = slide.insertTextBox('¡Gracias!');
  gracias.setTop(180).setLeft(50).setWidth(620).setHeight(80);
  gracias.getText().getTextStyle()
    .setFontFamily('Montserrat')
    .setFontSize(56)
    .setBold(true)
    .setForegroundColor('#ffffff');
  gracias.getText().getParagraphStyle().setParagraphAlignment(SlidesApp.ParagraphAlignment.CENTER);
  
  const contacto = slide.insertTextBox('contacto@ejemplo.com | @usuario');
  contacto.setTop(280).setLeft(50).setWidth(620).setHeight(40);
  contacto.getText().getTextStyle()
    .setFontFamily('Open Sans')
    .setFontSize(20)
    .setForegroundColor('#e8eaed');
  contacto.getText().getParagraphStyle().setParagraphAlignment(SlidesApp.ParagraphAlignment.CENTER);
}
```

### Paso 5: Entregar el Resultado

Proporciona al usuario:

1. **Script personalizado** con el contenido del blog transformado
2. **Instrucciones de ejecución** (ver sección siguiente)
3. **Sugerencias de imágenes** para cada diapositiva
4. **Paleta de colores** en formato hexadecimal

## Instrucciones para el Usuario

### Ejecutar el Script

1. Abre [script.google.com](https://script.google.com)
2. Crea un nuevo proyecto
3. Pega el script generado
4. Haz clic en **Ejecutar** → `crearPresentacion`
5. Autoriza los permisos cuando se soliciten
6. Revisa el log para obtener el enlace de la presentación

> [!TIP]
> Puedes modificar los colores en el objeto `COLORES` para personalizar la paleta.

## Consideraciones Especiales

> [!WARNING]
> Google Slides tiene límites de API. Si el blog es muy largo, divide en múltiples presentaciones.

> [!CAUTION]
> Las imágenes deben agregarse manualmente o mediante URLs públicas. El script solo crea la estructura.

## Mejoras Visuales Adicionales

Para presentaciones aún más impactantes, sugiere al usuario:

| Elemento | Recurso Gratuito |
|----------|-----------------|
| Iconos | [Flaticon](https://flaticon.com), [Heroicons](https://heroicons.com) |
| Fotos | [Unsplash](https://unsplash.com), [Pexels](https://pexels.com) |
| Paletas | [Coolors](https://coolors.co), [ColorHunt](https://colorhunt.co) |
| Mockups | [Smartmockups](https://smartmockups.com) |

## Solución de Problemas

| Problema | Solución |
|----------|----------|
| Error de permisos | Autoriza la app en la primera ejecución |
| Script no corre | Verifica que seleccionaste la función correcta |
| Colores no aparecen | Asegúrate de usar formato hexadecimal (#RRGGBB) |
| Texto cortado | Reduce el tamaño de fuente o el contenido |
