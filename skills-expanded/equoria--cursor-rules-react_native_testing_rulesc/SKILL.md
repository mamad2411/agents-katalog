---
description: 
globs: 
alwaysApply: false
---
# React Native Testing Best Practices

You are a React Native Testing Expert specializing in Test-Driven Development with React Native Testing Library, Jest, and Expo for the Equoria horse breeding game.

## Core Testing Philosophy

### 1. Test-Driven Mobile Development
- **Mobile-First TDD**: Write tests that simulate real user interactions on mobile devices
- **Component Behavior**: Test what users see and do, not implementation details
- **Accessibility Testing**: Ensure screen reader compatibility and WCAG compliance
- **Cross-Platform**: Tests should work on both iOS and Android
- **Performance Testing**: Test component rendering performance and memory usage

### 2. React Native Testing Library Approach
```javascript
// ALWAYS test user behavior, not implementation:
import { render, screen, fireEvent, waitFor } from '@testing-library/react-native';
import { TraitDisplay } from '../TraitDisplay';

// Good: Test user interactions
it('should display trait when user taps on hidden trait', async () => {
  const mockTraits = { speed: { value: 85, hidden: true } };
  
  render(<TraitDisplay traits={mockTraits} showHidden={false} />);
  
  const hiddenTraitButton = screen.getByRole('button', { name: /reveal traits/i });
  fireEvent.press(hiddenTraitButton);
  
  await waitFor(() => {
    expect(screen.getByText('Speed: 85')).toBeVisible();
  });
});

// Bad: Test implementation details
it('should call setState when button pressed', () => {
  // DON'T test internal state changes
});
```

## React Native Testing Patterns

### 1. Component Testing Structure
```javascript
// ALWAYS structure React Native tests like this:
describe('TraitDisplay Component', () => {
  // Test data setup
  const mockTraits = {
    speed: { value: 85, hidden: false },
    stamina: { value: 72, hidden: true },
    intelligence: { value: 91, hidden: false }
  };

  beforeEach(() => {
    // Reset any global state or mocks
    jest.clearAllMocks();
  });

  describe('trait visibility', () => {
    it('should show visible traits by default', () => {
      render(<TraitDisplay traits={mockTraits} />);
      
      expect(screen.getByText('Speed: 85')).toBeVisible();
      expect(screen.getByText('Intelligence: 91')).toBeVisible();
      expect(screen.queryByText('Stamina: 72')).toBeNull();
    });

    it('should reveal hidden traits when showHidden is true', () => {
      render(<TraitDisplay traits={mockTraits} showHidden={true} />);
      
      expect(screen.getByText('Stamina: 72')).toBeVisible();
    });
  });

  describe('user interactions', () => {
    it('should call onTraitClick when trait is pressed', () => {
      const mockOnTraitClick = jest.fn();
      
      render(
        <TraitDisplay 
          traits={mockTraits} 
          onTraitClick={mockOnTraitClick} 
        />
      );
      
      const speedTrait = screen.getByText('Speed: 85');
      fireEvent.press(speedTrait);
      
      expect(mockOnTraitClick).toHaveBeenCalledWith('speed');
    });
  });

  describe('accessibility', () => {
    it('should provide proper accessibility labels', () => {
      render(<TraitDisplay traits={mockTraits} />);
      
      const speedTrait = screen.getByRole('button', { 
        name: /speed trait.*85/i 
      });
      expect(speedTrait).toHaveAccessibilityRole('button');
    });

    it('should support screen reader navigation', () => {
      render(<TraitDisplay traits={mockTraits} />);
      
      const traits = screen.getAllByRole('button');
      traits.forEach(trait => {
        expect(trait).toBeAccessible();
      });
    });
  });
});
```

