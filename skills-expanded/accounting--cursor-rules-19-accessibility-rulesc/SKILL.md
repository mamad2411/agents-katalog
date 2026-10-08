---
globs:
  - "src/presentation/**/*"
  - "**/*.tsx"
alwaysApply: false
---

# Accessibility (A11y) Rules

## Why Accessibility Matters
- Legal compliance (ADA, WCAG)
- Larger user base (15%+ have disabilities)
- Better UX for everyone
- Improved SEO and discoverability

## Core Accessibility Requirements

### 1. Screen Reader Support

#### AccessibilityLabel
```typescript
// ✅ GOOD: Descriptive label for screen readers
<TouchableOpacity
  accessibilityLabel="View details for Bessie the cow, 450 kg"
  accessibilityRole="button"
  onPress={() => navigateToAnimal(animal)}
>
  <Text>{animal.name}</Text>
  <Text>{animal.weight} kg</Text>
</TouchableOpacity>

// ❌ BAD: No accessibility information
<TouchableOpacity onPress={() => navigateToAnimal(animal)}>
  <Text>{animal.name}</Text>
</TouchableOpacity>
```

#### AccessibilityHint
```typescript
// Provide hints for complex interactions
<TouchableOpacity
  accessibilityLabel="Delete Bessie"
  accessibilityHint="Double tap to permanently delete this animal"
  accessibilityRole="button"
  onPress={handleDelete}
>
  <TrashIcon />
</TouchableOpacity>
```

#### AccessibilityRole
```typescript
// Use semantic roles
<View accessibilityRole="header">
  <Text>Animal List</Text>
</View>

<TextInput
  accessibilityRole="search"
  accessibilityLabel="Search animals"
  placeholder="Search..."
/>

<Switch
  accessibilityRole="switch"
  accessibilityLabel="Enable notifications"
  accessibilityState={{ checked: isEnabled }}
/>

// Common roles: button, link, header, search, image, text, 
// checkbox, radio, switch, slider, progressbar, menu, menuitem
```

### 2. Touch Targets

#### Minimum Size (44x44 points)
```typescript
// ✅ GOOD: Adequate touch target
<TouchableOpacity
  style={{
    minHeight: 44,
    minWidth: 44,
    padding: 12,
  }}
  onPress={onPress}
>
  <Icon name="settings" size={20} />
</TouchableOpacity>

// ❌ BAD: Touch target too small
<TouchableOpacity style={{ padding: 4 }}>
  <Icon name="settings" size={16} />
</TouchableOpacity>
```

#### Spacing Between Targets
```typescript
// Ensure adequate spacing between interactive elements
const styles = StyleSheet.create({
  buttonContainer: {
    flexDirection: 'row',
    gap: 12, // Minimum 8pt between touch targets
  },
  button: {
    minHeight: 44,
    minWidth: 44,
    padding: 12,
  },
});
```

### 3. Color & Contrast

#### Minimum Contrast Ratios
- **Normal text**: 4.5:1 ratio
- **Large text (18pt+)**: 3:1 ratio
- **UI components**: 3:1 ratio

```typescript
// src/shared/constants/accessible-colors.ts
export const COLORS = {
  // High contrast text colors
  textPrimary: '#1A1A1A',      // On white: 16:1
  textSecondary: '#5C5C5C',    // On white: 5.9:1
  
  // Background colors
  background: '#FFFFFF',
  surface: '#F5F5F5',
  
  // Interactive elements
  primary: '#0066CC',          // On white: 4.5:1 ✓
  primaryDark: '#004499',      // On white: 8.6:1 ✓
  
  // Status colors (with accessible alternatives)
  error: '#CC0000',            // On white: 5.9:1 ✓
  success: '#006600',          // On white: 7.3:1 ✓
  warning: '#856404',          // On #FFF3CD: 4.5:1 ✓
} as const;
```

#### Don't Rely on Color Alone
```typescript
// ✅ GOOD: Color + icon + text
<View style={styles.errorContainer}>
  <ErrorIcon color={COLORS.error} />
  <Text style={styles.errorText}>Error: Weight is required</Text>
</View>

// ❌ BAD: Color only
<Text style={{ color: 'red' }}>Weight is required</Text>
```

### 4. Text & Typography

#### Scalable Text
```typescript
// ✅ GOOD: Allow system font scaling
<Text 
  style={{ fontSize: 16 }}
  allowFontScaling={true}
  maxFontSizeMultiplier={1.5}
>
  Animal Name
</Text>

// Handle large text gracefully
const styles = StyleSheet.create({
  card: {
    padding: 16,
    // Don't use fixed heights that clip scaled text
    minHeight: 80,
  },
  text: {
    fontSize: 16,
    lineHeight: 24, // 1.5x font size for readability
  },
});
```

#### Readable Font Sizes
```typescript
// Minimum font sizes
export const FONT_SIZES = {
  caption: 12,    // Minimum for legibility
  body: 16,       // Default body text
  subtitle: 18,
  title: 20,
  headline: 24,
} as const;
```

