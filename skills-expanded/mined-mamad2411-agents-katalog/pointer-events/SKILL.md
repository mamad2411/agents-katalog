---
name: pointer-events
description: "Forward DOM pointer events into a Three.js scene and filter them with @pmndrs/pointer-events for click/tap/hover interaction with 3D objects and portals. Use when objects in the scene need to be clickable, selectable, or hoverable."
---

# Pointer Events via `@pmndrs/pointer-events`

## How to use

We can use `forwardHtmlEvents` to forward the html document events into the 3D scene.

```js
import * as THREE from 'three'
import { forwardHtmlEvents, PointerEvent } from '@pmndrs/pointer-events'

const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(70, width / height, 0.01, 10)
camera.position.z = 1
const { update } = forwardHtmlEvents(document.body, () => camera, scene)

const width = window.innerWidth,
  height = window.innerHeight

const geometry = new THREE.BoxGeometry(0.2, 0.2, 0.2)
const material = new THREE.MeshBasicMaterial({ color: new THREE.Color('red') })
const mesh = new THREE.Mesh(geometry, material)
scene.add(mesh)

mesh.addEventListener('pointerover', (e: PointerEvent) => material.color.set('blue'))
mesh.addEventListener('pointerover', (e: PointerEvent) => console.log(e.point.toArray()))
mesh.addEventListener('pointerout', (e: PointerEvent) => material.color.set('red'))

const renderer = new THREE.WebGLRenderer({ antialias: true })
renderer.setSize(width, height)
renderer.setAnimationLoop(() => {
  update()
  renderer.render(scene, camera)
})
```

Furthermore, we can also use `forwardObjectEvents` to forward events from e.g. a plane into a seperate scene rendered on this plane for building an interactive portal.

## Event Filtering

Based on the css `pointer-events` property, the behavior of pointer events can be configured with the values `none`, `listener`, or `auto`.

```js
object.pointerEvents = 'none'
```

The values `none` and `auto` correspond to the css properties, where `none` means that an object is not directly targetted and `auto` means the object is always targetted for events. The additional value `listener`, which is the default value, expresses that the object is only targetted by events if the object has any listeners. In 3D scenes this default is more reasonable than `auto`, which is the default in the web, because 3D scenes often contain semi-transparent content, such as particles, that should not catch pointer events by default.

In addition to the `pointerEvents` property, each 3D object can also filter events based on the `pointerType` with the `pointerEventsType` property. This property defaults to the value `all`, which expresses that pointer events from pointers of all types should be accepted. To filter specific pointer types, such as `screen-mouse`, which represents a normal mouse used through a 2D screen, `pointerEventsType` can be set to `{ allow: "screen-mouse" }` or `{ deny: "screen-touch" }`. `pointerEventsType`'s `allow` and `deny` accept strings and array of strings. In case more custom logic is needed, `pointerEventsType` also accepts a function. In general the pointer types `screen-touch`, `screen-pen`, `ray`, `grab`, and `touch` are used by default. For pointer events that were forwarded through a portal using `forwardObjectEvents`, their `pointerType` is prefixed with `forward-`, while events forwarded from the dom to the scene are prefixed with `screen-`.

## But wait ... there's more

Create your own `Pointer` that can, for example, allow to make first person controls interact with their environment by placing the pointer inside the camera or something else. These `Pointer` can use a normal `Ray` for intersection, or a set of `Lines`, or even a `Sphere`, for grab and touch events.

## Pitfalls

The `pointerEvents` attribute of any Mesh/Object3D/... will not be cloned when cloning the object.
