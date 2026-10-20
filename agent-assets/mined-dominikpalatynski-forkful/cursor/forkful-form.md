---
description: Rules for creating forms in the application
globs:
alwaysApply: false
---

## Forms

### Form Structure
- Use shadcn `<Form>` component to define Form wrapper
- Pass into `<Form>` form schema using `useForm` from `"hooks/use-form.ts"`

### Form Setup
```typescript
type CompanyFormSchemaType = z.infer<typeof CompanyFormSchema>;
const form = useForm({
  schema: CompanyFormSchema,
  defaultValues: {
    name: company.name,
    nip: company.nip,
    city: company.city,
    street: company.street,
    postalCode: company.postalCode,
    email: company.email,
    phone: company.phone,
    website: company.website,
  },
});
```

### Form Fields Structure
Each field in form should be wrapped into:
- `<FormField>` component
- `<FormItem>` 
- `<Label>`
- `<FormControl>`
- Input component (depends on input type)

Example:
```tsx
<FormField
  control={form.control}
  name="city"
  render={({ field }) => (
    <FormItem className="w-full">
      <Label>Miasto *</Label>
      <FormControl>
        <Input
          className="w-full"
          type="text"
          placeholder="Miasto"
          autoComplete="address-level2"
          {...field}
        />
      </FormControl>
      <FormMessage />
    </FormItem>
  )}
/>
```

### Dynamic Arrays
For dynamic arrays of form fields (add/remove items), use `useFieldArray` from react-hook-form:
```typescript
const { fields, append, remove } = useFieldArray({
  control: form.control,
  name: "arrayFieldName",
});
```

### Form Submission
Submit form should be defined on the top of the form:
```tsx
<form onSubmit={form.handleSubmit(onSubmit)}>
```

With schema from useForm:
```typescript
const onSubmit = (data: CompanyFormSchemaType) => {
  if (isPending) return;
  toast.promise(
    updateCompanyDetails({
      id: company.id,
      ...data,
    }),
    {
      loading: "Zapisywanie zmian",
      success: "Zmiany zostały zapisane",
      error: "Wystąpił błąd podczas zapisywania zmian",
    },
  );
};
```

### Submit Button
Submit form should be done by Button with type submit:
```tsx
<Button
  type="submit"
  disabled={!form.formState.isDirty || isPending}
>
  Zapisz
</Button>
```

### Required Imports
```typescript
import { useForm } from "@/hooks/use-form";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input"
import { toast } from "sonner";
```
