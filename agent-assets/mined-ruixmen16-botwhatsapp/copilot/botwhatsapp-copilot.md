# WhatsApp Bot con AI - Instrucciones de Copilot

Este proyecto es un bot automatizado de WhatsApp que utiliza inteligencia artificial para responder mensajes automáticamente.

## Tecnologías Utilizadas
- Node.js
- whatsapp-web.js - Para interactuar con WhatsApp Web
- OpenAI API - Para generar respuestas inteligentes
- dotenv - Para manejo de variables de entorno

## Estructura del Proyecto
```
ROBOT/
├── src/
│   ├── bot.js          # Lógica principal del bot
│   ├── config.js       # Configuración del bot
│   └── utils/
│       └── openai.js   # Integración con OpenAI
├── .env                # Variables de entorno
├── package.json        # Dependencias del proyecto
└── README.md          # Documentación
```

## Funcionalidades Principales
- Lectura automática de mensajes de WhatsApp
- Generación de respuestas usando OpenAI
- Filtros para evitar responder a todos los mensajes
- Configuración personalizable de comportamiento