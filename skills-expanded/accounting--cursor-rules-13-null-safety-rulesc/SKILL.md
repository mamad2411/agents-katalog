---
globs:
  - "**/*.ts"
  - "**/*.tsx"
alwaysApply: false
---

# Null Safety & Defensive Programming

## TypeScript Strict Mode

### Enable Strict Null Checks
```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "strictNullChecks": true,
    "noImplicitAny": true,
    "noUncheckedIndexedAccess": true
  }
}
```

## Null Checking Patterns

### Explicit Null Types
```typescript
// ✅ GOOD: Explicit nullable types
interface Animal {
  id: string;
  name: string;
  notes: string | null;        // Can be null
  lastWeighedAt?: Date;        // Optional (undefined)
}

// ❌ BAD: Implicit any/null
interface Animal {
  notes: any;  // Don't use any
}
```

### Null Coalescing
```typescript
// ✅ GOOD: Nullish coalescing operator
const displayName = animal.nickname ?? animal.name ?? 'Unknown';
const weight = record.weight ?? 0;

// ✅ GOOD: Optional chaining
const ownerName = animal.owner?.name ?? 'No owner';
const firstTag = animal.tags?.[0]?.value;

// ❌ BAD: Truthy checks (0 and '' are falsy!)
const weight = record.weight || 0;  // Bug if weight is 0
```

### Type Guards
```typescript
// Type guard functions
function isNotNull<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

function isString(value: unknown): value is string {
  return typeof value === 'string';
}

// Usage
const animals = results.filter(isNotNull);

if (isString(input)) {
  // TypeScript knows input is string here
  console.log(input.toUpperCase());
}
```

### Assertion Functions
```typescript
// Assert and throw if null
function assertNotNull<T>(
  value: T | null | undefined, 
  message: string
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message);
  }
}

// Usage
const animal = await repository.getById(id);
assertNotNull(animal, `Animal ${id} not found`);
// TypeScript knows animal is not null below this line
console.log(animal.name);
```

## Repository Patterns

### Nullable Return Types
```typescript
interface IAnimalRepository {
  // Returns null when not found (expected case)
  getById(id: string): Promise<Animal | null>;
  
  // Returns empty array when none found
  getAll(): Promise<Animal[]>;
  
  // Throws if operation fails (unexpected case)
  save(animal: Animal): Promise<void>;
}
```

### Handle Null in Use Cases
```typescript
export class GetAnimalUseCase {
  async execute(id: string): Promise<Result<Animal, DomainException>> {
    const animal = await this.repository.getById(id);
    
    // Explicit null check with typed error
    if (animal === null) {
      return Result.failure(new AnimalNotFoundException(id));
    }
    
    return Result.ok(animal);
  }
}
```

## Array Safety

### Safe Array Access
```typescript
// ✅ GOOD: Check array bounds
function getFirstAnimal(animals: Animal[]): Animal | undefined {
  return animals[0];  // With noUncheckedIndexedAccess, this is Animal | undefined
}

// ✅ GOOD: Use array methods
const firstAnimal = animals.at(0);  // Returns undefined if empty
const lastAnimal = animals.at(-1);

// ✅ GOOD: Destructuring with defaults
const [first = defaultAnimal] = animals;

// ❌ BAD: Assuming array has elements
const first = animals[0]!;  // Avoid non-null assertion
```

### Safe Array Operations
```typescript
// ✅ GOOD: Filter out nulls with type safety
const animals: (Animal | null)[] = await fetchAnimals();
const validAnimals: Animal[] = animals.filter(isNotNull);

// ✅ GOOD: Safe map with null handling
const names = animals
  .filter(isNotNull)
  .map(a => a.name);
```

## Object Property Access

### Safe Property Access
```typescript
// ✅ GOOD: Optional chaining for nested properties
const city = user?.address?.city ?? 'Unknown';

// ✅ GOOD: Check before accessing
if (animal.owner && animal.owner.contact) {
  sendNotification(animal.owner.contact);
}

// ✅ GOOD: Destructuring with defaults
const { name = 'Unknown', weight = 0 } = animal;
```

### Record/Map Access
```typescript
// ✅ GOOD: Type-safe record access
const animalMap: Record<string, Animal> = {};

function getAnimal(id: string): Animal | undefined {
  return animalMap[id];  // Correctly typed as Animal | undefined
}

// Usage with null check
const animal = getAnimal(id);
if (animal) {
  console.log(animal.name);
}
```

## Function Parameters

### Required vs Optional
```typescript
// ✅ GOOD: Clear parameter requirements
function createWeight(
  animalId: string,                    // Required
  weight: number,                       // Required
  notes?: string,                       // Optional
  recordedAt: Date = new Date()         // Default value
): WeightRecord {
  return {
    id: generateId(),
    animalId,
    weight,
    notes: notes ?? null,
    recordedAt,
  };
}
```

### Validate Parameters
```typescript
function processWeight(weight: number | null | undefined): number {
  if (weight === null || weight === undefined) {
    throw new InvalidParameterException('Weight is required');
  }
  
  if (weight <= 0) {
    throw new InvalidParameterException('Weight must be positive');
  }
  
  return weight;
}
```

## React Component Props

### Props with Defaults
```typescript
interface AnimalCardProps {
  animal: Animal;
  showWeight?: boolean;
  onPress?: (id: string) => void;
}

export const AnimalCard: React.FC<AnimalCardProps> = ({
  animal,
  showWeight = true,
  onPress,
}) => {
  const handlePress = () => {
    onPress?.(animal.id);  // Safe optional call
  };

  return (
    <TouchableOpacity onPress={handlePress}>
      <Text>{animal.name}</Text>
      {showWeight && animal.currentWeight && (
        <Text>{animal.currentWeight} kg</Text>
      )}
    </TouchableOpacity>
  );
};
```

## Database Null Handling

### SQLite NULL Mapping
```typescript
// Mapper handles database nulls
class AnimalMapper {
  static toDomain(dto: AnimalDTO): Animal {
    return {
      id: dto.id,
      name: dto.name,
      // Map SQL NULL to TypeScript null
      notes: dto.notes ?? null,
      // Map missing timestamp to undefined
      lastWeighedAt: dto.last_weighed_at 
        ? new Date(dto.last_weighed_at) 
        : undefined,
    };
  }
}
```

## Avoid These Anti-Patterns

```typescript
// ❌ BAD: Non-null assertion without checks
const name = animal!.name;

// ❌ BAD: Type assertion to bypass null checks
const animal = result as Animal;

// ❌ BAD: Catching null errors instead of preventing
try {
  console.log(animal.name);
} catch (e) {
  // Too late - should check before
}

// ❌ BAD: Using || for defaults (fails for 0, '', false)
const count = value || 10;  // Bug if value is 0
```

## Best Practices Summary

1. **Enable strict TypeScript** - `strictNullChecks: true`
2. **Use explicit types** - `string | null` vs `string?`
3. **Prefer `??` over `||`** - Nullish coalescing is null-safe
4. **Use optional chaining** - `obj?.prop?.nested`
5. **Filter nulls explicitly** - `.filter(isNotNull)`
6. **Return `Result<T, E>`** - Instead of throwing or returning null
7. **Validate at boundaries** - Check inputs at API/UI boundaries
