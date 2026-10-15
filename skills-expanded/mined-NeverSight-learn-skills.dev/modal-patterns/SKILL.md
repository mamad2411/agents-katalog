---
name: modal-patterns
description: Modal dialog patterns including confirmation, edit, selector, and wizard modals with proper focus management and accessibility
license: MIT
---

# Modal Dialog UX Patterns

Modals interrupt user flow and must be used intentionally. This skill covers proper modal implementation.

## When to Use Modals

### Use Modals For
| Use Case | Example |
|----------|---------|
| Destructive confirmations | Delete item, leave without saving |
| Quick edits | Rename, update single field |
| Selection from list | Pick item, choose option |
| Critical alerts | Session expiring, unsaved changes |
| Focused sub-tasks | Add new item inline |

### DON'T Use Modals For
| Avoid | Alternative |
|-------|-------------|
| Long forms (5+ fields) | Dedicated page |
| Complex workflows | Multi-step page |
| Informational content | Inline expansion |
| Frequent actions | Inline editing |

## Base Modal Component

### Modal Shell Structure
```tsx
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  description?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  children: ReactNode;
  footer?: ReactNode;
  closeOnOverlayClick?: boolean;
  closeOnEscape?: boolean;
}

function Modal({
  isOpen,
  onClose,
  title,
  description,
  size = 'md',
  children,
  footer,
  closeOnOverlayClick = true,
  closeOnEscape = true,
}: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);

  // Lock body scroll when open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      return () => { document.body.style.overflow = ''; };
    }
  }, [isOpen]);

  // Handle escape key
  useEffect(() => {
    if (!isOpen || !closeOnEscape) return;
    
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, closeOnEscape, onClose]);

  // Focus trap
  useEffect(() => {
    if (!isOpen) return;
    
    const focusableElements = modalRef.current?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstElement = focusableElements?.[0] as HTMLElement;
    const lastElement = focusableElements?.[focusableElements.length - 1] as HTMLElement;
    
    firstElement?.focus();

    const handleTab = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;
      
      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault();
        lastElement?.focus();
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault();
        firstElement?.focus();
      }
    };

    document.addEventListener('keydown', handleTab);
    return () => document.removeEventListener('keydown', handleTab);
  }, [isOpen]);

  if (!isOpen) return null;

  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    full: 'max-w-4xl',
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={closeOnOverlayClick ? onClose : undefined}
        aria-hidden="true"
      />

      {/* Modal */}
      <div
        ref={modalRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        aria-describedby={description ? 'modal-description' : undefined}
        className={`
          relative w-full ${sizeClasses[size]}
          bg-surface-base border border-border rounded-xl shadow-2xl
          animate-in fade-in zoom-in-95 duration-200
        `}
      >
        {/* Header */}
        <div className="flex items-start justify-between p-5 border-b border-border">
          <div>
            <h2 id="modal-title" className="text-lg font-semibold text-white">
              {title}
            </h2>
            {description && (
              <p id="modal-description" className="mt-1 text-sm text-text-secondary">
                {description}
              </p>
            )}
          </div>
          <button
            onClick={onClose}
            className="p-1.5 -mr-1.5 -mt-1.5 rounded-lg text-text-muted hover:text-white hover:bg-surface-raised"
            aria-label="Close modal"
          >
            <XIcon className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-5 max-h-[60vh] overflow-y-auto">
          {children}
        </div>

        {/* Footer */}
        {footer && (
          <div className="flex items-center justify-end gap-3 p-5 border-t border-border bg-surface-deep/50 rounded-b-xl">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
}
```

## Confirmation Modal

