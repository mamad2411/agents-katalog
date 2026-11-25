---
name: jem-ui-recipes
description: Copy-paste-ready code blocks for common pages and features built with @jem-open/jem-ui — search tables, CRUD forms, settings pages, and more.
---

# jem-ui-recipes

Copy-paste-ready code blocks for common pages and features built with `@jem-open/jem-ui`. Each recipe is a complete, working component with TypeScript types, realistic placeholder data, and inline comments marking customization points.

---

## Step 1 — Check prerequisites

Before using any recipe, verify the project is set up for `@jem-open/jem-ui`.

**Check 1: Package installed**

Look for `@jem-open/jem-ui` in `package.json` dependencies. If missing, install it with peer dependencies:

```bash
npm install @jem-open/jem-ui
```

**Check 2: Styles imported**

Confirm the global entry point (e.g. `app/layout.tsx`, `src/main.tsx`) contains:

```ts
import "@jem-open/jem-ui/styles.css"
```

If missing, add it near the top of the file alongside other CSS imports.

**Check 3: Tailwind preset configured**

Confirm `tailwind.config.ts` (or `.js`) includes the jem-ui preset and content path:

```ts
import { jemUIPreset } from "@jem-open/jem-ui/tailwind"

export default {
  presets: [jemUIPreset],
  content: [
    "./node_modules/@jem-open/jem-ui/dist/**/*.{js,mjs}",
    // ...your app paths
  ],
}
```

**Halt** if any check fails — recipes will not render correctly without all three in place.

---

## Step 2 — Select a recipe

Choose the recipe that best matches your use case:

| Recipe | Description | Key components |
|---|---|---|
| Search + filter + data table | Searchable, filterable table with pagination | DataTable, DataTableColumnHeader, SearchInput, Select, Tag, EmptyState |
| CRUD form in a dialog | Create/edit modal with validation | Dialog, InputField, Select, Checkbox, Button |
| Settings page with sections | Tabbed settings with grouped form fields | Tabs, InputField, Switch, Select, Button, Divider |
| Detail drawer | Side panel showing record details | Drawer, Avatar, Tag, Button, Divider, Tooltip |
| Multi-step wizard | Step-by-step flow with progress | Dialog, Progress, Button, form components |
| Empty state with CTA | Placeholder for empty pages/sections | EmptyState, Button |
| Confirmation dialog | Destructive action confirmation | Dialog, Button, Alert |
| File upload form | Upload with progress and validation | Upload, Button, Progress, Alert |

---

## Step 3 — Apply the recipe

Copy the recipe that matches your selection. Each recipe is a complete, working TypeScript/React component with all imports, types, state hooks, and `// TODO:` comments marking customization points.

### Recipe 1: Search + filter + data table

```tsx
"use client"

import { useState } from "react"
import {
  DataTable, DataTableColumnHeader, Tag, EmptyState
} from "@jem-open/jem-ui"
import { ColumnDef } from "@tanstack/react-table"

// TODO: Replace with your data type
type Employee = {
  id: string
  name: string
  email: string
  department: string
  status: "active" | "inactive" | "pending"
}

// TODO: Replace with your column definitions
const columns: ColumnDef<Employee>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Name" />,
  },
  {
    accessorKey: "email",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Email" />,
  },
  {
    accessorKey: "department",
    header: ({ column }) => <DataTableColumnHeader column={column} title="Department" />,
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue("status") as string
      const variant = status === "active" ? "success" : status === "pending" ? "pending" : "failed"
      return <Tag variant={variant}>{status}</Tag>
    },
  },
]

// TODO: Replace with your data fetching
const sampleData: Employee[] = [
  { id: "1", name: "Alice Johnson", email: "alice@example.com", department: "Engineering", status: "active" },
  { id: "2", name: "Bob Smith", email: "bob@example.com", department: "Design", status: "active" },
  { id: "3", name: "Carol Williams", email: "carol@example.com", department: "Marketing", status: "pending" },
]

export function EmployeeTable() {
  // TODO: Replace with your data source
  const data = sampleData

  if (data.length === 0) {
    return (
      <EmptyState
        icon="users"
        title="No employees found"
        description="Add employees to see them listed here"
        primaryAction={{ label: "Add employee", onClick: () => {} }}
        variant="card"
      />
    )
  }

  return (
    <DataTable
      columns={columns}
      data={data}
      filterColumn="name"
      filterPlaceholder="Search by name..."
    />
  )
}
```

### Recipe 2: CRUD form in a dialog

