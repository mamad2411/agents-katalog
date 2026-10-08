
# Skill


## Properties

Name | Type
------------ | -------------
`id` | number
`event` | [IdInfo](IdInfo.md)
`team` | [IdInfo](IdInfo.md)
`type` | [SkillType](SkillType.md)
`season` | [IdInfo](IdInfo.md)
`division` | [IdInfo](IdInfo.md)
`rank` | number
`score` | number
`attempts` | number

## Example

```typescript
import type { Skill } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "event": null,
  "team": null,
  "type": null,
  "season": null,
  "division": null,
  "rank": null,
  "score": null,
  "attempts": null,
} satisfies Skill

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as Skill
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


