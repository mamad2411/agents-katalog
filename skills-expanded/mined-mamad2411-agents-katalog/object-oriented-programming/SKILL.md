-----
name: object-oriented-programming
description: >
  Expert in Object-Oriented Programming (OOP) design principles, patterns, and best 
  practices. Use this skill for designing maintainable software, implementing robust 
  class hierarchies, applying SOLID principles, and solving architectural challenges 
  using object-oriented approaches. Covers inheritance, polymorphism, encapsulation, 
  composition, design patterns, and code organization.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: computer-science
  tags: [oop, design-patterns, solid, architecture, software-design]

# Object-Oriented Programming

Covers: **SOLID Principles · Design Patterns · Class Design · Inheritance vs Composition · Polymorphism · Encapsulation · SOLID · Dependency Injection**

-----

## Core OOP Principles

### The Four Pillars

| Principle | Description | Benefit |
|-----------|-------------|---------|
| **Encapsulation** | Bundling data with methods that operate on it | Data hiding, reduced coupling |
| **Inheritance** | Creating new classes from existing ones | Code reuse, IS-A relationships |
| **Polymorphism** | Objects of different types treated uniformly | Flexibility, substitutability |
| **Abstraction** | Hiding complex implementation details | Simplicity, maintainability |

### Encapsulation Best Practices

```python
from typing import Optional, List, Any
from datetime import datetime

class BankAccount:
    """Proper encapsulation with validation and data hiding"""
    
    def __init__(self, account_id: str, initial_balance: float = 0.0):
        self._id = account_id  # Protected attribute
        self.__balance = initial_balance  # Private attribute (name mangling)
        self._transactions: List[dict] = []
    
    @property
    def balance(self) -> float:
        """Read-only balance access"""
        return self.__balance
    
    @property
    def account_id(self) -> str:
        return self._id
    
    def deposit(self, amount: float) -> bool:
        """Deposit money with validation"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        if amount > 100000:  # Regulatory limit
            raise ValueError("Deposit amount exceeds limit")
        
        self.__balance += amount
        self._record_transaction('deposit', amount)
        return True
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw money with overdraft protection"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        
        self.__balance -= amount
        self._record_transaction('withdrawal', amount)
        return True
    
    def _record_transaction(self, tx_type: str, amount: float):
        """Internal method - protected"""
        self._transactions.append({
            'type': tx_type,
            'amount': amount,
            'timestamp': datetime.now(),
            'balance_after': self.__balance
        })
    
    def get_transaction_history(self) -> List[dict]:
        """Return copy to preserve encapsulation"""
        return self._transactions.copy()
```

### Inheritance vs Composition

```python
from abc import ABC, abstractmethod
from typing import List

# INHERITANCE - Use when clear IS-A relationship exists
class Animal(ABC):
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def speak(self) -> str:
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"

class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} says Meow!"

# COMPOSITION - Use when HAS-A or CAN-DO relationship
class Engine:
    def start(self):
        return "Engine started"
    
    def stop(self):
        return "Engine stopped"

class Car:
    """Car HAS-A Engine - composition"""
    def __init__(self, make: str, model: str):
        self.make = make
        self.model = model
        self._engine = Engine()  # Composition: owns the engine
    
    def start(self):
        return f"{self.make} {self.model}: {self._engine.start()}"
    
    def stop(self):
        return f"{self.make} {self.model}: {self._engine.stop()}"

# MIXIN - For reusable behaviors
class Swimmer:
    def swim(self) -> str:
        return f"{self.name} is swimming"

class Diver(Swimmer, Animal):
    """Multiple inheritance with mixins"""
    def __init__(self, name: str):
        super().__init__(name)
    
    def dive(self) -> str:
        return f"{self.name} dives underwater"

# PREFER COMPOSITION OVER INHERITANCE
class Logger:
    def log(self, message: str):
        print(f"[LOG] {message}")

class FileLogger(Logger):
    def log(self, message: str):
        with open('app.log', 'a') as f:
            f.write(f"{message}\n")

class DatabaseLogger(Logger):
    def log(self, message: str):
        # Save to database
        pass

class ReportGenerator:
    """Uses composition for flexible logging"""
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def generate(self):
        self.logger.log("Generating report")
        # Generation logic
```