```tsx
"use client"

import { useState } from "react"
import {
  Dialog, DialogTrigger, DialogContent, DialogHeader,
  DialogTitle, DialogDescription, DialogFooter, DialogClose
} from "@jem-open/jem-ui"
import {
  Button, InputField, Select, SelectTrigger, SelectContent,
  SelectItem, SelectValue, SelectField, CheckboxWithLabel
} from "@jem-open/jem-ui"

// TODO: Replace with your form data type
type UserFormData = {
  name: string
  email: string
  role: string
  sendInvite: boolean
}

export function CreateUserDialog() {
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [form, setForm] = useState<UserFormData>({
    name: "",
    email: "",
    role: "",
    sendInvite: true,
  })

  function validate(): boolean {
    const newErrors: Record<string, string> = {}
    if (!form.name) newErrors.name = "Name is required"
    if (!form.email) newErrors.email = "Email is required"
    if (!form.role) newErrors.role = "Role is required"
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  async function handleSubmit() {
    if (!validate()) return
    setLoading(true)
    try {
      // TODO: Replace with your API call
      await new Promise((resolve) => setTimeout(resolve, 1000))
      setOpen(false)
      setForm({ name: "", email: "", role: "", sendInvite: true })
      setErrors({})
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="primary">Add user</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create new user</DialogTitle>
          <DialogDescription>Add a new user to your organization.</DialogDescription>
        </DialogHeader>
        <div className="flex flex-col gap-md py-md">
          <InputField
            label="Full name"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            error={!!errors.name}
            helperText={errors.name}
          />
          <InputField
            label="Email"
            type="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            error={!!errors.email}
            helperText={errors.email}
          />
          <SelectField label="Role">
            <Select value={form.role} onValueChange={(value) => setForm({ ...form, role: value })}>
              <SelectTrigger>
                <SelectValue placeholder="Select a role" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="admin">Admin</SelectItem>
                <SelectItem value="editor">Editor</SelectItem>
                <SelectItem value="viewer">Viewer</SelectItem>
              </SelectContent>
            </Select>
          </SelectField>
          <CheckboxWithLabel
            label="Send invite email"
            description="User will receive an email to set up their account"
            checked={form.sendInvite}
            onCheckedChange={(checked) => setForm({ ...form, sendInvite: checked as boolean })}
          />
        </div>
        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline">Cancel</Button>
          </DialogClose>
          <Button variant="primary" loading={loading} onClick={handleSubmit}>
            Create user
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

### Recipe 3: Settings page with sections

```tsx
"use client"

import { useState } from "react"
import {
  Tabs, TabsList, TabsTrigger, TabsContent
} from "@jem-open/jem-ui"
import {
  Button, InputField, SwitchWithLabel, Select, SelectTrigger,
  SelectContent, SelectItem, SelectValue, SelectField, Divider
} from "@jem-open/jem-ui"
import { toast } from "sonner"

