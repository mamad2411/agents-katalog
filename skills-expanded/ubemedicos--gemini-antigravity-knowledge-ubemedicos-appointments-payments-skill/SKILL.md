---
name: ubemedicos-appointments-payments
description: Documentación del flujo entre el módulo de citas y el módulo de pagos. Úsalo cuando el usuario necesite implementar el checkout, validar confirmaciones de pago o entender la sincronización de estados entre una reserva y su transacción.
---

# Ubemedicos Appointments & Payments

## Ciclo de Vida de la Cita (`Appointment`)
Ubicación: `backend/apps/appointments/models.py`.

### Estados (`status`):
- `pending_confirmation`: Cita creada pero esperando validación o pago.
- `confirmed`: Cita válida y agendada (bloquea el slot).
- `cancelled_by_patient` / `cancelled_by_professional`: Cita anulada.
- `completed`: La consulta ya se realizó.
- `no_show_patient` / `no_show_professional`: Inasistencia.

## Módulo de Pagos (`Payment`)
Ubicación: `backend/apps/payments/models.py`.

### Estados (`status`):
- `pending`: Pago iniciado/esperando respuesta de pasarela.
- `succeeded`: Cobro exitoso.
- `failed`: Error en el cobro.
- `refunded`: Dinero devuelto al paciente.

## Relación y Lógica de Negocio
- **Vínculo**: Existe una relación `OneToOne` entre `Payment` y `Appointment`.
- **Sincronización**: 
  - Al recibir una notificación de pago exitoso (`succeeded`), el campo `is_paid` de la cita debe marcarse como `True`.
  - Dependiendo de la configuración del médico, un pago exitoso puede mover la cita automáticamente de `pending_confirmation` a `confirmed`.
- **Pagos Demo**: Actualmente el sistema utiliza un flujo de demostración donde la validación puede ser manual o simulada a través de `apps.payments.api_views`.

## Reglas de Slot
- Solo las citas en estado `pending_confirmation` o `confirmed` activan la restricción `UniqueConstraint` para evitar duplicidad de pacientes en el mismo horario para un profesional.