### 2. Screen Testing Patterns
```javascript
// ALWAYS test screens as complete user flows:
describe('HorseDetailsScreen', () => {
  const mockHorse = {
    id: '123',
    name: 'Thunder',
    age: 4,
    disciplines: { dressage: 65, showjumping: 78 },
    traits: { speed: { value: 85, hidden: false } }
  };

  beforeEach(() => {
    // Mock navigation
    jest.mock('@react-navigation/native', () => ({
      useNavigation: () => ({
        navigate: jest.fn(),
        goBack: jest.fn()
      }),
      useRoute: () => ({
        params: { horseId: '123' }
      })
    }));
  });

  it('should display horse information correctly', async () => {
    // Mock API call
    jest.spyOn(api, 'getHorse').mockResolvedValue(mockHorse);
    
    render(<HorseDetailsScreen />);
    
    await waitFor(() => {
      expect(screen.getByText('Thunder')).toBeVisible();
      expect(screen.getByText('Age: 4 years')).toBeVisible();
    });
  });

  it('should navigate to training screen when train button pressed', async () => {
    const mockNavigate = jest.fn();
    jest.spyOn(require('@react-navigation/native'), 'useNavigation')
      .mockReturnValue({ navigate: mockNavigate });
    
    render(<HorseDetailsScreen />);
    
    await waitFor(() => {
      const trainButton = screen.getByRole('button', { name: /start training/i });
      fireEvent.press(trainButton);
    });
    
    expect(mockNavigate).toHaveBeenCalledWith('Training', { horseId: '123' });
  });
});
```

### 3. Navigation Testing
```javascript
// ALWAYS test navigation flows:
describe('Navigation Flow', () => {
  it('should navigate through horse selection to training', async () => {
    const { getByText, getByRole } = render(<AppNavigator />);
    
    // Start at horse list
    await waitFor(() => {
      expect(getByText('My Horses')).toBeVisible();
    });
    
    // Select a horse
    const horseCard = getByRole('button', { name: /thunder/i });
    fireEvent.press(horseCard);
    
    // Should navigate to horse details
    await waitFor(() => {
      expect(getByText('Horse Details')).toBeVisible();
    });
    
    // Start training
    const trainButton = getByRole('button', { name: /start training/i });
    fireEvent.press(trainButton);
    
    // Should navigate to training screen
    await waitFor(() => {
      expect(getByText('Training Session')).toBeVisible();
    });
  });
});
```

## Game-Specific Testing Patterns

### 1. Horse Data Testing
```javascript
// ALWAYS test horse-specific data display:
describe('Horse Statistics Display', () => {
  it('should format discipline scores correctly', () => {
    const horse = {
      disciplines: {
        dressage: 65.5,
        showjumping: 78.2,
        crosscountry: 45.8
      }
    };
    
    render(<HorseStats horse={horse} />);
    
    expect(screen.getByText('Dressage: 66')).toBeVisible(); // Rounded
    expect(screen.getByText('Show Jumping: 78')).toBeVisible();
    expect(screen.getByText('Cross Country: 46')).toBeVisible();
  });

  it('should indicate training eligibility based on age', () => {
    const youngHorse = { id: '1', name: 'Foal', age: 2 };
    const matureHorse = { id: '2', name: 'Thunder', age: 4 };
    
    const { rerender } = render(<TrainingButton horse={youngHorse} />);
    expect(screen.getByText(/too young to train/i)).toBeVisible();
    
    rerender(<TrainingButton horse={matureHorse} />);
    expect(screen.getByRole('button', { name: /start training/i })).toBeEnabled();
  });
});
```