-----

## SOLID Principles

### Single Responsibility Principle (SRP)

```python
# BAD - Multiple responsibilities
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
    
    def save(self):
        # Database logic
        pass
    
    def send_email(self):
        # Email logic
        pass
    
    def validate(self):
        # Validation logic
        pass

# GOOD - Each class has one responsibility
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class UserValidator:
    def validate(self, user: User) -> bool:
        if not user.email or '@' not in user.email:
            return False
        return True

class UserRepository:
    def save(self, user: User):
        # Database save logic
        pass
    
    def find_by_email(self, email: str) -> User:
        # Find user logic
        pass

class EmailService:
    def send(self, to: str, subject: str, body: str):
        # Email sending logic
        pass
```

### Open/Closed Principle (OCP)

```python
from abc import ABC, abstractmethod

# BAD - Need to modify for each new discount type
class OrderDiscount:
    def apply_discount(self, order_total: float, discount_type: str) -> float:
        if discount_type == 'percentage':
            return order_total * 0.9
        elif discount_type == 'fixed':
            return order_total - 10
        elif discount_type == 'shipping':
            return order_total  # Free shipping
        # Must modify this for new types!
        return order_total

# GOOD - Open for extension, closed for modification
class Discount(ABC):
    @abstractmethod
    def apply(self, order_total: float) -> float:
        pass

class PercentageDiscount(Discount):
    def __init__(self, percent: float):
        self.percent = percent
    
    def apply(self, order_total: float) -> float:
        return order_total * (1 - self.percent / 100)

class FixedDiscount(Discount):
    def __init__(self, amount: float):
        self.amount = amount
    
    def apply(self, order_total: float) -> float:
        return max(0, order_total - self.amount)

class FreeShipping(Discount):
    def apply(self, order_total: float) -> float:
        return order_total  # Free shipping

class DiscountCalculator:
    def __init__(self):
        self._discounts: List[Discount] = []
    
    def add_discount(self, discount: Discount):
        self._discounts.append(discount)
    
    def calculate(self, order_total: float) -> float:
        result = order_total
        for discount in self._discounts:
            result = discount.apply(result)
        return result
```

### Liskov Substitution Principle (LSP)

```python
# BAD - Square violates rectangle contract
class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height

class Square(Rectangle):
    def __init__(self, side: float):
        super().__init__(side, side)
    
    @Rectangle.width.setter
    def width(self, value: float):
        self.width = value
        self.height = value  # Breaks expectation!

# GOOD - Proper abstraction
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height

class Square(Shape):
    def __init__(self, side: float):
        self.side = side
    
    def area(self) -> float:
        return self.side ** 2

# Or use a factory
class ShapeFactory:
    @staticmethod
    def create_rectangle(width: float, height: float) -> Shape:
        return Rectangle(width, height)
    
    @staticmethod
    def create_square(side: float) -> Shape:
        return Square(side)
```

### Interface Segregation Principle (ISP)

```python
from abc import ABC, abstractmethod

# BAD - Fat interface forces implementation of unused methods
class Machine(ABC):
    @abstractmethod
    def print(self, document):
        pass
    
    @abstractmethod
    def scan(self, document):
        pass
    
    @abstractmethod
    def fax(self, document):
        pass

class OldPrinter(Machine):
    def print(self, document):
        print(f"Printing: {document}")
    
    def scan(self, document):
        raise NotImplementedError("Cannot scan")
    
    def fax(self, document):
        raise NotImplementedError("Cannot fax")

# GOOD - Small, focused interfaces
class Printer(ABC):
    @abstractmethod
    def print(self, document):
        pass

class Scanner(ABC):
    @abstractmethod
    def scan(self, document):
        pass

class Fax(ABC):
    @abstractmethod
    def fax(self, document):
        pass

class OldPrinter(Printer):
    def print(self, document):
        print(f"Printing: {document}")

class MultiFunctionPrinter(Printer, Scanner, Fax):
    def print(self, document):
        print(f"Printing: {document}")
    
    def scan(self, document):
        print(f"Scanning: {document}")
    
    def fax(self, document):
        print(f"Faxing: {document}")
```