### Delete Confirmation Pattern
```tsx
interface DeleteConfirmModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => Promise<void>;
  itemName: string;
  itemType?: string;
  warningMessage?: string;
}

function DeleteConfirmModal({
  isOpen,
  onClose,
  onConfirm,
  itemName,
  itemType = 'item',
  warningMessage,
}: DeleteConfirmModalProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [confirmText, setConfirmText] = useState('');

  // Reset state when modal closes
  useEffect(() => {
    if (!isOpen) {
      setConfirmText('');
      setIsDeleting(false);
    }
  }, [isOpen]);

  const handleConfirm = async () => {
    setIsDeleting(true);
    try {
      await onConfirm();
      onClose();
    } catch (error) {
      // Error handling - keep modal open
      setIsDeleting(false);
    }
  };

  const requiresTypedConfirmation = warningMessage !== undefined;
  const canConfirm = !requiresTypedConfirmation || confirmText === itemName;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`Delete ${itemType}`}
      size="sm"
      closeOnOverlayClick={!isDeleting}
      closeOnEscape={!isDeleting}
      footer={
        <>
          <Button
            variant="ghost"
            onClick={onClose}
            disabled={isDeleting}
          >
            Cancel
          </Button>
          <Button
            variant="danger"
            onClick={handleConfirm}
            disabled={isDeleting || !canConfirm}
          >
            {isDeleting ? (
              <>
                <Spinner className="w-4 h-4 mr-2" />
                Deleting...
              </>
            ) : (
              'Delete'
            )}
          </Button>
        </>
      }
    >
      <div className="text-center">
        {/* Warning icon */}
        <div className="mx-auto w-12 h-12 rounded-full bg-red-500/20 flex items-center justify-center mb-4">
          <TrashIcon className="w-6 h-6 text-red-400" />
        </div>

        <p className="text-text-primary mb-2">
          Are you sure you want to delete{' '}
          <span className="font-semibold text-white">"{itemName}"</span>?
        </p>

        <p className="text-sm text-text-secondary mb-4">
          This action cannot be undone.
        </p>

        {/* Warning message with typed confirmation */}
        {warningMessage && (
          <div className="mt-4 p-3 bg-red-900/20 border border-red-600/30 rounded-lg text-left">
            <p className="text-sm text-red-400 mb-3">{warningMessage}</p>
            <label className="block">
              <span className="text-xs text-text-muted">
                Type "{itemName}" to confirm:
              </span>
              <input
                type="text"
                value={confirmText}
                onChange={(e) => setConfirmText(e.target.value)}
                className="mt-1 w-full px-3 py-2 bg-surface-deep border border-border rounded-lg text-white text-sm"
                placeholder={itemName}
                disabled={isDeleting}
              />
            </label>
          </div>
        )}
      </div>
    </Modal>
  );
}
```

## Edit Modal

### Form Edit Modal Pattern
```tsx
interface EditModalProps<T> {
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: T) => Promise<void>;
  initialData: T;
  title: string;
  children: (props: {
    data: T;
    setData: React.Dispatch<React.SetStateAction<T>>;
    errors: Record<string, string>;
  }) => ReactNode;
  validate?: (data: T) => Record<string, string>;
}

function EditModal<T extends Record<string, any>>({
  isOpen,
  onClose,
  onSave,
  initialData,
  title,
  children,
  validate,
}: EditModalProps<T>) {
  const [data, setData] = useState<T>(initialData);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSaving, setIsSaving] = useState(false);
  const [isDirty, setIsDirty] = useState(false);

  // Reset form when modal opens with new data
  useEffect(() => {
    if (isOpen) {
      setData(initialData);
      setErrors({});
      setIsDirty(false);
    }
  }, [isOpen, initialData]);

  // Track dirty state
  useEffect(() => {
    if (isOpen) {
      const hasChanges = JSON.stringify(data) !== JSON.stringify(initialData);
      setIsDirty(hasChanges);
    }
  }, [data, initialData, isOpen]);

  const handleClose = () => {
    if (isDirty && !confirm('You have unsaved changes. Discard?')) {
      return;
    }
    onClose();
  };

  const handleSave = async () => {
    // Validate
    if (validate) {
      const validationErrors = validate(data);
      if (Object.keys(validationErrors).length > 0) {
        setErrors(validationErrors);
        return;
      }
    }

    setIsSaving(true);
    try {
      await onSave(data);
      onClose();
    } catch (error) {
      setErrors({ _form: 'Failed to save. Please try again.' });
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title={title}
      size="md"
      closeOnOverlayClick={!isDirty}
      footer={
        <>
          <Button variant="ghost" onClick={handleClose} disabled={isSaving}>
            Cancel
          </Button>
          <Button
            variant="primary"
            onClick={handleSave}
            disabled={isSaving || !isDirty}
          >
            {isSaving ? 'Saving...' : 'Save Changes'}
          </Button>
        </>
      }
    >
      {errors._form && (
        <div className="mb-4 p-3 bg-red-900/20 border border-red-600/30 rounded-lg text-sm text-red-400">
          {errors._form}
        </div>
      )}
      {children({ data, setData, errors })}
    </Modal>
  );
}

// Usage example
<EditModal
  isOpen={isEditOpen}
  onClose={() => setIsEditOpen(false)}
  onSave={handleSaveIdentity}
  initialData={{ name: pilot.name, callsign: pilot.callsign }}
  title="Edit Identity"
  validate={(data) => {
    const errors: Record<string, string> = {};
    if (!data.name.trim()) errors.name = 'Name is required';
    if (!data.callsign.trim()) errors.callsign = 'Callsign is required';
    return errors;
  }}
>
  {({ data, setData, errors }) => (
    <div className="space-y-4">
      <FormField label="Name" error={errors.name}>
        <Input
          value={data.name}
          onChange={(e) => setData(d => ({ ...d, name: e.target.value }))}
        />
      </FormField>
      <FormField label="Callsign" error={errors.callsign}>
        <Input
          value={data.callsign}
          onChange={(e) => setData(d => ({ ...d, callsign: e.target.value }))}
        />
      </FormField>
    </div>
  )}
</EditModal>
```

