---
name: nitro-form
description: For projects using nitro-web only. Building a form, modal, or dialog in a nitro-web app. Use for Field, Select, validation errors, save handlers, or form and confirm modals.
---

# Notes

  - No form library used. Just a state plain object, where validation errors come back from the server and bind by field path.
  - Validation rules belong in the model, not in the controller or component if it can be helped, see the nitro-model skill.
  - If the form saves a list which is tracked on the store cache, invalidate it with `clearCache(setStore, 'organisationOptions')`, provided in: `/client/use-fetch.ts`

# State

  - See the nitro-page skill for the initial state object shape and the `initialX()` function that seeds the state.

# Submitting

  - See `import { request } from 'nitro-web';` which takes `(route, data, event, setIsLoading, setState)`
  - Passing `setState` is what surfaces server side field errors, so pass it even when you also catch.
  - Strip `errors` from the payload before sending.
  - Failures that are not field errors go through `showError(setStore, error)`.

  ## Example save handler, serving both create and edit:

  ```tsx
  import { request, getResponseErrors } from 'nitro-web'

  export const OrganisationPage = () => {
    const { id } = useParams()
    const location = useLocation() 
    const navigate = useNavigate()
    const [, setStore] = useTracked()

    //...

    async function onSave(e?: React.FormEvent<HTMLFormElement>) {
      try {
        if (e) e.preventDefault()
        if (isLoading || isSaving) return
        const payload = { ...state, errors: undefined }
        await request(`${!!id ? 'put' : 'post'} /api/organisations/${id || ''}`, payload, undefined, setIsSaving, setState)
        clearCache(setStore, 'organisationOptions') // only if this save changed a cached list
        setStore((prev) => ({ ...prev,  message: `${!!id ? 'Company' : 'New company'} saved successfully.` }))
        if (!!!id) setTimeout(() => navigate('/companies'), 0)
      } catch (error) {
        setState((prev) => ({ ...prev, errors: getResponseErrors(error) }))
      }
    }
  }
  ```

# Fields & Selects

  - `name` supports dot paths and should match the server field path, which is how validation errors land under the right input from state.errors.
  - Shared props like `selectCommonProps` live in `/components/partials/elements/`, spread them on every `<Select>`.
  - For custom elements, use the project's spacing tokens on labels, e.g. `mb-label-after`, rather than ad hoc margins.

  ```tsx
  import { Field, FormError, Select, onChange } from 'nitro-web'

  <label htmlFor="customer.email">Email *</label>
  <Field name="customer.email" type="email" state={state} onChange={(e) => onChange(e, setState)} />
  <Field name="message" type="textarea" rows={9} state={state} onChange={(e) => onChange(e, setState)} />
  <Select {...selectCommonProps} name="status" state={state} options={statusOptions} />
  <FormError state={state} fields={['customer.email', 'message']} /> // shows miscellaneous errors for these paths
  ```

# Custom onChange handlers

  - Custom onChange handlers are used to handle complex field logic, such as calculating the container size based on the freight type and dimensions.

  ```tsx
  function onContainerFieldChange(e: { target: { name: string; value: unknown } }) {
    onChange(e, setState, undefined, ({ state }: { state: DocumentState }) => {
      state.container = calcContainer(state.container, state.freightType, isDimensions)
      return calcLines(state, exchangeRateRef.current)
    })
  }

  <Field name="container.number" type="number" state={state} onChange={onContainerFieldChange} />
  <Select name="container.containerType" state={state} options={containerTypeOptions} onChange={onContainerFieldChange} />
  ```

# Modals

  - `FormModal` and `ConfirmModal` come from the elements barrel and already block double submission, so no `isSubmitting` guard is needed.
  - Modals stay mounted, so reset state when one opens.

  ## FormModal example:

  ```tsx
  import { useState, useEffect } from 'react'
  import { Field, FormError, Select, onChange, request, getResponseErrors } from 'nitro-web'
  import { FormModal } from '../partials/elements'
  import { userRoleOptions } from '../../client/constants'
  import type { StateErrors, Store, UserRole } from 'types'

  type InviteState = StateErrors & {
    companyId: string
    email: string
    firstName: string
    role: UserRole
  }

  const [{ user }, setStore] = useTracked()
  const [state, setState] = useState<InviteState>(() => initialState())

  useEffect(() => {
    // For invite modal, refresh each time the modal opens
    if (isOpen) setState(initialState())
  }, [isOpen])

  function initialState(): InviteState {
    return { companyId: user.company._id || '', email: '', firstName: '', role: 'manager', errors: [] }
  }

  async function onSubmit() {
    try {
      const response = await request('post /api/invite-instructions', state, undefined, undefined, setState)
      setStore((prev: Store) => ({
        ...prev,
        message: 'Invitation sent.',
        user: { ...prev.user, company: { ...prev.user.company, ...response } }, // preserve the user & user.company objects
      }))
      onClose()
    } catch (error) {
      setState((prev) => ({ ...prev, errors: getResponseErrors(error) }))
    }
  }
  return (
    <div>
      {/* content... */}

      <FormModal
        isOpen={isOpen}
        onClose={onClose}
        title="Add Team Member"
        subtitle={(
          <span>
            Invite someone to join&nbsp;
            <span className="font-medium text-black">{user.company.business.name || 'your company'}</span>
            . They will receive an email with a link to set up their account.
          </span>
        )}
        onSubmit={onSubmit}
        submitText="Send Invite"
        submitIcon={<MailIcon size={15} />}
      >
        <div>
          <div className="grid grid-cols-2 gap-x-input-after">
            <div>
              <label htmlFor="email">Email *</label>
              <Field
                name="email"
                type="email"
                state={state}
                placeholder="name@example.com"
                onChange={(e) => onChange(e, setState)}
              />
            </div>
            <div>
              <label htmlFor="firstName">First Name *</label>
              <Field
                name="firstName"
                state={state}
                placeholder="First name"
                onChange={(e) => onChange(e, setState)}
              />
            </div>
          </div>
          <div>
            <label htmlFor="role">Role *</label>
            <Select
              name="role"
              state={state}
              options={userRoleOptions}
              onChange={(e) => onChange(e, setState)}
            />
          </div>
          <FormError state={state} className="mt-2" fields={['email', 'firstName', 'role']} />
        </div>
      </FormModal>
    </div>
  )
  ```

  ## ConfirmModal example (bulk remove):

  ```tsx
  const [removeIds, setRemoveIds] = useState<string[] | null>(null)
  const { rows, total, isLoading, refetch } = useFetchCol<Document>('/quotes', search)
  
  async function onRemoveSubmit() {
    try {
      // <ConfirmModal> prevents double submissions
      const idsCached = removeIds
      await request(`delete /api/quotes/${idsCached?.join(',')}`)
      await refetch()
      setStore((prev: Store) => ({ ...prev, message: `Removed ${idsCached?.length || 0} quote(s)` }))
    } catch (error) {
      showError(setStore, error)
    } finally {
      setRemoveIds(null)
    }
  }

  return (
    <div>
      {/* content... */}

      <ConfirmModal
        isOpen={!!removeIds}
        onClose={() => setRemoveIds(null)}
        onSubmit={onRemoveSubmit}
        title={`Remove ${removeIds?.length || 0} quote${removeIds?.length === 1 ? '' : 's'}?`}
        subtitle="This action cannot be undone."
        confirmText="Remove"
      />
    </div>
  )
  ```