export function SettingsPage() {
  // TODO: Replace with your settings state
  const [name, setName] = useState("Jane Doe")
  const [email, setEmail] = useState("jane@example.com")
  const [emailNotifs, setEmailNotifs] = useState(true)
  const [pushNotifs, setPushNotifs] = useState(false)
  const [language, setLanguage] = useState("en")

  function handleSave() {
    // TODO: Replace with your save logic
    toast.success("Settings saved")
  }

  return (
    <div className="flex flex-col gap-md max-w-2xl">
      <h1 className="text-2xl font-semibold text-greyscale-text-title">Settings</h1>

      <Tabs defaultValue="profile">
        <TabsList variant="line">
          <TabsTrigger variant="line" value="profile">Profile</TabsTrigger>
          <TabsTrigger variant="line" value="notifications">Notifications</TabsTrigger>
          <TabsTrigger variant="line" value="preferences">Preferences</TabsTrigger>
        </TabsList>

        <TabsContent value="profile">
          <div className="flex flex-col gap-md py-md">
            <InputField label="Display name" value={name} onChange={(e) => setName(e.target.value)} />
            <InputField label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <Divider spacing="md" />
            <div className="flex justify-end">
              <Button variant="primary" onClick={handleSave}>Save profile</Button>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="notifications">
          <div className="flex flex-col gap-md py-md">
            <SwitchWithLabel
              label="Email notifications"
              description="Receive updates about your account via email"
              checked={emailNotifs}
              onCheckedChange={setEmailNotifs}
            />
            <SwitchWithLabel
              label="Push notifications"
              description="Receive push notifications in your browser"
              checked={pushNotifs}
              onCheckedChange={setPushNotifs}
            />
            <Divider spacing="md" />
            <div className="flex justify-end">
              <Button variant="primary" onClick={handleSave}>Save notifications</Button>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="preferences">
          <div className="flex flex-col gap-md py-md">
            <SelectField label="Language">
              <Select value={language} onValueChange={setLanguage}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="en">English</SelectItem>
                  <SelectItem value="es">Spanish</SelectItem>
                  <SelectItem value="fr">French</SelectItem>
                </SelectContent>
              </Select>
            </SelectField>
            <Divider spacing="md" />
            <div className="flex justify-end">
              <Button variant="primary" onClick={handleSave}>Save preferences</Button>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
```

### Recipe 4: Detail drawer

```tsx
"use client"

import {
  Drawer, DrawerTrigger, DrawerContent, DrawerHeader,
  DrawerBody, DrawerFooter, DrawerTitle, DrawerClose
} from "@jem-open/jem-ui"
import {
  Button, Avatar, AvatarImage, AvatarFallback, Tag, Divider,
  Tooltip, TooltipTrigger, TooltipContent
} from "@jem-open/jem-ui"
import { Mail, Phone } from "lucide-react"

// TODO: Replace with your data type
type Contact = {
  name: string
  initials: string
  email: string
  phone: string
  role: string
  status: "active" | "inactive"
  avatarUrl?: string
}

export function ContactDetailDrawer({ contact }: { contact: Contact }) {
  return (
    <Drawer direction="right">
      <DrawerTrigger asChild>
        <Button variant="ghost" size="sm">View</Button>
      </DrawerTrigger>
      <DrawerContent>
        <DrawerHeader>
          <DrawerTitle>Contact Details</DrawerTitle>
        </DrawerHeader>
        <DrawerBody>
          <div className="flex items-center gap-md mb-md">
            <Avatar size="lg">
              {contact.avatarUrl && <AvatarImage src={contact.avatarUrl} alt={contact.name} />}
              <AvatarFallback size="lg">{contact.initials}</AvatarFallback>
            </Avatar>
            <div>
              <p className="text-lg font-semibold text-greyscale-text-title">{contact.name}</p>
              <Tag variant={contact.status === "active" ? "success" : "failed"}>
                {contact.status}
              </Tag>
            </div>
          </div>

          <Divider spacing="md" />

          <div className="flex flex-col gap-sm">
            <div className="flex justify-between items-center">
              <span className="text-greyscale-text-subtitle">Role</span>
              <span className="text-greyscale-text-body">{contact.role}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-greyscale-text-subtitle">Email</span>
              <Tooltip>
                <TooltipTrigger asChild>
                  <a href={`mailto:${contact.email}`} className="text-secondary-text-label flex items-center gap-xxs">
                    <Mail className="size-4" /> {contact.email}
                  </a>
                </TooltipTrigger>
                <TooltipContent>Send email</TooltipContent>
              </Tooltip>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-greyscale-text-subtitle">Phone</span>
              <span className="flex items-center gap-xxs text-greyscale-text-body">
                <Phone className="size-4" /> {contact.phone}
              </span>
            </div>
          </div>
        </DrawerBody>
        <DrawerFooter>
          <Button variant="primary">Edit contact</Button>
          <DrawerClose asChild>
            <Button variant="outline">Close</Button>
          </DrawerClose>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  )
}
```

### Recipe 5: Multi-step wizard

```tsx
"use client"

import { useState } from "react"
import {
  Dialog, DialogTrigger, DialogContent, DialogHeader,
  DialogTitle, DialogDescription, DialogFooter, DialogClose
} from "@jem-open/jem-ui"
import { Button, InputField, Progress } from "@jem-open/jem-ui"
import {
  Select, SelectTrigger, SelectContent, SelectItem, SelectValue, SelectField,
  CheckboxWithLabel
} from "@jem-open/jem-ui"

const TOTAL_STEPS = 3

export function OnboardingWizard() {
  const [open, setOpen] = useState(false)
  const [step, setStep] = useState(1)
  const [loading, setLoading] = useState(false)

  // TODO: Replace with your form state
  const [form, setForm] = useState({
    companyName: "",
    industry: "",
    teamSize: "",
    inviteEmails: "",
    agreeToTerms: false,
  })

  function handleNext() {
    // TODO: Add step validation
    if (step < TOTAL_STEPS) setStep(step + 1)
  }

  function handleBack() {
    if (step > 1) setStep(step - 1)
  }

  async function handleSubmit() {
    setLoading(true)
    try {
      // TODO: Replace with your API call
      await new Promise((resolve) => setTimeout(resolve, 1000))
      setOpen(false)
      setStep(1)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={(isOpen) => { setOpen(isOpen); if (!isOpen) setStep(1) }}>
      <DialogTrigger asChild>
        <Button variant="primary">Get started</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <div className="mb-sm">
            <Progress value={(step / TOTAL_STEPS) * 100} />
          </div>
          <DialogTitle>
            {step === 1 && "Company details"}
            {step === 2 && "Invite your team"}
            {step === 3 && "Review & confirm"}
          </DialogTitle>
          <DialogDescription>Step {step} of {TOTAL_STEPS}</DialogDescription>
        </DialogHeader>

        <div className="flex flex-col gap-md py-md">
          {step === 1 && (
            <>
              <InputField
                label="Company name"
                value={form.companyName}
                onChange={(e) => setForm({ ...form, companyName: e.target.value })}
              />
              <SelectField label="Industry">
                <Select value={form.industry} onValueChange={(v) => setForm({ ...form, industry: v })}>
                  <SelectTrigger><SelectValue placeholder="Select industry" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="tech">Technology</SelectItem>
                    <SelectItem value="finance">Finance</SelectItem>
                    <SelectItem value="healthcare">Healthcare</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </SelectField>
            </>
          )}

          {step === 2 && (
            <>
              <SelectField label="Team size">
                <Select value={form.teamSize} onValueChange={(v) => setForm({ ...form, teamSize: v })}>
                  <SelectTrigger><SelectValue placeholder="Select size" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1-10">1-10</SelectItem>
                    <SelectItem value="11-50">11-50</SelectItem>
                    <SelectItem value="51-200">51-200</SelectItem>
                    <SelectItem value="200+">200+</SelectItem>
                  </SelectContent>
                </Select>
              </SelectField>
              <InputField
                label="Invite by email"
                description="Comma-separated email addresses"
                value={form.inviteEmails}
                onChange={(e) => setForm({ ...form, inviteEmails: e.target.value })}
                placeholder="alice@co.com, bob@co.com"
              />
            </>
          )}

          {step === 3 && (
            <>
              <div className="flex flex-col gap-xs text-sm">
                <div className="flex justify-between">
                  <span className="text-greyscale-text-subtitle">Company</span>
                  <span className="text-greyscale-text-body">{form.companyName || "—"}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-greyscale-text-subtitle">Industry</span>
                  <span className="text-greyscale-text-body">{form.industry || "—"}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-greyscale-text-subtitle">Team size</span>
                  <span className="text-greyscale-text-body">{form.teamSize || "—"}</span>
                </div>
              </div>
              <CheckboxWithLabel
                label="I agree to the terms of service"
                checked={form.agreeToTerms}
                onCheckedChange={(checked) => setForm({ ...form, agreeToTerms: checked as boolean })}
              />
            </>
          )}
        </div>

        <DialogFooter>
          {step > 1 && (
            <Button variant="outline" onClick={handleBack}>Back</Button>
          )}
          {step < TOTAL_STEPS ? (
            <Button variant="primary" onClick={handleNext}>Next</Button>
          ) : (
            <Button variant="primary" loading={loading} onClick={handleSubmit}>
              Complete setup
            </Button>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

### Recipe 6: Empty state with CTA

```tsx
"use client"

import { EmptyState } from "@jem-open/jem-ui"

// TODO: Replace icon, title, description, and actions to match your empty state
// Default variant
export function NoProjectsState({ onCreate }: { onCreate: () => void }) {
  return (
    <EmptyState
      icon="folder"
      title="No projects yet"
      description="Create your first project to get started"
      primaryAction={{ label: "Create project", onClick: onCreate }}
      secondaryAction={{ label: "Learn more", href: "/docs" }}
    />
  )
}

// Card variant — use inside a section or panel
export function NoSearchResults({ onClearFilters }: { onClearFilters: () => void }) {
  return (
    <EmptyState
      icon="search"
      title="No results found"
      description="Try adjusting your search terms or filters"
      primaryAction={{ label: "Clear filters", onClick: onClearFilters }}
      variant="card"
      size="sm"
    />
  )
}
```

### Recipe 7: Confirmation dialog

```tsx
"use client"

import { useState } from "react"
import {
  Dialog, DialogTrigger, DialogContent, DialogHeader,
  DialogTitle, DialogDescription, DialogFooter, DialogClose
} from "@jem-open/jem-ui"
import { Button, Alert, AlertDescription } from "@jem-open/jem-ui"

export function DeleteConfirmDialog({ onDelete }: { onDelete: () => Promise<void> }) {
  const [open, setOpen] = useState(false)
  const [loading, setLoading] = useState(false)

  async function handleDelete() {
    setLoading(true)
    try {
      // TODO: Replace with your delete logic
      await onDelete()
      setOpen(false)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="destructive">Delete</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle variant="error">Delete item</DialogTitle>
          <DialogDescription>This action cannot be undone.</DialogDescription>
        </DialogHeader>
        <Alert variant="destructive">
          <AlertDescription>
            All associated data will be permanently removed from your account.
          </AlertDescription>
        </Alert>
        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline">Cancel</Button>
          </DialogClose>
          <Button variant="destructive" loading={loading} onClick={handleDelete}>
            Delete permanently
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

### Recipe 8: File upload form

```tsx
"use client"

import { useState } from "react"
import { Upload, Button, Progress, Alert, AlertDescription } from "@jem-open/jem-ui"

type UploadState = "default" | "uploading" | "uploaded"

export function FileUploadForm() {
  const [state, setState] = useState<UploadState>("default")
  const [progress, setProgress] = useState(0)
  const [fileName, setFileName] = useState("")
  const [error, setError] = useState("")

  function handleSelectFile() {
    // TODO: Replace with your file selection logic
    const input = document.createElement("input")
    input.type = "file"
    input.accept = ".pdf,.doc,.docx"
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0]
      if (!file) return

      // TODO: Replace with your validation
      if (file.size > 10 * 1024 * 1024) {
        setError("File must be under 10MB")
        return
      }

      setError("")
      setFileName(file.name)
      simulateUpload()
    }
    input.click()
  }

  function simulateUpload() {
    setState("uploading")
    setProgress(0)
    // TODO: Replace with your actual upload logic
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setState("uploaded")
          return 100
        }
        return prev + 10
      })
    }, 200)
  }

  function handleRemove() {
    setState("default")
    setProgress(0)
    setFileName("")
    setError("")
  }

  function handleSubmit() {
    // TODO: Replace with your submit logic
    console.log("Submitting file:", fileName)
  }

  return (
    <div className="flex flex-col gap-md max-w-md">
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
      <Upload
        state={state}
        progress={progress}
        fileName={fileName}
        title="Upload document"
        description="PDF, DOC, or DOCX files"
        maxSize="10MB"
        onSelectFile={handleSelectFile}
        onRemoveFile={handleRemove}
        onSubmit={handleSubmit}
      />
    </div>
  )
}
```

---

## Step 4 — Customize the recipe

After pasting a recipe, adapt it to your application:

**Data & types:**

- Replace the `// TODO:` type definition with your actual data type
- Replace sample data arrays with your data source (API calls, database queries, props)
- Update `ColumnDef` definitions to match your data fields