### Dependency Inversion Principle (DIP)

```python
from abc import ABC, abstractmethod

# BAD - High-level depends on low-level
class MySQLDatabase:
    def connect(self):
        pass
    
    def query(self, sql: str):
        pass

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # Direct dependency
    
    def get_user(self, user_id: int):
        self.db.query(f"SELECT * FROM users WHERE id = {user_id}")

# GOOD - Depend on abstractions
class Database(ABC):
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def query(self, sql: str):
        pass

class MySQLDatabase(Database):
    def connect(self):
        pass
    
    def query(self, sql: str):
        pass

class PostgreSQLDatabase(Database):
    def connect(self):
        pass
    
    def query(self, sql: str):
        pass

class UserService:
    def __init__(self, database: Database):  # Dependency injection
        self.db = database
    
    def get_user(self, user_id: int):
        self.db.query(f"SELECT * FROM users WHERE id = {user_id}")

# Usage
mysql_db = MySQLDatabase()
user_service = UserService(mysql_db)
```

-----

## Design Patterns

### Creational Patterns

```python
# FACTORY METHOD
class Document(ABC):
    @abstractmethod
    def render(self):
        pass

class PDFDocument(Document):
    def render(self):
        return "Rendering PDF"

class WordDocument(Document):
    def render(self):
        return "Rendering Word"

class DocumentFactory(ABC):
    @abstractmethod
    def create_document(self) -> Document:
        pass

class PDFDocumentFactory(DocumentFactory):
    def create_document(self) -> Document:
        return PDFDocument()

# ABSTRACT FACTORY
class Button(ABC):
    @abstractmethod
    def render(self):
        pass

class Checkbox(ABC):
    @abstractmethod
    def render(self):
        pass

class WindowsButton(Button):
    def render(self):
        return "Windows Button"

class MacButton(Button):
    def render(self):
        return "Mac Button"

class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

class WindowsFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

# SINGLETON
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# BUILDER
class QueryBuilder:
    def __init__(self):
        self._select = []
        self._from = None
        self._where = []
        self._order_by = []
    
    def select(self, *columns):
        self._select = list(columns)
        return self
    
    def from_table(self, table):
        self._from = table
        return self
    
    def where(self, condition):
        self._where.append(condition)
        return self
    
    def order_by(self, column):
        self._order_by.append(column)
        return self
    
    def build(self) -> str:
        query = f"SELECT {', '.join(self._select) if self._select else '*'}"
        query += f" FROM {self._from}"
        if self._where:
            query += f" WHERE {' AND '.join(self._where)}"
        if self._order_by:
            query += f" ORDER BY {', '.join(self._order_by)}"
        return query

# Usage
query = (QueryBuilder()
    .select("id", "name", "email")
    .from_table("users")
    .where("active = true")
    .where("role = 'admin'")
    .order_by("name")
    .build())
```

### Structural Patterns

