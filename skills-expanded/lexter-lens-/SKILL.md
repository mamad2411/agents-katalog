source: https://highbar.notion.site/React-Dev-Handbook-15296734e9f080768790c218f35469fb

# React Dev Handbook

# Design Patterns

the benefit of the patterns below are:

- readability, as everything is consistently nested in the DOM
- a better layout flow state, there is less cognitive overhead when laying out views, as you don’t need to think “what prop should I use to do this thing”
- generally less cognitive overhead when looking at any given piece of data or code.

## Child first design

Instead of drilling data into a component, favor creating wrapper elements and nesting child components within.

If a component has one view function (display a single item like a “card” or “chip”), prefer children over props such as “title” or “label”.

Example: `Card.tsx`

## Widgets to be Type Generic w/ accessors

more complex widgets, such as tables, etc, should use accessors and be type flexible.

example: `PapCraTa3.tsx`

## Wrap complex design library widgets

Design Libraries often supply very complex widgets to use in the apps, we would like to land on a standard that can be used between any given libraries. This piece is a work in progress, and likely will be a moving target during the lifecycle of the Lexter ecosystem. When working on short-term proof-of-concepts this is not necessary.

See: `PapCraTa.tsx` for examples

The benefit from this pattern is a unified api for common elements, and less overhead when swapping out (or re-writing) libraries in the future.

# Styling Concerns

## Opt for tailwind

when using multiple libraries, as shown in components like `Page.tsx` , we see that we combine Radix UI with Material’s styled components.
We prefer the styling of material at the definition of a design system element, and then we can opt to customize it further with tailwind at implementation.

## Prefer className prop over emotion style attributes

| do                                                | do not                                 |
| ------------------------------------------------- | -------------------------------------- |
| try                                               | try not                                |
| `className="flex flex-col gap-3 justify-between"` | `flex=”col” gap="3" justify="between"` |

# Code Style

## Atomic, immutable, guard statement thinking - for happier brains and quicker grok.

when working within a function, opt to use guard statements to discard possibilities before getting to the main use of your code. for the love of god, avoid nesting truthy conditionals. Sometimes, this means less DRY code, but in most non-maintenance portions of the project, we are going to be throwing away a lot of the code, often, so do not over abstract, or try to solve things in a more complex way.

### Good

```tsx
const createUrl = (path?: string | number) => {
  if (!value) return `/api/data?format=csv`

  return `/api/data/${path}?format=csv&records=all`
}
```

### Bad

```tsx
const createUrl = (partial?: string | number) => {
  let result = '/api'
  let params = '?format=csv'

  if (value) {
    result += `${partial}`
    params += '&records=all'
  }

  return (result += params)
}
```

## Don’t DRY until it’s actually MOIST

I don’t have an acronym for moist, just don’t dry up your code until you actually have to re-write something 3 or 4 times. Make sure that your solution is an actual pattern that can be implemented often without a ton of configuration.

This means writing the same thing a few times, it means longer functions, but as mentioned above, your (and my) code will likely be deleted in short order and replaced with something newer and more fitting to the domain.

## Destructure props, contain hooks in a variable

Props for a given component should be destructured at the top of the definition, while (most) hooks should retain their domain-specific naming to reduce cognitive load. The exception being array result hooks, where naming destructured elements leads to more clarity (like useState)

Hook Examples:

| favor                            | undesirable                                                |
| -------------------------------- | ---------------------------------------------------------- |
| `const form = useForm<Lawyer>()` | `const { onSubmit, values, register } = useForm<Lawyer>()` |

## Event Handler Naming Convention

if an event handler is passed as a prop, it should be called `onThing` , while if defined within a component, it should be called `handleThing`

## One File, One Component

Especially in the /lib folder. Splitting components into separate files gives the mind the context to grok a single domain concern, making code easier to understand and maintain.

## No magic numbers

having things like `const count = 3` outside of your component definition is discouraged, prefer to put all of these in a `constants.ts` file, or defined as parameters in the component props, or hook.

## No Barrel Files

No barrel files are to be used to provide convenient exports, it’s extra work with no benefit.
It also eliminates extra clicks when trying to navigate to a givent element’s source code (ctrl+click)

## Named Exports over Default Exports

Named exports provide absolute clarity on where data comes from when imported.

## (Pages) Path-based file naming (a-la next.js)

File paths should be representative of the browser path, the component to be named something representative of the domain

Example:

| path                          | name                               |
| ----------------------------- | ---------------------------------- |
| `/admin/questions/layout.tsx` | `export const AdminQuestionsIndex` |

## (Components/Widgets) Filename should match Component Name

# Architectural Patterns

## Typescript First, & at the source

Make sure data is accurately typed and maintained at the first place it enters the system. generally speaking, this is at the data hooks, or possibly when fetching from local storage or params. If it is one of the latter, a nice to have is a domain wrapper around those given pieces (which can live in the same hook file / folder as the types and other hooks)

- if you have to do a type cast, as yourself if the type could have been defined at an earlier stage in the data’s lifecycle.

## Favour Routing rather than drilling data into a view

each major view should fetch all domain data necessary to populate the view, rather than relying on a large data object to populate the view. We do not prefer central data sources and state management tools such as redux. The data that is expected at any given time should be reflected in the page/view’s route definition and parameters.
