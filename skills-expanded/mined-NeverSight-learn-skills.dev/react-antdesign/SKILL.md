---
name: react-antdesign
description: "Componentes React con Ant Design 5.29 y ProComponents v3. Cubre ConfigProvider + theme tokens, componentes core (Table, Form, Select, Modal, Drawer), ProTable y ProForm para productividad, integración con React Hook Form + Zod, Vite + tree shaking, y Ant Design Pro v6 (Tailwind + @tanstack/react-query). Actívala cuando el stack del equipo use Ant Design en vez de Tailwind/shadcn, especialmente en proyectos Sputnik (React + Vite + Ant Design)."
disable-model-invocation: true
---

# React + Ant Design 5

Guía de componentes React con Ant Design 5.29 + ProComponents v3. Stack del equipo Sputnik: React + Vite + Ant Design.

---

## Setup

```bash
npm install antd @ant-design/pro-components @ant-design/icons
npm install -D @ant-design/vite-plugin  # Tree shaking automático
```

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { antdComponents } from '@ant-design/vite-plugin';

export default defineConfig({
  plugins: [
    react(),
    antdComponents({ restrictToNamespace: true }), // Tree shaking: solo componentes usados
  ],
  css: {
    preprocessorOptions: {
      less: {
        javascriptEnabled: true,
      },
    },
  },
});
```

---

## ConfigProvider + Theme Tokens

```tsx
import { ConfigProvider, theme, App } from 'antd';
import type { ThemeConfig } from 'antd';

const customTheme: ThemeConfig = {
  token: {
    colorPrimary: '#1677ff',
    borderRadius: 6,
    fontFamily: 'Inter, -apple-system, sans-serif',
  },
  components: {
    Table: {
      headerBg: '#fafafa',
      rowHoverBg: '#f0f5ff',
    },
    Button: {
      borderRadius: 6,
      controlHeight: 36,
    },
  },
  algorithm: theme.defaultAlgorithm,  // o theme.darkAlgorithm para dark mode
};

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ConfigProvider theme={customTheme}>
      <App>
        {children}
      </App>
    </ConfigProvider>
  );
}
```

### CSS Variables mode (5.12+)

```tsx
<ConfigProvider theme={{ cssVar: true }}>
  {/* Genera --ant-color-primary, --ant-border-radius, etc. */}
  {children}
</ConfigProvider>
```

---

## Table — El componente más importante

```tsx
import { Table, Tag, Button, Space, Input } from 'antd';
import type { ColumnsType, TablePaginationConfig } from 'antd/es/table';
import type { SorterResult, FilterValue } from 'antd/es/table/interface';

interface OrderRecord {
  id: string;
  orderNumber: number;
  customerId: string;
  status: string;
  totalAmount: number;
  createdAt: string;
}

