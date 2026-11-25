---
name: javascript-mastery
description: "Referência abrangente de JavaScript cobrindo 33+ conceitos essenciais que todo desenvolvedor deve conhecer. Desde fundamentos como primitivos e closures até padrões avançados como async/await e programação funcional. Use ao explicar conceitos de JS, depurar problemas de JavaScript ou ensinar fundamentos de JavaScript."
---

# 🧠 JavaScript Mastery

> 33+ conceitos essenciais de JavaScript que todo desenvolvedor deve conhecer, inspirado em [33-js-concepts](https://github.com/leonardomso/33-js-concepts).

## Quando Usar Esta Skill

Use esta skill quando:

- Explicar conceitos de JavaScript
- Depurar comportamentos complicados de JS
- Ensinar fundamentos de JavaScript
- Revisar código para boas práticas em JS
- Entender peculiaridades da linguagem

---

## 1. Fundamentos

### 1.1 Tipos Primitivos

JavaScript possui 7 tipos primitivos:

```javascript
// String
const str = "hello";

// Number (inteiros e floats)
const num = 42;
const float = 3.14;

// BigInt (para inteiros grandes)
const big = 9007199254740991n;

// Boolean
const bool = true;

// Undefined
let undef; // undefined

// Null
const empty = null;

// Symbol (identificadores únicos)
const sym = Symbol("description");
```

**Pontos-chave**:

- Primitivos são imutáveis
- Passados por valor
- `typeof null === "object"` é um bug histórico

### 1.2 Coerção de Tipo

JavaScript converte tipos implicitamente:

```javascript
// Coerção de string
"5" + 3; // "53" (number → string)
"5" - 3; // 2    (string → number)

// Coerção de boolean
Boolean(""); // false
Boolean("hello"); // true
Boolean(0); // false
Boolean([]); // true (!)

// Coerção de igualdade
"5" == 5; // true  (coage)
"5" === 5; // false (estrito)
```

**Valores falsy** (8 no total):
`false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN`

### 1.3 Operadores de Igualdade

```javascript
// == (igualdade solta) - coage tipos
null == undefined; // true
"1" == 1; // true

// === (igualdade estrita) - sem coerção
null === undefined; // false
"1" === 1; // false

// Object.is() - trata casos especiais
Object.is(NaN, NaN); // true (NaN === NaN é false!)
Object.is(-0, 0); // false (0 === -0 é true!)
```

**Regra**: Sempre use `===` a menos que tenha uma razão específica para não fazer.

---

## 2. Escopo & Closures

### 2.1 Tipos de Escopo

```javascript
// Escopo global
var globalVar = "global";

function outer() {
  // Escopo de função
  var functionVar = "function";

  if (true) {
    // Escopo de bloco (somente let/const)
    let blockVar = "block";
    const alsoBlock = "block";
    var notBlock = "function"; // var ignora blocos!
  }
}
```

### 2.2 Closures

Um closure é uma função que lembra de seu escopo léxico:

```javascript
function createCounter() {
  let count = 0; // variável "fechada"

  return {
    increment() {
      return ++count;
    },
    decrement() {
      return --count;
    },
    getCount() {
      return count;
    },
  };
}

const counter = createCounter();
counter.increment(); // 1
counter.increment(); // 2
counter.getCount(); // 2
```

**Casos de uso comuns**:

- Privacidade de dados (padrão de módulo)
- Fábricas de função
- Aplicação parcial
- Memoização

### 2.3 var vs let vs const

```javascript
// var - escopo de função, hoisted, pode redeclarar
var x = 1;
var x = 2; // OK

// let - escopo de bloco, hoisted (TDZ), sem redeclaração
let y = 1;
// let y = 2; // Erro!

// const - como let, mas não pode reatribuir
const z = 1;
// z = 2; // Erro!

// MAS: objetos const são mutáveis
const obj = { a: 1 };
obj.a = 2; // OK
obj.b = 3; // OK
```

---

## 3. Funções & Execução

### 3.1 Call Stack

```javascript
function first() {
  console.log("first start");
  second();
  console.log("first end");
}

function second() {
  console.log("second");
}

first();
// Output:
// "first start"
// "second"
// "first end"
```

Exemplo de stack overflow:

```javascript
function infinite() {
  infinite(); // Sem caso base!
}
infinite(); // RangeError: Maximum call stack size exceeded
```

### 3.2 Hoisting

```javascript
// Hoisting de variável
console.log(a); // undefined (hoisted, não inicializado)
var a = 5;

console.log(b); // ReferenceError (TDZ)
let b = 5;

// Hoisting de função
sayHi(); // Funciona!
function sayHi() {
  console.log("Hi!");
}

// Expressões de função não sofrem hoisting
sayBye(); // TypeError
var sayBye = function () {
  console.log("Bye!");
};
```

### 3.3 Palavra-chave this

```javascript
// Contexto global
console.log(this); // window (browser) ou global (Node)

// Método de objeto
const obj = {
  name: "Alice",
  greet() {
    console.log(this.name); // "Alice"
  },
};

// Arrow functions (this léxico)
const obj2 = {
  name: "Bob",
  greet: () => {
    console.log(this.name); // undefined (herda this externo)
  },
};

// Binding explícito
function greet() {
  console.log(this.name);
}
greet.call({ name: "Charlie" }); // "Charlie"
greet.apply({ name: "Diana" }); // "Diana"
const bound = greet.bind({ name: "Eve" });
bound(); // "Eve"
```

---

## 4. Event Loop & Async

### 4.1 Event Loop

```javascript
console.log("1");

setTimeout(() => console.log("2"), 0);

Promise.resolve().then(() => console.log("3"));

console.log("4");

// Output: 1, 4, 3, 2
// Por quê? Microtasks (Promises) executam antes de macrotasks (setTimeout)
```

**Ordem de execução**:

1. Código síncrono (call stack)
2. Microtasks (callbacks de Promise, queueMicrotask)
3. Macrotasks (setTimeout, setInterval, I/O)

### 4.2 Callbacks

```javascript
// Padrão de callback
function fetchData(callback) {
  setTimeout(() => {
    callback(null, { data: "result" });
  }, 1000);
}

// Convenção error-first
fetchData((error, result) => {
  if (error) {
    console.error(error);
    return;
  }
  console.log(result);
});

// Callback hell (evitar!)
getData((data) => {
  processData(data, (processed) => {
    saveData(processed, (saved) => {
      notify(saved, () => {
        // 😱 Pirâmide do caos
      });
    });
  });
});
```

### 4.3 Promises

```javascript
// Criando uma Promise
const promise = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve("Success!");
    // ou: reject(new Error("Failed!"));
  }, 1000);
});

// Consumindo Promises
promise
  .then((result) => console.log(result))
  .catch((error) => console.error(error))
  .finally(() => console.log("Done"));

// Combinadores de Promise
Promise.all([p1, p2, p3]); // Todas devem suceder
Promise.allSettled([p1, p2]); // Espera todas, obtém status
Promise.race([p1, p2]); // Primeira a se resolver
Promise.any([p1, p2]); // Primeira a suceder
```

### 4.4 async/await

```javascript
async function fetchUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) throw new Error("Failed to fetch");
    const user = await response.json();
    return user;
  } catch (error) {
    console.error("Error:", error);
    throw error; // Relança para o chamador tratar
  }
}

// Execução paralela
async function fetchAll() {
  const [users, posts] = await Promise.all([
    fetch("/api/users"),
    fetch("/api/posts"),
  ]);
  return { users, posts };
}
```

---

## 5. Programação Funcional

### 5.1 Higher-Order Functions

Funções que recebem ou retornam funções:

```javascript
// Recebe uma função
const numbers = [1, 2, 3];
const doubled = numbers.map((n) => n * 2); // [2, 4, 6]

// Retorna uma função
function multiply(a) {
  return function (b) {
    return a * b;
  };
}
const double = multiply(2);
double(5); // 10
```

### 5.2 Funções Puras

```javascript
// Pura: mesma entrada → mesma saída, sem efeitos colaterais
function add(a, b) {
  return a + b;
}

// Impura: modifica estado externo
let total = 0;
function addToTotal(value) {
  total += value; // Efeito colateral!
  return total;
}

// Impura: depende de estado externo
function getDiscount(price) {
  return price * globalDiscountRate; // Dependência externa
}
```

### 5.3 map, filter, reduce

```javascript
const users = [
  { name: "Alice", age: 25 },
  { name: "Bob", age: 30 },
  { name: "Charlie", age: 35 },
];

// map: transforma cada elemento
const names = users.map((u) => u.name);
// ["Alice", "Bob", "Charlie"]

// filter: mantém elementos que correspondem à condição
const adults = users.filter((u) => u.age >= 30);
// [{ name: "Bob", ... }, { name: "Charlie", ... }]

// reduce: acumula em um único valor
const totalAge = users.reduce((sum, u) => sum + u.age, 0);
// 90

// Encadeamento
const result = users
  .filter((u) => u.age >= 30)
  .map((u) => u.name)
  .join(", ");
// "Bob, Charlie"
```

### 5.4 Currying & Composição

```javascript
// Currying: transforma f(a, b, c) em f(a)(b)(c)
const curry = (fn) => {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn.apply(this, args);
    }
    return (...moreArgs) => curried(...args, ...moreArgs);
  };
};

const add = curry((a, b, c) => a + b + c);
add(1)(2)(3); // 6
add(1, 2)(3); // 6
add(1)(2, 3); // 6

// Composição: combina funções
const compose =
  (...fns) =>
  (x) =>
    fns.reduceRight((acc, fn) => fn(acc), x);

const pipe =
  (...fns) =>
  (x) =>
    fns.reduce((acc, fn) => fn(acc), x);

const addOne = (x) => x + 1;
const double = (x) => x * 2;

const addThenDouble = compose(double, addOne);
addThenDouble(5); // 12 = (5 + 1) * 2

const doubleThenAdd = pipe(double, addOne);
doubleThenAdd(5); // 11 = (5 * 2) + 1
```

---

## 6. Objetos & Protótipos

### 6.1 Herança Prototípica

```javascript
// Cadeia de protótipos
const animal = {
  speak() {
    console.log("Some sound");
  },
};

const dog = Object.create(animal);
dog.bark = function () {
  console.log("Woof!");
};

dog.speak(); // "Some sound" (herdado)
dog.bark(); // "Woof!" (método próprio)

// Classes ES6 (açúcar sintático)
class Animal {
  speak() {
    console.log("Some sound");
  }
}

class Dog extends Animal {
  bark() {
    console.log("Woof!");
  }
}
```

### 6.2 Métodos de Objeto

```javascript
const obj = { a: 1, b: 2 };

// Chaves, valores, entradas
Object.keys(obj); // ["a", "b"]
Object.values(obj); // [1, 2]
Object.entries(obj); // [["a", 1], ["b", 2]]

// Cópia rasa
const copy = { ...obj };
const copy2 = Object.assign({}, obj);

// Congelar (imutável)
const frozen = Object.freeze({ x: 1 });
frozen.x = 2; // Silenciosamente falha (ou lança em strict mode)

// Selar (sem add/delete, pode modificar)
const sealed = Object.seal({ x: 1 });
sealed.x = 2; // OK
sealed.y = 3; // Falha
delete sealed.x; // Falha
```

---

## 7. JavaScript Moderno (ES6+)

### 7.1 Desestruturação

```javascript
// Desestruturação de array
const [first, second, ...rest] = [1, 2, 3, 4, 5];
// first = 1, second = 2, rest = [3, 4, 5]

// Desestruturação de objeto
const { name, age, city = "Unknown" } = { name: "Alice", age: 25 };
// name = "Alice", age = 25, city = "Unknown"

// Renomeação
const { name: userName } = { name: "Bob" };
// userName = "Bob"

// Aninhado
const {
  address: { street },
} = { address: { street: "123 Main" } };
```

### 7.2 Spread & Rest

```javascript
// Spread: expande iterável
const arr1 = [1, 2, 3];
const arr2 = [...arr1, 4, 5]; // [1, 2, 3, 4, 5]

const obj1 = { a: 1 };
const obj2 = { ...obj1, b: 2 }; // { a: 1, b: 2 }

// Rest: coleta remanescente
function sum(...numbers) {
  return numbers.reduce((a, b) => a + b, 0);
}
sum(1, 2, 3, 4); // 10
```

### 7.3 Módulos

```javascript
// Exportações nomeadas
export const PI = 3.14159;
export function square(x) {
  return x * x;
}

// Exportação padrão
export default class Calculator {}

// Importando
import Calculator, { PI, square } from "./math.js";
import * as math from "./math.js";

// Importação dinâmica
const module = await import("./dynamic.js");
```

### 7.4 Optional Chaining & Nullish Coalescing

```javascript
// Optional chaining (?.)
const user = { address: { city: "NYC" } };
const city = user?.address?.city; // "NYC"
const zip = user?.address?.zip; // undefined (sem erro)
const fn = user?.getName?.(); // undefined se sem método

// Nullish coalescing (??)
const value = null ?? "default"; // "default"
const zero = 0 ?? "default"; // 0 (não é nullish!)
const empty = "" ?? "default"; // "" (não é nullish!)

// Compare com ||
const value2 = 0 || "default"; // "default" (0 é falsy)
```

---

## Cartão de Referência Rápida

| Conceito       | Ponto-chave                           |
| :------------- | :------------------------------------ |
| `==` vs `===`  | Sempre use `===`                      |
| `var` vs `let` | Prefira `let`/`const`                 |
| Closures       | Função + escopo léxico                |
| `this`         | Depende de como a função é chamada    |
| Event loop     | Microtasks antes de macrotasks        |
| Funções puras  | Mesma entrada → mesma saída           |
| Protótipos     | `__proto__` → cadeia de protótipos    |
| `??` vs `\|\|` | `??` verifica apenas null/undefined   |

---

## Recursos

- [33 JS Concepts](https://github.com/leonardomso/33-js-concepts)
- [JavaScript.info](https://javascript.info/)
- [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)
- [You Don't Know JS](https://github.com/getify/You-Dont-Know-JS)