```python
# ADAPTER
class LegacyPayment:
    def pay(self, amount: float, currency: str):
        return f"Legacy payment: {amount} {currency}"

class ModernPayment(ABC):
    @abstractmethod
    def process_payment(self, amount: float):
        pass

class PaymentAdapter(ModernPayment):
    def __init__(self, legacy: LegacyPayment):
        self.legacy = legacy
    
    def process_payment(self, amount: float):
        return self.legacy.pay(amount, "USD")

# DECORATOR
class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass

class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 2.00

class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def cost(self) -> float:
        return self._coffee.cost()

class Milk(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.50

class Sugar(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.25

# PROXY
class RealImage:
    def __init__(self, filename: str):
        self.filename = filename
        self._load()
    
    def _load(self):
        print(f"Loading {self.filename}")
    
    def display(self):
        print(f"Displaying {self.filename}")

class ProxyImage:
    def __init__(self, filename: str):
        self.filename = filename
        self._real_image = None
    
    def display(self):
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()

# FACADE
class CPU:
    def freeze(self):
        print("CPU: Freezing")
    
    def jump(self, position):
        print(f"CPU: Jumping to {position}")
    
    def execute(self):
        print("CPU: Executing")

class Memory:
    def load(self, position, data):
        print(f"Memory: Loading {data} at {position}")

class HardDrive:
    def read(self, sector, size):
        print(f"HardDrive: Reading {size} bytes from sector {sector}")
        return "boot data"

class ComputerFacade:
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()
    
    def start(self):
        self.cpu.freeze()
        boot_data = self.hard_drive.read(0, 1024)
        self.memory.load(0, boot_data)
        self.cpu.jump(0)
        self.cpu.execute()
```

### Behavioral Patterns

```python
# OBSERVER
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

class Subject:
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def detach(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class ConcreteObserver(Observer):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, message):
        print(f"{self.name} received: {message}")

# STRATEGY
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List):
        pass

class QuickSort(SortStrategy):
    def sort(self, data: List):
        # Quick sort implementation
        return sorted(data)

class MergeSort(SortStrategy):
    def sort(self, data: List):
        # Merge sort implementation
        return sorted(data)

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy
    
    def sort(self, data: List):
        return self._strategy.sort(data)

# COMMAND
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

class Light:
    def on(self):
        print("Light ON")
    
    def off(self):
        print("Light OFF")

class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self):
        self.light.on()
    
    def undo(self):
        self.light.off()

class RemoteControl:
    def __init__(self):
        self._history: List[Command] = []
    
    def execute(self, command: Command):
        command.execute()
        self._history.append(command)
    
    def undo_last(self):
        if self._history:
            command = self._history.pop()
            command.undo()

# STATE
class State(ABC):
    @abstractmethod
    def handle(self, context):
        pass

class ConcreteStateA(State):
    def handle(self, context):
        print("State A handling")
        context.state = ConcreteStateB()

class Context:
    def __init__(self, state: State):
        self.state = state
    
    def request(self):
        self.state.handle(self)
```

-----

## Testing OOP Code

```python
import unittest
from unittest.mock import Mock, patch

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("ACC001", 1000.0)
    
    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000.0)
    
    def test_deposit_increases_balance(self):
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
    
    def test_withdraw_decreases_balance(self):
        self.account.withdraw(300.0)
        self.assertEqual(self.account.balance, 700.0)
    
    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(2000.0)
    
    def test_negative_deposit_raises_error(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100.0)
    
    def test_transaction_history_recorded(self):
        self.account.deposit(500.0)
        history = self.account.get_transaction_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['type'], 'deposit')

class TestDependencyInjection(unittest.TestCase):
    def test_user_service_with_different_databases(self):
        mock_mysql = Mock(spec=Database)
        mock_postgres = Mock(spec=Database)
        
        service_mysql = UserService(mock_mysql)
        service_postgres = UserService(mock_postgres)
        
        service_mysql.get_user(1)
        service_postgres.get_user(1)
        
        mock_mysql.query.assert_called_once()
        mock_postgres.query.assert_called_once()
```

-----

## Common OOP Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **God Object** | Class knows/does too much | Apply SRP, split responsibilities |
| **Shotgun Surgery** | Changes require many modifications | Increase cohesion |
| **Spaghetti Inheritance** | Deep, complex inheritance hierarchy | Prefer composition |
| **Circle-Ellipse Problem** | Inheritance for related but different types | Use composition or interfaces |
| **Anemic Domain Model** | Classes with only data, no behavior | Add business logic to domain objects |
| **Feature Envy** | Method uses too much of another class | Move method to the class it envies |