export function OrderTable() {
  const [data, setData] = useState<OrderRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({ current: 1, pageSize: 20, total: 0 });

  const columns: ColumnsType<OrderRecord> = [
    {
      title: 'N.° Orden',
      dataIndex: 'orderNumber',
      sorter: true,
    },
    {
      title: 'Cliente',
      dataIndex: 'customerId',
      filterDropdown: ({ setSelectedKeys, selectedKeys, confirm }) => (
        <div className="p-2">
          <Input
            placeholder="Buscar cliente..."
            value={selectedKeys[0]}
            onChange={e => setSelectedKeys(e.target.value ? [e.target.value] : [])}
            onPressEnter={() => confirm()}
          />
        </div>
      ),
    },
    {
      title: 'Estado',
      dataIndex: 'status',
      filters: [
        { text: 'Pendiente', value: 'pending' },
        { text: 'Enviado', value: 'shipped' },
        { text: 'Cancelado', value: 'cancelled' },
      ],
      render: (status: string) => (
        <Tag color={statusColor[status]}>{status}</Tag>
      ),
    },
    {
      title: 'Total',
      dataIndex: 'totalAmount',
      sorter: true,
      render: (amount: number) => `$${amount.toFixed(2)}`,
    },
    {
      title: 'Fecha',
      dataIndex: 'createdAt',
      sorter: true,
      render: (date: string) => new Date(date).toLocaleDateString('es-MX'),
    },
    {
      title: 'Acciones',
      render: (_, record) => (
        <Space>
          <Button type="link" onClick={() => handleView(record.id)}>Ver</Button>
          {record.status === 'pending' && (
            <Button type="link" danger onClick={() => handleCancel(record.id)}>Cancelar</Button>
          )}
        </Space>
      ),
    },
  ];

  const fetchData = async (params: TableParams) => {
    setLoading(true);
    try {
      const { data, total } = await fetchOrders(params);
      setData(data);
      setPagination(prev => ({ ...prev, total }));
    } finally {
      setLoading(false);
    }
  };

  const handleTableChange = (
    pag: TablePaginationConfig,
    filters: Record<string, FilterValue | null>,
    sorter: SorterResult<OrderRecord> | SorterResult<OrderRecord>[],
  ) => {
    fetchData({
      page: pag.current!,
      pageSize: pag.pageSize!,
      sortField: (sorter as SorterResult<OrderRecord>).field as string,
      sortOrder: (sorter as SorterResult<OrderRecord>).order,
      filters,
    });
  };

  return (
    <Table
      columns={columns}
      dataSource={data}
      rowKey="id"
      loading={loading}
      pagination={pagination}
      onChange={handleTableChange}
      scroll={{ x: 800 }}
    />
  );
}
```

---

## Form — Ant Design vs React Hook Form

### Opción 1: Ant Design Form (rápido, simple)

```tsx
import { Form, Input, InputNumber, Select, Button, message } from 'antd';

export function CreateOrderForm() {
  const [form] = Form.useForm();

  const onFinish = async (values: CreateOrderInput) => {
    try {
      await createOrder(values);
      message.success('Orden creada exitosamente');
      form.resetFields();
    } catch {
      message.error('Error al crear la orden');
    }
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={onFinish}
      initialValues={{ currency: 'MXN' }}
    >
      <Form.Item
        name="customerId"
        label="ID del Cliente"
        rules={[{ required: true, message: 'Requerido' }]}
      >
        <Input placeholder="CUST-001" />
      </Form.Item>

      <Form.Item
        name="amount"
        label="Monto"
        rules={[
          { required: true, message: 'Requerido' },
          { type: 'number', min: 0.01, message: 'Debe ser positivo' },
        ]}
      >
        <InputNumber min={0.01} style={{ width: '100%' }} />
      </Form.Item>

      <Form.Item name="currency" label="Moneda">
        <Select>
          <Select.Option value="MXN">MXN</Select.Option>
          <Select.Option value="USD">USD</Select.Option>
          <Select.Option value="EUR">EUR</Select.Option>
        </Select>
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit">Crear Orden</Button>
      </Form.Item>
    </Form>
  );
}
```

### Opción 2: React Hook Form + Ant Design (validación Zod)

```tsx
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Form, Input, InputNumber, Select, Button } from 'antd';
import { z } from 'zod';

const schema = z.object({
  customerId: z.string().min(1, 'Requerido').max(50),
  amount: z.number().positive('Debe ser positivo'),
  currency: z.enum(['MXN', 'USD', 'EUR']).default('MXN'),
});

type FormValues = z.infer<typeof schema>;