**Form fields:**

- Add or remove form fields to match your data model
- Update validation logic in `validate()` functions
- Wire `onSubmit` to your API endpoint

**Layout:**

- Adjust `max-w-*` classes for your page width
- Change spacing tokens (`gap-md`, `py-md`) if needed
- Add `Breadcrumb` above the component for navigation context

**State management:**

- Replace `useState` with your state management (React Hook Form, Zustand, etc.)
- Connect controlled dialogs/drawers to your routing if needed
- Replace `toast.success()` messages with your copy

---

## Step 5 — Verify the result

Run through this checklist before considering the recipe complete:

- [ ] Every interactive component has an accessible label (InputField label, Button text, IconButton aria-label)
- [ ] Spacing between elements uses design tokens (`gap-md`, `p-sm`), not arbitrary values (`gap-6`, `p-4`)
- [ ] Loading states are handled (Button `loading` prop during async operations)
- [ ] Empty states are handled (EmptyState when no data, not a blank page)
- [ ] Error states are handled (InputField `error` + `helperText`, Alert for form-level errors, toast.error for async failures)
- [ ] Class composition uses `cn()` from `@jem-open/jem-ui` if custom classes were added
- [ ] No unnecessary wrapper elements (use `asChild` on triggers instead)
- [ ] `TooltipProvider` is present in the layout (if using Tooltip)
- [ ] `Toaster` is added once in the root layout (if using toast)
- [ ] All `// TODO:` comments have been addressed or intentionally left for future work