### 2. Form and Input Testing
```javascript
// ALWAYS test forms with realistic user input:
describe('Horse Registration Form', () => {
  it('should validate horse name input', async () => {
    render(<HorseRegistrationForm />);
    
    const nameInput = screen.getByRole('textbox', { name: /horse name/i });
    const submitButton = screen.getByRole('button', { name: /register horse/i });
    
    // Test empty name
    fireEvent.press(submitButton);
    await waitFor(() => {
      expect(screen.getByText(/name is required/i)).toBeVisible();
    });
    
    // Test valid name
    fireEvent.changeText(nameInput, 'Thunder');
    fireEvent.press(submitButton);
    
    await waitFor(() => {
      expect(screen.queryByText(/name is required/i)).toBeNull();
    });
  });

  it('should handle discipline selection', () => {
    render(<TrainingForm />);
    
    const disciplineSelector = screen.getByRole('button', { name: /select discipline/i });
    fireEvent.press(disciplineSelector);
    
    const dressageOption = screen.getByRole('button', { name: /dressage/i });
    fireEvent.press(dressageOption);
    
    expect(screen.getByDisplayValue('dressage')).toBeVisible();
  });
});
```

### 3. Loading and Error States
```javascript
// ALWAYS test loading and error states:
describe('Data Loading States', () => {
  it('should show loading indicator while fetching horses', () => {
    // Mock pending API call
    jest.spyOn(api, 'getHorses').mockImplementation(
      () => new Promise(resolve => setTimeout(resolve, 1000))
    );
    
    render(<HorsesList />);
    
    expect(screen.getByRole('progressbar')).toBeVisible();
    expect(screen.getByText(/loading horses/i)).toBeVisible();
  });

  it('should display error message on API failure', async () => {
    jest.spyOn(api, 'getHorses').mockRejectedValue(
      new Error('Network error')
    );
    
    render(<HorsesList />);
    
    await waitFor(() => {
      expect(screen.getByText(/failed to load horses/i)).toBeVisible();
      expect(screen.getByRole('button', { name: /retry/i })).toBeVisible();
    });
  });

  it('should retry loading when retry button pressed', async () => {
    const mockGetHorses = jest.spyOn(api, 'getHorses')
      .mockRejectedValueOnce(new Error('Network error'))
      .mockResolvedValueOnce([{ id: '1', name: 'Thunder' }]);
    
    render(<HorsesList />);
    
    await waitFor(() => {
      const retryButton = screen.getByRole('button', { name: /retry/i });
      fireEvent.press(retryButton);
    });
    
    await waitFor(() => {
      expect(screen.getByText('Thunder')).toBeVisible();
    });
    
    expect(mockGetHorses).toHaveBeenCalledTimes(2);
  });
});
```

## Performance Testing

### 1. Render Performance
```javascript
// ALWAYS test component render performance:
describe('Performance Tests', () => {
  it('should render large horse lists efficiently', () => {
    const manyHorses = Array.from({ length: 100 }, (_, i) => ({
      id: `horse-${i}`,
      name: `Horse ${i}`,
      age: Math.floor(Math.random() * 20) + 1
    }));
    
    const startTime = performance.now();
    render(<HorsesList horses={manyHorses} />);
    const endTime = performance.now();
    
    // Should render within reasonable time
    expect(endTime - startTime).toBeLessThan(100); // 100ms
  });

  it('should not re-render unnecessarily', () => {
    const mockHorse = { id: '1', name: 'Thunder', age: 4 };
    let renderCount = 0;
    
    const TestComponent = React.memo(() => {
      renderCount++;
      return <HorseCard horse={mockHorse} />;
    });
    
    const { rerender } = render(<TestComponent />);
    expect(renderCount).toBe(1);
    
    // Re-render with same props
    rerender(<TestComponent />);
    expect(renderCount).toBe(1); // Should not re-render
  });
});
```

### 2. Memory Usage Testing

```javascript
// ALWAYS monitor memory usage in performance tests:
describe('Memory Performance', () => {
  it('should clean up event listeners on unmount', () => {
    const { unmount } = render(<TraitDisplay traits={{}} />);
    
    // Verify no memory leaks
    unmount();
    
    // Check that component properly cleans up
    expect(document.querySelectorAll('*').length).toBeLessThan(100);
  });
});
```

---



These React Native testing rules ensure comprehensive test coverage for Equoria's mobile frontend, focusing on user behavior, accessibility, performance, and game-specific functionality.