### 5. Focus & Navigation

#### Focus Order
```typescript
// Logical focus order with accessibilityViewIsModal
<Modal visible={isVisible}>
  <View accessibilityViewIsModal={true}>
    <Text accessibilityRole="header">Edit Animal</Text>
    <TextInput
      ref={nameInputRef}
      accessibilityLabel="Animal name"
    />
    <Button title="Save" />
    <Button title="Cancel" onPress={closeModal} />
  </View>
</Modal>

// Auto-focus first input when modal opens
useEffect(() => {
  if (isVisible) {
    nameInputRef.current?.focus();
  }
}, [isVisible]);
```

#### Skip Links / Group Navigation
```typescript
// Group related content for easier navigation
<View accessible={true} accessibilityLabel="Animal statistics section">
  <Text>Weight: 450 kg</Text>
  <Text>Last weighed: 2 days ago</Text>
  <Text>Average gain: 1.2 kg/day</Text>
</View>
```

### 6. Forms & Inputs

#### Accessible Form Fields
```typescript
// Complete accessible input
<View>
  <Text 
    nativeID="weight-label"
    accessibilityRole="text"
  >
    Weight (kg)
  </Text>
  <TextInput
    accessibilityLabel="Weight in kilograms"
    accessibilityLabelledBy="weight-label"
    accessibilityHint="Enter the animal's weight"
    keyboardType="decimal-pad"
    returnKeyType="done"
    value={weight}
    onChangeText={setWeight}
  />
  {error && (
    <Text 
      accessibilityRole="alert"
      accessibilityLiveRegion="polite"
    >
      {error}
    </Text>
  )}
</View>
```

#### Error Announcements
```typescript
// Announce errors to screen readers
<Text
  accessibilityRole="alert"
  accessibilityLiveRegion="assertive"
>
  Please enter a valid weight
</Text>
```

### 7. Images & Icons

#### Image Accessibility
```typescript
// Informative images
<Image
  source={animalPhoto}
  accessibilityLabel="Photo of Bessie, a brown Holstein cow"
  accessibilityRole="image"
/>

// Decorative images (hide from screen readers)
<Image
  source={decorativeBorder}
  accessibilityElementsHidden={true}
  importantForAccessibility="no"
/>

// Icon buttons
<TouchableOpacity
  accessibilityLabel="Edit animal"
  accessibilityRole="button"
>
  <EditIcon accessibilityElementsHidden={true} />
</TouchableOpacity>
```

### 8. Loading & State Changes

#### Announce State Changes
```typescript
// Loading state
<View
  accessibilityRole="progressbar"
  accessibilityLabel="Loading animals"
  accessibilityValue={{ now: 50, min: 0, max: 100 }}
>
  <ActivityIndicator />
</View>

// Success feedback
<Text accessibilityLiveRegion="polite">
  Animal saved successfully
</Text>
```

## Accessibility Testing

### Manual Testing Checklist
- [ ] Navigate entire app with TalkBack (Android) / VoiceOver (iOS)
- [ ] All interactive elements have labels
- [ ] Focus order is logical
- [ ] Touch targets are 44x44 minimum
- [ ] Text scales properly with system settings
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] App works in both orientations
- [ ] Forms have proper labels and error messages

### Automated Testing
```typescript
// Add accessibility tests
describe('AnimalCard Accessibility', () => {
  it('should have accessible label', () => {
    const { getByRole } = render(<AnimalCard animal={testAnimal} />);
    
    const button = getByRole('button');
    expect(button.props.accessibilityLabel).toContain(testAnimal.name);
  });

  it('should have minimum touch target size', () => {
    const { getByTestId } = render(<AnimalCard animal={testAnimal} />);
    
    const card = getByTestId('animal-card');
    const { height, width } = card.props.style;
    
    expect(height).toBeGreaterThanOrEqual(44);
    expect(width).toBeGreaterThanOrEqual(44);
  });
});
```

## Accessibility Components

### Reusable Accessible Button
```typescript
// src/presentation/components/accessible-button.tsx
interface AccessibleButtonProps {
  onPress: () => void;
  label: string;
  hint?: string;
  icon?: React.ReactNode;
  children?: React.ReactNode;
  disabled?: boolean;
}

export const AccessibleButton: React.FC<AccessibleButtonProps> = ({
  onPress,
  label,
  hint,
  icon,
  children,
  disabled = false,
}) => {
  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={disabled}
      accessibilityLabel={label}
      accessibilityHint={hint}
      accessibilityRole="button"
      accessibilityState={{ disabled }}
      style={[styles.button, disabled && styles.disabled]}
    >
      {icon && (
        <View accessibilityElementsHidden={true}>
          {icon}
        </View>
      )}
      {children}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    minHeight: 44,
    minWidth: 44,
    paddingHorizontal: 16,
    paddingVertical: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  disabled: {
    opacity: 0.5,
  },
});
```