## Selector Modal

### Item Selection Modal
```tsx
interface SelectorModalProps<T> {
  isOpen: boolean;
  onClose: () => void;
  onSelect: (item: T) => void;
  items: T[];
  selectedId?: string;
  title: string;
  searchPlaceholder?: string;
  renderItem: (item: T, isSelected: boolean) => ReactNode;
  getItemId: (item: T) => string;
  filterItem: (item: T, search: string) => boolean;
}

function SelectorModal<T>({
  isOpen,
  onClose,
  onSelect,
  items,
  selectedId,
  title,
  searchPlaceholder = 'Search...',
  renderItem,
  getItemId,
  filterItem,
}: SelectorModalProps<T>) {
  const [search, setSearch] = useState('');

  // Reset search when modal opens
  useEffect(() => {
    if (isOpen) setSearch('');
  }, [isOpen]);

  const filteredItems = useMemo(() => {
    if (!search.trim()) return items;
    return items.filter(item => filterItem(item, search.toLowerCase()));
  }, [items, search, filterItem]);

  const handleSelect = (item: T) => {
    onSelect(item);
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={title}
      size="lg"
    >
      {/* Search */}
      <div className="mb-4">
        <Input
          type="text"
          placeholder={searchPlaceholder}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          autoFocus
        />
      </div>

      {/* Results count */}
      <p className="text-xs text-text-muted mb-3">
        {filteredItems.length} of {items.length} items
      </p>

      {/* Items list */}
      <div className="max-h-80 overflow-y-auto -mx-5 px-5">
        {filteredItems.length === 0 ? (
          <p className="text-center text-text-secondary py-8">
            No items match your search
          </p>
        ) : (
          <div className="space-y-1">
            {filteredItems.map((item) => {
              const id = getItemId(item);
              const isSelected = id === selectedId;
              return (
                <button
                  key={id}
                  onClick={() => handleSelect(item)}
                  className={`
                    w-full text-left p-3 rounded-lg transition-colors
                    ${isSelected
                      ? 'bg-accent/20 border border-accent/30'
                      : 'hover:bg-surface-raised border border-transparent'
                    }
                  `}
                >
                  {renderItem(item, isSelected)}
                </button>
              );
            })}
          </div>
        )}
      </div>
    </Modal>
  );
}
```

## Wizard Modal

