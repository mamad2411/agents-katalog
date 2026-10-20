<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-darien-alexander-torres
description: CTF writeups and security challenges by Darien-Alexander-Torres.
---

# Writeups by Darien-Alexander-Torres

Source repository: `/repos/Darien-Alexander-Torres`

## Repository Index

- Offensive-Security-Pentesting-Reports/README.md

## Writeup Content


### File: Offensive-Security-Pentesting-Reports/README.md

🛡️ Web Application Pentesting Report: SegaPharmacy

Este repositorio contiene el informe técnico detallado de la auditoría de seguridad y pruebas de penetración realizadas a la plataforma web SegaPharmacy. El objetivo del proyecto fue identificar vulnerabilidades críticas que pudieran comprometer la integridad de la base de datos y la confidencialidad de los usuarios.

📊 Resumen Ejecutivo

La auditoría se realizó bajo una metodología de Caja Negra (Black Box), simulando un ataque externo para evaluar la resistencia de los controles de seguridad actuales. Durante el proceso, se detectaron múltiples vectores de ataque que permitieron el acceso no autorizado a información sensible.

🛠️ Metodología y Herramientas

Se siguió el estándar de pruebas de penetración web para garantizar una cobertura exhaustiva:

 Reconocimiento: Análisis de la arquitectura y mapeo de puntos de entrada de datos.

Interceptación de Tráfico: Uso de Burp Suite para analizar y manipular peticiones HTTP/HTTPS.

Escaneo de Vulnerabilidades: Empleo de OWASP ZAP para la detección automatizada de fallos comunes.

Explotación Controlada: Validación manual de hallazgos para confirmar el impacto real.

🔍 Hallazgos Críticos Identificados

1. Inyección SQL (SQLi)

    Vulnerabilidad: Falta de sanitización en el formulario de inicio de sesión.

    Impacto: Se logró realizar un Bypass de Autenticación mediante la inyección de comandos SQL, obteniendo acceso a niveles administrativos sin credenciales válidas.

2. Cross-Site Scripting (XSS) Reflejado

    Vulnerabilidad: Los parámetros de búsqueda no filtran caracteres especiales de JavaScript.

    Impacto: Capacidad de ejecutar scripts en el navegador de otros usuarios, facilitando el robo de cookies de sesión.

3. Almacenamiento Inseguro de Credenciales

    Vulnerabilidad: Las contraseñas en la base de datos se encuentran almacenadas en texto plano o con cifrados débiles.

    Impacto: En caso de una filtración de datos, la información de acceso de todos los usuarios queda expuesta de inmediato.

💡 Recomendaciones de Mitigación

    Implementación de Consultas Parametrizadas: Sustituir la concatenación de cadenas por sentencias preparadas (PDO/Prepared Statements) para neutralizar ataques SQLi.

Hashing de Contraseñas: Adoptar algoritmos de derivación de claves robustos como Argon2 o BCRYPT con salt aleatorio.

Sanitización de Salidas: Implementar filtros globales para codificar caracteres especiales antes de renderizarlos en el navegador (XSS protection).

⚠️ Nota de Ética: Este análisis se realizó estrictamente con fines académicos y bajo un acuerdo de autorización mutua entre el equipo auditor y el propietario del sistema. No se realizaron cambios permanentes ni extracciones de datos reales fuera del entorno de prueba.