export function CreateOrderForm() {
  const { control, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { currency: 'MXN' },
  });

  const onSubmit = async (values: FormValues) => {
    await createOrder(values);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Form.Item
        label="ID del Cliente"
        validateStatus={errors.customerId ? 'error' : ''}
        help={errors.customerId?.message}
      >
        <Controller
          name="customerId"
          control={control}
          render={({ field }) => <Input {...field} />}
        />
      </Form.Item>

      <Form.Item
        label="Monto"
        validateStatus={errors.amount ? 'error' : ''}
        help={errors.amount?.message}
      >
        <Controller
          name="amount"
          control={control}
          render={({ field }) => (
            <InputNumber {...field} style={{ width: '100%' }} min={0.01} />
          )}
        />
      </Form.Item>

      <Form.Item label="Moneda">
        <Controller
          name="currency"
          control={control}
          render={({ field }) => (
            <Select {...field}>
              <Select.Option value="MXN">MXN</Select.Option>
              <Select.Option value="USD">USD</Select.Option>
              <Select.Option value="EUR">EUR</Select.Option>
            </Select>
          )}
        />
      </Form.Item>

      <Button type="primary" htmlType="submit" loading={isSubmitting}>
        Crear Orden
      </Button>
    </form>
  );
}
```

**¿Cuándo cada uno?**
- **Ant Design Form**: formularios rápidos, sin validación compleja cross-field.
- **RHF + Zod**: validación cross-field, schemas compartidos con backend, arrays dinámicos.

---

## ProComponents v3

```bash
npm install @ant-design/pro-components  # Un solo paquete, reemplaza pro-table, pro-form, etc.
```

### ProTable — Tabla con búsqueda, filtros y paginación automática

```tsx
import { ProTable } from '@ant-design/pro-components';
import type { ProColumns, ActionType } from '@ant-design/pro-components';
import { useRef } from 'react';

export function OrderProTable() {
  const actionRef = useRef<ActionType>();

  const columns: ProColumns<OrderRecord>[] = [
    {
      title: 'N.° Orden',
      dataIndex: 'orderNumber',
      key: 'orderNumber',
      valueType: 'digit',
      sorter: true,
    },
    {
      title: 'Cliente',
      dataIndex: 'customerId',
      key: 'customerId',
      fieldProps: { placeholder: 'Buscar cliente...' },
    },
    {
      title: 'Estado',
      dataIndex: 'status',
      key: 'status',
      valueType: 'select',
      valueEnum: {
        pending: { text: 'Pendiente', status: 'Processing' },
        shipped: { text: 'Enviado', status: 'Success' },
        cancelled: { text: 'Cancelado', status: 'Error' },
      },
    },
    {
      title: 'Total',
      dataIndex: 'totalAmount',
      key: 'totalAmount',
      valueType: 'money',
      sorter: true,
    },
    {
      title: 'Fecha',
      dataIndex: 'createdAt',
      key: 'createdAt',
      valueType: 'dateTime',
      sorter: true,
    },
  ];

  return (
    <ProTable<OrderRecord>
      columns={columns}
      request={async (params, sort, filter) => {
        const { data, total } = await fetchOrders({
          page: params.current!,
          pageSize: params.pageSize!,
          ...params,
          sort,
          filter,
        });
        return { data, total, success: true };
      }}
      actionRef={actionRef}
      rowKey="id"
      search={{ labelWidth: 'auto' }}
      pagination={{ pageSize: 20 }}
      dateFormatter="string"
      headerTitle="Órdenes"
      toolBarRender={() => [
        <Button key="new" type="primary" onClick={handleCreate}>
          Nueva Orden
        </Button>,
      ]}
    />
  );
}
```

### ProForm — Formularios con diseño responsive

```tsx
import { ProForm, ProFormText, ProFormSelect, ProFormDigit } from '@ant-design/pro-components';

<ProForm
  onFinish={async (values) => {
    await createOrder(values);
    return true; // No cerrar drawer/modal
  }}
>
  <ProFormText
    name="customerId"
    label="ID del Cliente"
    rules={[{ required: true }]}
    placeholder="CUST-001"
  />
  <ProFormDigit
    name="amount"
    label="Monto"
    rules={[{ required: true }]}
    min={0.01}
    fieldProps={{ precision: 2 }}
  />
  <ProFormSelect
    name="currency"
    label="Moneda"
    options={[
      { label: 'MXN', value: 'MXN' },
      { label: 'USD', value: 'USD' },
      { label: 'EUR', value: 'EUR' },
    ]}
  />
</ProForm>
```

---

## Select con búsqueda remota (API)

```tsx
import { Select } from 'antd';
import { useState } from 'react';
import { useDebounce } from 'ahooks';