### Multi-Step Modal
```tsx
interface WizardStep {
  id: string;
  title: string;
  validate?: () => boolean;
}

interface WizardModalProps {
  isOpen: boolean;
  onClose: () => void;
  onComplete: () => Promise<void>;
  steps: WizardStep[];
  children: (stepId: string) => ReactNode;
  title: string;
}

function WizardModal({
  isOpen,
  onClose,
  onComplete,
  steps,
  children,
  title,
}: WizardModalProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [isCompleting, setIsCompleting] = useState(false);

  // Reset on open
  useEffect(() => {
    if (isOpen) setCurrentStep(0);
  }, [isOpen]);

  const isFirstStep = currentStep === 0;
  const isLastStep = currentStep === steps.length - 1;
  const step = steps[currentStep];

  const handleNext = () => {
    if (step.validate && !step.validate()) return;
    setCurrentStep(prev => prev + 1);
  };

  const handleBack = () => {
    setCurrentStep(prev => prev - 1);
  };

  const handleComplete = async () => {
    if (step.validate && !step.validate()) return;
    setIsCompleting(true);
    try {
      await onComplete();
      onClose();
    } finally {
      setIsCompleting(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={title}
      size="lg"
      footer={
        <>
          {!isFirstStep && (
            <Button variant="ghost" onClick={handleBack} disabled={isCompleting}>
              Back
            </Button>
          )}
          <div className="flex-1" />
          <Button variant="ghost" onClick={onClose} disabled={isCompleting}>
            Cancel
          </Button>
          {isLastStep ? (
            <Button variant="primary" onClick={handleComplete} disabled={isCompleting}>
              {isCompleting ? 'Completing...' : 'Complete'}
            </Button>
          ) : (
            <Button variant="primary" onClick={handleNext}>
              Next
            </Button>
          )}
        </>
      }
    >
      {/* Step indicator */}
      <div className="flex items-center justify-center gap-2 mb-6">
        {steps.map((s, index) => (
          <div
            key={s.id}
            className={`
              flex items-center gap-2
              ${index < currentStep ? 'text-accent' : index === currentStep ? 'text-white' : 'text-text-muted'}
            `}
          >
            <div className={`
              w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium
              ${index < currentStep ? 'bg-accent text-white' :
                index === currentStep ? 'bg-accent/20 border-2 border-accent' :
                'bg-surface-raised'}
            `}>
              {index < currentStep ? <CheckIcon className="w-4 h-4" /> : index + 1}
            </div>
            {index < steps.length - 1 && (
              <div className={`w-8 h-0.5 ${index < currentStep ? 'bg-accent' : 'bg-border'}`} />
            )}
          </div>
        ))}
      </div>

      {/* Step title */}
      <h3 className="text-lg font-medium text-white text-center mb-6">
        {step.title}
      </h3>

      {/* Step content */}
      {children(step.id)}
    </Modal>
  );
}
```

## Accessibility Requirements

### Focus Management
```tsx
// Focus first interactive element on open
useEffect(() => {
  if (isOpen) {
    const firstFocusable = modalRef.current?.querySelector(
      'button, [href], input:not([type="hidden"]), select, textarea, [tabindex]:not([tabindex="-1"])'
    ) as HTMLElement;
    firstFocusable?.focus();
  }
}, [isOpen]);

// Return focus to trigger on close
const triggerRef = useRef<HTMLElement | null>(null);

const openModal = (e: React.MouseEvent) => {
  triggerRef.current = e.currentTarget as HTMLElement;
  setIsOpen(true);
};

const closeModal = () => {
  setIsOpen(false);
  triggerRef.current?.focus();
};
```

### ARIA Attributes
```tsx
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
>
```

## Animation Patterns

### Enter/Exit Animations
```css
/* Tailwind animation utilities */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes zoomIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

.animate-in {
  animation: fadeIn 200ms ease-out, zoomIn 200ms ease-out;
}
```

## Audit Checklist for Modals

### Critical (Must Fix)
- [ ] Traps focus within modal - accessibility violation, focus escapes
- [ ] Closes on Escape key - accessibility violation
- [ ] Has proper ARIA attributes (role, aria-modal, aria-labelledby) - screen readers can't announce
- [ ] Returns focus to trigger on close - focus gets lost

### Major (Should Fix)
- [ ] Has clear title describing action - users confused about context
- [ ] Has close button (X) in header - no obvious way to dismiss
- [ ] Body scroll is locked when open - background scrolls unexpectedly
- [ ] Confirmation modals show item name - users unsure what they're deleting
- [ ] Delete modals have warning styling - destructive action not obvious
- [ ] Edit modals warn about unsaved changes - data loss risk
- [ ] Loading states disable all actions - double submissions

### Minor (Nice to Have)
- [ ] Closes on backdrop click (unless editing) - convenience
- [ ] Edit modals reset on open - stale data visible briefly
- [ ] Footer buttons are right-aligned - consistency
- [ ] Primary action matches intent (danger for delete) - visual clarity
- [ ] Footer buttons are right-aligned
- [ ] Cancel is secondary/ghost style
- [ ] Primary action matches intent (danger for delete)
