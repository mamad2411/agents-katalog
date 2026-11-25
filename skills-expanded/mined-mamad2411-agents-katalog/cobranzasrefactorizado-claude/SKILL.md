# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Descripción del Proyecto

**TV Cable Cobranzas** - Sistema de Gestión de Cobranza de TV Cable. Sistema basado en React para gestión de cobranzas de servicios de TV cable con acceso basado en roles (Admin, SubAdmin, Cobrador, Cliente) usando LocalStorage como base de datos simulada.

## Comandos de Desarrollo

```bash
# Navegar primero al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Servidor de desarrollo (puerto 3000)
npm run dev
# o
npm start

# Compilar para producción
npm run build

# Previsualizar build de producción
npm preview
```

## Stack Tecnológico

- **Frontend**: React 18.3 + Vite 5.4
- **Enrutamiento**: React Router DOM 6.26
- **Gestión de Estado**: Zustand 4.5 (con middleware persist)
- **Estilos**: Tailwind CSS 3.4
- **Formularios**: React Hook Form 7.52
- **Almacenamiento**: LocalStorage (base de datos simulada)
- **Generación de PDFs**: @react-pdf/renderer 3.4
- **Gráficos**: Recharts 2.12
- **Alertas**: SweetAlert2 11.10
- **Manejo de Fechas**: date-fns 2.30

## Arquitectura

### Gestión de Estado (Stores de Zustand)

La aplicación usa stores de Zustand ubicados en `frontend/src/stores/`:

- **authStore**: Autenticación de usuarios, login/logout, validación de token, gestión de sesión
- **clientStore**: Operaciones CRUD de clientes, filtrado, búsqueda
- **clientExtendedStore**: Datos extendidos de clientes (detalles de instalación, info de facturación)
- **paymentStore**: Seguimiento de pagos, métricas, filtrado, actualización de estados
- **monthlyDebtStore**: Seguimiento y cálculos de deudas mensuales
- **cashBoxStore**: Gestión de caja de cobradores con estado complejo (solicitudes, transacciones, validación)
- **serviceStore**: Gestión de planes de servicio (básico/estándar/premium)
- **paymentMethodStore**: Configuración de métodos de pago
- **voucherStore**: Carga y validación de comprobantes
- **notificationStore**: Notificaciones del sistema
- **alertStore**: Alertas para cobradores
- **backupStore**: Operaciones de respaldo/restauración de datos
- **settingsStore**: Configuraciones de la aplicación
- **uiStore**: Estado de UI (sidebar, loading, navegación móvil)
- **paymentReceiptStore**: Generación de recibos PDF

Todos los stores siguen los patrones de Zustand con middleware `persist` para sincronización con LocalStorage.

### Sistema de Base de Datos Simulada

Ubicado en `frontend/src/services/mock/`:

- **db.js**: Capa de abstracción de LocalStorage con control de versiones (`DB_VERSION`)
- **server.js**: Servidor API REST simulado con simulación de latencia, manejo de errores, paginación
- **seeder.js**: Genera datos de prueba realistas (200 clientes, pagos, usuarios, etc.)
- **schemas/**: Esquemas de validación de datos para entidades (client, payment, user, service, etc.)

**Importante**: La base de datos se regenera automáticamente al cambiar la versión. El seeder crea datos de prueba localizados para Perú con nombres, direcciones y teléfonos realistas.

### Enrutamiento y Acceso Basado en Roles

Las rutas se definen en `App.jsx` con cuatro secciones basadas en roles:

1. **Admin** (`/admin/*`): Acceso completo a todas las funcionalidades
2. **SubAdmin** (`/subadmin/*`): Capacidades administrativas limitadas, no puede gestionar usuarios
3. **Cobrador** (`/collector/*`): Gestión de clientes, cobro de pagos, caja
4. **Cliente** (`/client/*`): Ver deudas, subir comprobantes de pago

El componente `ProtectedRoute` refuerza el control de acceso basado en roles.

### Estructura de Páginas

```
frontend/src/pages/
├── admin/          # Páginas solo para admin (15 páginas)
│   ├── Dashboard.jsx
│   ├── ClientManagement.jsx (archivo complejo de 105k+)
│   ├── PaymentManagement.jsx
│   ├── MonthlyDebts.jsx
│   ├── CollectorManagement.jsx
│   ├── CashBoxManagement.jsx
│   ├── ServiceManagement.jsx
│   ├── BackupManagement.jsx
│   ├── Reports.jsx
│   ├── Analytics.jsx
│   └── ...
├── collector/      # Páginas de cobrador (5 páginas)
│   ├── Dashboard.jsx
│   ├── Clients.jsx
│   ├── Payments.jsx
│   ├── CashBox.jsx
│   └── Vouchers.jsx
├── client/         # Portal de cliente (2 páginas)
│   ├── Dashboard.jsx
│   └── UploadVoucher.jsx
├── subadmin/       # Páginas de SubAdmin
│   └── UserManagement.jsx
└── Login.jsx       # Autenticación
```

### Lógica de Negocio Clave

#### Calculadora de Facturación (`utils/billingCalculator.js`)

**Reglas de Prorrateo**:
- Instalación en/después del día 26: Primer mes gratis, facturación comienza el mes siguiente
- Instalación antes del día 26: Cobro prorrateado basado en días usados
- Fórmula: `(tarifaMensual * díasUsados) / díasDelMes`

#### Planes de Servicio

Definidos en `constants/ui.js`:
- **Básico**: S/ 50/mes
- **Estándar**: S/ 80/mes
- **Premium**: S/ 120/mes

#### Servicios de Automatización (`services/automation/`)

- **paymentStatusService.js**: Actualiza automáticamente el estado de pagos basado en fechas de vencimiento, marca pagos vencidos
- **clientStatusService.js**: Actualiza automáticamente el estado de clientes basado en historial de pagos

### Organización de Componentes

```
frontend/src/components/
├── layout/         # Componentes de layout (Header, Sidebar, MobileNav)
├── common/         # Componentes reutilizables (modales, filtros, alertas, etc.)
├── reports/        # Componentes de generación de reportes
└── subadmin/       # Componentes específicos de SubAdmin
```

### Patrón de Flujo de Datos

1. **Páginas** llaman acciones de stores de Zustand
2. **Stores** interactúan con `mockServer` (services/mock/server.js)
3. **MockServer** realiza operaciones CRUD en `db` (services/mock/db.js)
4. **DB** persiste en LocalStorage con prefijo `tv-cable:`
5. **Actualizaciones de UI** vía suscripciones de Zustand

### Funcionalidades de Importación/Exportación

- **Importación Excel**: `modules/import/ExcelImporter.js` - Importación masiva de clientes desde XLSX
- **Exportación Excel**: `utils/excelExport.js` - Exportar matriz de deudas mensuales a XLSX
- **Reportes PDF**: `services/reports/pdfGenerator.jsx` - Generar recibos de pago y reportes
- **Sistema de Respaldo**: Respaldo/restauración completo de LocalStorage en formato JSON

## Tareas Comunes de Desarrollo

### Agregar una Nueva Funcionalidad

1. Crear store en `stores/` si es necesario (seguir patrones de Zustand existentes)
2. Agregar validación de esquema en `services/mock/schemas/`
3. Agregar endpoints en mock server en `services/mock/server.js`
4. Crear componente de página en el subdirectorio apropiado de `pages/`
5. Agregar ruta en `App.jsx` con wrapper `ProtectedRoute`
6. Actualizar navegación en `components/layout/Sidebar.jsx`

### Trabajar con Formularios

Usar el patrón de React Hook Form visto en toda la base de código:

```jsx
import { useForm } from 'react-hook-form';

const { register, handleSubmit, formState: { errors } } = useForm();
```

### Generación de Datos Simulados

Para regenerar datos de prueba:
1. Limpiar localStorage: `localStorage.clear()`
2. Recargar app - el seeder se ejecuta automáticamente
3. O incrementar `DB_VERSION` en `services/mock/db.js`

Ver `GENERAR_DATOS_PRUEBA.md` para instrucciones detalladas.

### Convenciones de Estilos

- Utilidades de Tailwind CSS para todos los estilos
- Colores personalizados definidos en `tailwind.config.js` (primary, success, error, warning, info)
- Animaciones personalizadas: fade-in, slide-up, slide-down
- Diseño responsivo: mobile-first con breakpoints `sm:`, `md:`, `lg:`

### Probar Operaciones de Fin de Mes

Usar la página de prueba en `/test/month-end` (ver `pages/TestMonthEnd.jsx`) para verificar la lógica de cierre de mes sin esperar transiciones de mes reales.

## Autenticación y Usuarios por Defecto

Los usuarios simulados se generan en el seeder con estas credenciales por defecto:

- **Admin**: `admin` / `admin123`
- **Cobrador**: `collector` / `collector123`
- **Cliente**: `client-1` / `password123`

Las sesiones persisten vía middleware persist de Zustand con la clave `tv-cable-auth` en localStorage.

## Notas Importantes

- **Sin Backend**: Todo se ejecuta en el navegador vía base de datos simulada en LocalStorage
- **Persistencia de Datos**: Todos los datos se almacenan con prefijo `tv-cable:` en localStorage
- **Control de Versión**: `DB_VERSION` en db.js fuerza regeneración de datos cuando cambia
- **Simulación Asíncrona**: MockServer agrega latencia de 100-600ms para simular API real
- **Simulación de Errores**: Tasa de error aleatorio del 2% en API simulada (configurable en server.js)
- **Localización Peruana**: Toda la moneda (S/), números telefónicos (+51), direcciones usan convenciones peruanas

## Alias de Archivos

Vite configurado con alias `@` apuntando al directorio `/src` (ver `vite.config.js`).

## Solución de Problemas

- **Problemas de datos**: Limpiar localStorage y recargar
- **Rutas obsoletas**: Verificar que los requisitos de rol de `ProtectedRoute` coincidan con el rol del usuario
- **Store no se actualiza**: Verificar que la acción del store se está llamando y la operación de db tiene éxito
- **Errores de compilación**: Asegurar que estás en el directorio `frontend/` al ejecutar comandos npm