export function CustomerSelect({ onChange }: { onChange: (id: string) => void }) {
  const [options, setOptions] = useState<{ label: string; value: string }[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const debouncedSearch = useDebounce(search, { wait: 300 });

  useEffect(() => {
    if (!debouncedSearch) return;
    setLoading(true);
    fetch(`/api/customers?q=${debouncedSearch}`)
      .then(r => r.json())
      .then(data => setOptions(data.map((c: any) => ({ label: c.name, value: c.id }))))
      .finally(() => setLoading(false));
  }, [debouncedSearch]);

  return (
    <Select
      showSearch
      placeholder="Buscar cliente..."
      filterOption={false}
      onSearch={setSearch}
      loading={loading}
      options={options}
      onChange={onChange}
      style={{ width: '100%' }}
    />
  );
}
```

---

## Modal y Drawer

```tsx
import { Modal, Drawer, Button } from 'antd';

// Modal para confirmaciones
function CancelOrderModal({ orderId, onClose }: Props) {
  return (
    <Modal
      title="Cancelar Orden"
      open
      onOk={async () => {
        await cancelOrder(orderId);
        message.success('Orden cancelada');
        onClose();
      }}
      onCancel={onClose}
      okText="Sí, cancelar"
      cancelText="No"
      okButtonProps={{ danger: true }}
    >
      ¿Estás seguro de cancelar la orden?
    </Modal>
  );
}

// Drawer para formularios laterales
<Drawer
  title="Crear Orden"
  open={open}
  onClose={() => setOpen(false)}
  width={600}
>
  <CreateOrderForm onSuccess={() => setOpen(false)} />
</Drawer>
```

---

## Buenas prácticas Ant Design

```tsx
// ✅ Columnas de tabla: funciones render fuera del componente o useMemo
const columns = useMemo<ColumnsType<OrderRecord>>(() => [
  {
    title: 'Estado',
    dataIndex: 'status',
    render: (_, record) => <StatusTag status={record.status} />, // Componente separado
  },
], []);

// ❌ render con hooks inline (se ejecuta en cada re-render)
{
  render: (_, record) => {
    const [open, setOpen] = useState(false); // ❌ No hacer esto
    return <Button onClick={() => setOpen(true)}>Abrir</Button>;
  },
}

// ✅ Paginación server-side: onChange dispara fetch, no Slice local
<Table
  pagination={{ current: page, pageSize, total }}
  onChange={handleTableChange} // fetchData con nuevos params
/>

// ✅ Mensajes globales con App.useApp() (Ant Design 5+)
const { message, modal, notification } = App.useApp();
message.success('Orden creada');

// ✅ ProTable request debe devolver { data, total, success }
request={async (params) => {
  const { data, total } = await fetchData(params);
  return { data, total, success: true };
}}
```

---

## Ant Design Pro v6 (scaffolding)

Ant Design Pro v6 es la plantilla completa para proyectos nuevos. Cambios clave vs v5:

| v5 | v6 |
|----|----|
| Less + CSS Modules | **Tailwind + antd-style + CSS Modules** |
| umi-request | **@tanstack/react-query** |
| Moment.js | **Day.js** |
| ESLint + Prettier | **Biome** |
| React 18 | **React 19** |

Proyectos nuevos del equipo Sputnik pueden usar Pro v6 como base. Proyectos existentes probablemente están en v5 → migrar gradualmente.

---

## Checklist Ant Design

- [ ] `ConfigProvider` con theme personalizado (colorPrimary, borderRadius)
- [ ] `@ant-design/vite-plugin` para tree shaking
- [ ] Table con paginación server-side (no Slice local)
- [ ] ProTable para tablas complejas (filtros, búsqueda, sorting)
- [ ] Select con búsqueda remota (`onSearch` + debounce + `filterOption={false}`)
- [ ] `App.useApp()` para message/notification/modal (no static methods)
- [ ] Columnas `useMemo` para evitar re-renders
- [ ] Form.Item con `rules` para validación simple; RHF + Zod para compleja
- [ ] Dark mode con `theme.darkAlgorithm` en ConfigProvider
