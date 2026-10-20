---
description: "Crea un formulario usando TanStack Query, validación con Zod y TanStack Form."
name: "Crear formulario con TanStack Query, Zod y TanStack Form"
argument-hint: "Describe el formulario y los campos que necesitas"
agent: "agent"
---
Crea un formulario en React siguiendo estas pautas:

- Usa **TanStack Form** para la gestión del formulario.
- Implementa la validación de los campos usando **Zod**.
- Utiliza **TanStack Query** para manejar el envío de datos (mutación) y la obtención de datos si es necesario.
- Genera los componentes de campos de formulario según la descripción proporcionada.
- Incluye ejemplos de validación y mensajes de error.
- El código debe ser modular y fácil de mantener.
- Si se especifica, incluye lógica para cargar datos iniciales (edición).

Ejemplo de salida:

```tsx
import { useForm } from '@tanstack/react-form';
import { z } from 'zod';
import { useMutation } from '@tanstack/react-query';

const schema = z.object({
  nombre: z.string().min(1, 'El nombre es obligatorio'),
  email: z.string().email('Email inválido'),
});

export function MiFormulario() {
  const mutation = useMutation(/* ... */);
  const form = useForm({
    defaultValues: { nombre: '', email: '' },
    schema,
    onSubmit: values => mutation.mutate(values),
  });

  return (
    <form onSubmit={form.handleSubmit}>
      {/* Campos y mensajes de error */}
    </form>
  );
}
```

Adapta el formulario a los campos y reglas que se indiquen en la petición.