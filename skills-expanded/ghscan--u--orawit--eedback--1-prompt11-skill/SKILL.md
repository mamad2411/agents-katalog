# Prompt 11: Skill Popup (`components/popups/SkillPopup.tsx`)

## Goal
Replace the placeholder SkillPopup from prompt9 with full implementation.
2 tabs: Passive Skill / Active Skill.
Drag & Drop equip system + Skill information modal.

---

## Assets Used
- `../Resource/prompt11_skill/04_Main_Skill_Passive.png` — reference: Passive tab
- `../Resource/prompt11_skill/04_Main_Skill_Active.png` — reference: Active tab
- `../Resource/prompt11_skill/04_Main_Skill_Infomation.png` — reference: Skill info modal
- Skill icons: `../Resource/prompt11_skill/Skill/{skill-id}.png`
  - `Ignite.png`, `Capsule.png`, `Draw.png`, `Revive.png`
  - `Spark.png`, `Flow.png`, `Depth.png`, `Grace.png`

> ⚠️ FLAG: Skill icon filenames in Resource use **PascalCase** (e.g., `Ignite.png`) but code references use **lowercase** (e.g., `ignite.png`). Update code to use exact capitalized filenames.
> ⚠️ FLAG: Alternate `-2` icon variants (`ignite-2.png`, `capsule-2.png`, etc.) are **not found in Resource**.

---

## States Overview

```
SkillPopup
  ├── Tab: 'passive'     → Passive Skill tab
  ├── Tab: 'active'      → Active Skill tab
  └── selectedSkill      → Skill Information modal (overlay)
```

---

## Skill Data

```ts
// lib/skillData.ts

export interface SkillData {
  id: string
  name: string
  reference: string       // ทฤษฎีอ้างอิง
  type: 'passive' | 'active'
  description: string
  mbtiMatch: string[]
  price: number           // coins to equip
  evolutionChain: string[] // icon paths [current, next, '?']
}

export const skillList: SkillData[] = [
  // ── Active Skills ──
  {
    id: 'ignite',
    name: 'Ignite',
    reference: '5 Second Rule',
    type: 'active',
    description: 'กดแล้วนับถอยหลัง 5 วินาที บังคับสมองข้าม hesitation และเริ่ม task ทันที',
    mbtiMatch: ['ISFP', 'INFP', 'ESFP', 'ENFP'],
    price: 80,
    evolutionChain: [
      '../Resource/prompt11_skill/Skill/ignite.png',
      '../Resource/prompt11_skill/Skill/ignite-2.png',
      '?',
    ],
  },
  {
    id: 'capsule',
    name: 'Capsule',
    reference: "Parkinson's Law",
    type: 'active',
    description: 'ล็อก deadline +30 นาทีให้ task อัตโนมัติ บังคับให้โฟกัสและทำให้เสร็จใน window ที่จำกัด',
    mbtiMatch: ['INTJ', 'INTP', 'ENTJ', 'ENTP'],
    price: 80,
    evolutionChain: [
      '../Resource/prompt11_skill/Skill/capsule.png',
      '../Resource/prompt11_skill/Skill/capsule-2.png',
      '?',
    ],
  },
  {
    id: 'draw',
    name: 'Draw',
    reference: 'Decision Fatigue Research',
    type: 'active',
    description: 'สุ่ม 1 task จาก list ตัดวงจรเลือกไม่ได้ และเริ่มทำได้ทันทีโดยไม่ต้องคิด',
    mbtiMatch: ['ISTP', 'ISFP', 'ESTP', 'ESFP'],
    price: 60,
    evolutionChain: [
      '../Resource/prompt11_skill/Skill/draw.png',
      '../Resource/prompt11_skill/Skill/draw-2.png',
      '?',
    ],
  },
  {
    id: 'revive',
    name: 'Revive',
    reference: 'Re-engagement Design',
    type: 'active',
    description: 'ป้องกัน streak พังหลังหายไป >3 วัน แสดง Welcome back แทน penalty เพื่อดึงกลับมา',
    mbtiMatch: ['INFP', 'ISFP', 'ENFP', 'ESFP'],
    price: 100,
    evolutionChain: [
      '../Resource/prompt11_skill/Skill/revive.png',
      '../Resource/prompt11_skill/Skill/revive-2.png',
      '?',
    ],
  },

  // ── Passive Skills ──
  {
    id: 'spark',
    name: 'Spark',
    reference: 'Immediate Reinforcement',
    type: 'passive',
    description: 'ให้ XP พร้อม animation ทันทีที่ tick task ทุกครั้ง สร้าง dopamine loop ให้อยากทำต่อ',
    mbtiMatch: ['ESFP', 'ENFP', 'ESTP', 'ENTP'],
    price: 50,
    evolutionChain: [
      '../Resource/prompt11_skill/Skill/spark.png',
      '../Resource/prompt11_skill/Skill/spark-2.png',
      '?',
    ],
  },
  {
    id: 'flow',
    name: 'Flow',
    reference: 'Behavioral Momentum',
    type: 'passive',
    description: 'ทำ task ต่อกัน 2+ อัน XP multiplier stack ขึ้นเรื่อยๆ หยุดแล้ว reset สร้าง momentum ให้ทำต่อเนื่อง',
    mbtiMatch: ['ENTJ', 'ESTJ', 'ENFJ', 'ESFJ'],
    price: 50,
    evolutionChain: [
      '../Resource/prompt11_skill/Skill/flow.png',
      '../Resource/prompt11_skill/Skill/flow-2.png',
      '?',
    ],
  },
  {
    id: 'depth',
    name: 'Depth',
    reference: 'Delayed Gratification',
    type: 'passive',
    description: 'task นานกว่า 1 ชม. ได้ XP ×1.5 อัตโนมัติ reward คนที่กล้าลงทุนกับงานยากและลึก',
    mbtiMatch: ['INTJ', 'INTP', 'INFJ', 'ISTJ'],
    price: 50,
    evolutionChain: [
      '../Resource/prompt11_skill/Skill/depth.png',
      '../Resource/prompt11_skill/Skill/depth-2.png',
      '?',
    ],
  },
  {
    id: 'grace',
    name: 'Grace',
    reference: 'Self-compassion — Kristin Neff',
    type: 'passive',
    description: 'พลาด streak ไม่โดน penalty แต่ได้ Fresh Start badge แทน ลบ guilt loop ที่ทำให้คนเลิกใช้ app',
    mbtiMatch: ['INFJ', 'INFP', 'ISFJ', 'ISFP'],
    price: 50,
    evolutionChain: [
      '../Resource/prompt11_skill/Skill/grace.png',
      '../Resource/prompt11_skill/Skill/grace-2.png',
      '?',
    ],
  },
]
```

---

## Zustand Store Update

```ts
// store/useSkillStore.ts
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface SkillState {
  // Owned skills (bought with coins)
  ownedSkills: string[]       // skill ids

  // Passive slots (max 3, unlock by streak)
  passiveSlots: (string | null)[]  // [skillId | null, skillId | null, skillId | null]

  // Active skills equipped
  activeEquipped: string[]    // skill ids currently active

  buySkill: (skillId: string) => void
  equipPassive: (skillId: string, slotIndex: number) => void
  unequipPassive: (slotIndex: number) => void
  equipActive: (skillId: string) => void
  unequipActive: (skillId: string) => void
  getUnlockedPassiveSlots: (streak: number) => number
}

export const useSkillStore = create<SkillState>()(
  persist(
    (set, get) => ({
      ownedSkills: [],
      passiveSlots: [null, null, null],
      activeEquipped: [],

      buySkill: (skillId) => set(state => ({
        ownedSkills: state.ownedSkills.includes(skillId)
          ? state.ownedSkills
          : [...state.ownedSkills, skillId]
      })),

      equipPassive: (skillId, slotIndex) => set(state => {
        const slots = [...state.passiveSlots]
        slots[slotIndex] = skillId
        return { passiveSlots: slots }
      }),

      unequipPassive: (slotIndex) => set(state => {
        const slots = [...state.passiveSlots]
        slots[slotIndex] = null
        return { passiveSlots: slots }
      }),

      equipActive: (skillId) => set(state => ({
        activeEquipped: state.activeEquipped.includes(skillId)
          ? state.activeEquipped
          : [...state.activeEquipped, skillId]
      })),

      unequipActive: (skillId) => set(state => ({
        activeEquipped: state.activeEquipped.filter(id => id !== skillId)
      })),

      // Slot 1 = always unlocked
      // Slot 2 = unlock at streak 7
      // Slot 3 = unlock at streak 14
      getUnlockedPassiveSlots: (streak) => {
        if (streak >= 14) return 3
        if (streak >= 7) return 2
        return 1
      },
    }),
    { name: 'skill-store' }
  )
)
```

---

## Implementation

```tsx
// components/popups/SkillPopup.tsx
'use client'

import { useState } from 'react'
import Image from 'next/image'
import { DragDropContext, Droppable, Draggable, DropResult } from '@hello-pangea/dnd'
import { skillList, SkillData } from '@/lib/skillData'
import { useSkillStore } from '@/store/useSkillStore'
import { useUserStore } from '@/store/useUserStore'
import { useTaskStore } from '@/store/useTaskStore'

type TabType = 'passive' | 'active'

interface SkillPopupProps {
  onClose: () => void
}

export default function SkillPopup({ onClose }: SkillPopupProps) {
  const [activeTab, setActiveTab] = useState<TabType>('passive')
  const [selectedSkill, setSelectedSkill] = useState<SkillData | null>(null)

  const { profile, addCoins } = useUserStore()
  const {
    ownedSkills, passiveSlots, activeEquipped,
    buySkill, equipPassive, unequipPassive,
    equipActive, getUnlockedPassiveSlots,
  } = useSkillStore()
  const { tasks } = useTaskStore()

  const streak = profile?.streak ?? 0
  const coins = profile?.coins ?? 0
  const unlockedSlots = getUnlockedPassiveSlots(streak)

  const passiveSkills = skillList.filter(s => s.type === 'passive')
  const activeSkills = skillList.filter(s => s.type === 'active')
  const incompleteTasks = tasks.filter(t => !t.completed)

  // ── Equip passive via drag ──
  const handlePassiveDragEnd = (result: DropResult) => {
    if (!result.destination) return
    const skillId = result.draggableId
    const slotIndex = parseInt(result.destination.droppableId.replace('slot-', ''))
    if (isNaN(slotIndex)) return
    if (slotIndex >= unlockedSlots) return  // slot locked
    if (!ownedSkills.includes(skillId)) return  // not owned
    equipPassive(skillId, slotIndex)
  }

  // ── Buy + Equip skill ──
  const handleEquip = (skill: SkillData) => {
    if (!ownedSkills.includes(skill.id)) {
      // Buy first
      if (coins < skill.price) return  // not enough coins
      addCoins(-skill.price)
      buySkill(skill.id)
    }
    if (skill.type === 'active') {
      equipActive(skill.id)
    }
    setSelectedSkill(null)
  }

  // ────────────────────────────
  // RENDER: Skill Information Modal
  // ────────────────────────────
  if (selectedSkill) {
    const isOwned = ownedSkills.includes(selectedSkill.id)
    const canAfford = coins >= selectedSkill.price

    return (
      <div className="p-4">
        {/* Back */}
        <button
          onClick={() => setSelectedSkill(null)}
          className="font-pixel text-[10px] text-gray-400 hover:text-brand-pink mb-4 block"
        >
          ← Back
        </button>

        {/* Tab header (same style) */}
        <div className="flex border-b border-gray-100 mb-4">
          <div className="px-4 py-2 font-pixel text-sm text-gray-400">
            {selectedSkill.type === 'passive' ? 'Passive Skill' : 'Active Skill'}
          </div>
          <div className="px-4 py-2 font-pixel text-sm text-brand-pink border-b-2 border-brand-pink">
            {selectedSkill.type === 'passive' ? 'Passive Skill' : 'Active Skill'}
          </div>
        </div>

        {/* Evolution Chain */}
        {/* ⚠️ Coming Soon — no upgrade logic yet */}
        <div className="flex items-center justify-center gap-3 mb-4">
          {selectedSkill.evolutionChain.map((src, i) => (
            <div key={i} className="flex items-center gap-2">
              <div className="w-16 h-16 rounded-2xl border-2 border-gray-200
                flex items-center justify-center bg-pink-50">
                {src === '?' ? (
                  <span className="font-pixel text-2xl text-gray-300">?</span>
                ) : (
                  <Image
                    src={src}
                    alt={`evolution-${i}`}
                    width={48}
                    height={48}
                    className="object-contain"
                    onError={(e) => { e.currentTarget.style.display = 'none' }}
                  />
                )}
              </div>
              {i < selectedSkill.evolutionChain.length - 1 && (
                <span className="text-gray-300 text-lg">→</span>
              )}
            </div>
          ))}
        </div>

        {/* Skill name */}
        <h2 className="font-pixel text-lg text-gray-800 text-center mb-1">
          {selectedSkill.name}
        </h2>

        {/* Description */}
        <p className="font-thai text-sm text-gray-600 text-center leading-relaxed mb-3 px-2">
          {selectedSkill.description}
        </p>

        {/* Example button — placeholder */}
        <div className="flex justify-center mb-3">
          <button className="border border-gray-200 rounded-full px-6 py-2
            font-pixel text-xs text-gray-500 hover:border-brand-pink hover:text-brand-pink
            transition-colors">
            Example
          </button>
        </div>

        {/* MBTI tags */}
        <p className="font-pixel text-[10px] text-gray-400 text-center mb-6">
          {selectedSkill.mbtiMatch.join(' / ')}
        </p>

        {/* Equip button */}
        <button
          onClick={() => handleEquip(selectedSkill)}
          disabled={!canAfford && !isOwned}
          className={`
            w-full py-4 rounded-full font-pixel text-sm
            flex items-center justify-center gap-2
            transition-all active:scale-95
            ${isOwned
              ? 'bg-brand-mint text-white'
              : canAfford
                ? 'bg-white border-2 border-gray-200 text-gray-700 hover:border-brand-pink'
                : 'bg-gray-100 text-gray-300 cursor-not-allowed'}
          `}
        >
          {isOwned ? (
            <>Equipped ✓</>
          ) : (
            <>
              Equip | {selectedSkill.price}
              <span className="text-base">💰</span>
            </>
          )}
        </button>

        {!canAfford && !isOwned && (
          <p className="font-pixel text-[9px] text-red-400 text-center mt-2">
            coins ไม่พอ (มี {coins} / ต้องการ {selectedSkill.price})
          </p>
        )}
      </div>
    )
  }

  // ────────────────────────────
  // RENDER: Main Popup
  // ────────────────────────────
  return (
    <div className="flex flex-col max-h-[80vh]">

      {/* Tabs */}
      <div className="flex border-b border-gray-100 flex-shrink-0">
        <button
          onClick={() => setActiveTab('passive')}
          className={`flex-1 py-3 font-pixel text-sm transition-colors
            ${activeTab === 'passive'
              ? 'text-brand-pink border-b-2 border-brand-pink'
              : 'text-gray-400'}`}
        >
          Passive Skill
        </button>
        <button
          onClick={() => setActiveTab('active')}
          className={`flex-1 py-3 font-pixel text-sm transition-colors
            ${activeTab === 'active'
              ? 'text-brand-pink border-b-2 border-brand-pink'
              : 'text-gray-400'}`}
        >
          Active Skill
        </button>
      </div>

      <div className="flex-1 overflow-y-auto">

        {/* ── PASSIVE TAB ── */}
        {activeTab === 'passive' && (
          <DragDropContext onDragEnd={handlePassiveDragEnd}>
            <div className="p-4">

              {/* Passive Slots (top) — Drop targets */}
              <div className="flex gap-3 mb-4">
                {[0, 1, 2].map(slotIndex => {
                  const isUnlocked = slotIndex < unlockedSlots
                  const equippedId = passiveSlots[slotIndex]
                  const equippedSkill = equippedId
                    ? skillList.find(s => s.id === equippedId)
                    : null
                  const lockStreakRequired = slotIndex === 1 ? 7 : 14

                  return (
                    <Droppable
                      key={slotIndex}
                      droppableId={`slot-${slotIndex}`}
                      isDropDisabled={!isUnlocked}
                    >
                      {(provided, snapshot) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.droppableProps}
                          className={`
                            flex-1 h-20 rounded-2xl border-2 flex flex-col
                            items-center justify-center gap-1 transition-colors
                            ${snapshot.isDraggingOver && isUnlocked
                              ? 'border-brand-pink bg-pink-50'
                              : isUnlocked
                                ? 'border-gray-200 bg-white'
                                : 'border-gray-100 bg-gray-50'}
                          `}
                          onClick={() => !isUnlocked && null}
                        >
                          {!isUnlocked ? (
                            // Locked slot
                            <>
                              <span className="text-2xl">🔒</span>
                              <span className="font-pixel text-[9px] text-gray-400">
                                {lockStreakRequired}🔥
                              </span>
                            </>
                          ) : equippedSkill ? (
                            // Equipped skill
                            <div className="relative">
                              <Image
                                src={`../Resource/prompt11_skill/Skill/${equippedSkill.id}.png`}
                                alt={equippedSkill.name}
                                width={40}
                                height={40}
                                className="object-contain"
                                onError={(e) => { e.currentTarget.style.display = 'none' }}
                              />
                              <button
                                onClick={() => unequipPassive(slotIndex)}
                                className="absolute -top-1 -right-1 w-4 h-4 bg-gray-400
                                  rounded-full text-white text-[8px] flex items-center justify-center"
                              >
                                ✕
                              </button>
                            </div>
                          ) : (
                            // Empty slot
                            <span className="font-pixel text-[9px] text-gray-300">
                              Empty Slot
                            </span>
                          )}
                          {provided.placeholder}
                        </div>
                      )}
                    </Droppable>
                  )
                })}
              </div>

              {/* How to use + filter */}
              <div className="flex items-center justify-between mb-3">
                <button className="font-pixel text-[10px] text-gray-400 flex items-center gap-1">
                  How to use <span className="text-base">?</span>
                </button>
                <button className="text-gray-400">
                  <span className="text-lg">≡</span>
                </button>
              </div>

              {/* Skill Grid 3×3 — Draggable */}
              <div className="grid grid-cols-3 gap-2">
                {Array.from({ length: 9 }).map((_, i) => {
                  const skill = passiveSkills[i]
                  const isOwned = skill ? ownedSkills.includes(skill.id) : false

                  if (!skill) {
                    // Empty locked slot in grid
                    return (
                      <div key={i} className="aspect-square rounded-2xl border border-gray-100 bg-gray-50" />
                    )
                  }

                  return (
                    <Draggable
                      key={skill.id}
                      draggableId={skill.id}
                      index={i}
                      isDragDisabled={!isOwned}
                    >
                      {(provided, snapshot) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          className={`
                            aspect-square rounded-2xl border flex flex-col
                            items-center justify-center gap-1 cursor-pointer
                            transition-all
                            ${snapshot.isDragging ? 'shadow-lg scale-105 z-50' : ''}
                            ${isOwned
                              ? 'border-gray-200 bg-white hover:border-brand-pink'
                              : 'border-gray-100 bg-pink-50/30'}
                          `}
                          onClick={() => setSelectedSkill(skill)}
                        >
                          <div className="relative">
                            <Image
                              src={`../Resource/prompt11_skill/Skill/${skill.id}.png`}
                              alt={skill.name}
                              width={40}
                              height={40}
                              className={`object-contain ${!isOwned ? 'opacity-40' : ''}`}
                              onError={(e) => {
                                e.currentTarget.style.display = 'none'
                              }}
                            />
                            {/* Price badge if not owned */}
                            {!isOwned && (
                              <span className="absolute -top-1 -right-1 bg-yellow-400
                                text-[8px] font-pixel text-white rounded-full px-1">
                                {skill.price}💰
                              </span>
                            )}
                          </div>
                          <span className="font-pixel text-[9px] text-gray-600">
                            {skill.name}
                          </span>
                        </div>
                      )}
                    </Draggable>
                  )
                })}
              </div>

            </div>
          </DragDropContext>
        )}

        {/* ── ACTIVE TAB ── */}
        {activeTab === 'active' && (
          <div className="p-4">

            {/* Task list (scrollable, draggable for priority) */}
            <div className="mb-4 max-h-[140px] overflow-y-auto border border-gray-100 rounded-2xl">
              {incompleteTasks.length === 0 ? (
                <p className="font-pixel text-[10px] text-gray-300 text-center py-4">
                  ไม่มี Task ที่ค้างอยู่
                </p>
              ) : (
                incompleteTasks.map((task, index) => (
                  <div
                    key={task.id}
                    className="flex items-center gap-3 px-3 py-2.5 border-b border-gray-50 last:border-0"
                  >
                    <div className="w-10 h-10 rounded-xl border border-gray-200 bg-gray-50 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="font-pixel text-xs text-gray-700 truncate">
                        #{index + 1} | {task.title}
                      </p>
                      {task.subtitle && (
                        <p className="font-thai text-[10px] text-gray-400 truncate">
                          {task.subtitle}
                        </p>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* How to use + filter */}
            <div className="flex items-center justify-between mb-3">
              <button className="font-pixel text-[10px] text-gray-400 flex items-center gap-1">
                How to use <span className="text-base">?</span>
              </button>
              <button className="text-gray-400">
                <span className="text-lg">≡</span>
              </button>
            </div>

            {/* Active Skill Grid 3×3 */}
            <div className="grid grid-cols-3 gap-2">
              {Array.from({ length: 9 }).map((_, i) => {
                const skill = activeSkills[i]
                const isOwned = skill ? ownedSkills.includes(skill.id) : false
                const isEquipped = skill ? activeEquipped.includes(skill.id) : false

                if (!skill) {
                  return (
                    <div key={i} className="aspect-square rounded-2xl border border-gray-100 bg-gray-50" />
                  )
                }

                return (
                  <div
                    key={skill.id}
                    className={`
                      aspect-square rounded-2xl border flex flex-col
                      items-center justify-center gap-1 cursor-pointer
                      transition-all hover:scale-105
                      ${isEquipped
                        ? 'border-brand-pink bg-pink-50 shadow-md'
                        : isOwned
                          ? 'border-gray-200 bg-white hover:border-brand-pink'
                          : 'border-gray-100 bg-pink-50/30'}
                    `}
                    onClick={() => setSelectedSkill(skill)}
                  >
                    <div className="relative">
                      <Image
                        src={`../Resource/prompt11_skill/Skill/${skill.id}.png`}
                        alt={skill.name}
                        width={40}
                        height={40}
                        className={`object-contain ${!isOwned ? 'opacity-40' : ''}`}
                        onError={(e) => { e.currentTarget.style.display = 'none' }}
                      />
                      {/* Stack count badge if equipped */}
                      {isEquipped && (
                        <span className="absolute -top-1 -right-1 w-5 h-5 bg-yellow-400
                          rounded-full text-[9px] font-pixel text-white
                          flex items-center justify-center">
                          5
                        </span>
                      )}
                      {/* Price badge if not owned */}
                      {!isOwned && (
                        <span className="absolute -top-1 -right-1 bg-yellow-400
                          text-[8px] font-pixel text-white rounded-full px-1">
                          {skill.price}💰
                        </span>
                      )}
                    </div>
                    <span className="font-pixel text-[9px] text-gray-600">
                      {skill.name}
                    </span>
                  </div>
                )
              })}
            </div>

          </div>
        )}
      </div>
    </div>
  )
}
```

---

## Behavior Summary

| Interaction | Action |
|-------------|--------|
| กด tab Passive | แสดง passive slots + skill grid |
| กด tab Active | แสดง task list + active skill grid |
| กด skill card | เปิด Skill Information modal |
| กด Equip (มี coins) | หัก coins → add to ownedSkills → equip |
| กด Equip (ไม่มี coins) | disabled + แสดง error |
| Drag passive skill → slot | equipPassive (ต้อง owned + slot unlocked) |
| Slot 🔒 | แสดง streak requirement |
| กด ✕ บน equipped slot | unequipPassive |
| Evolution chain | แสดง visual only, "Coming Soon" |

---

## Files to Edit (Quick Reference)
| What to change | Where |
|----------------|-------|
| ราคา skill | `lib/skillData.ts` → field `price` |
| คำอธิบาย skill | `lib/skillData.ts` → field `description` |
| MBTI ที่เหมาะ | `lib/skillData.ts` → field `mbtiMatch` |
| Passive slot unlock threshold | `store/useSkillStore.ts` → `getUnlockedPassiveSlots()` |
| Skill icons | `../Resource/prompt11_skill/Skill/{skill-id}.png` |

---

## Edge Cases
- **Skill image missing**: hidden gracefully (`onError`)
- **ไม่มี coins**: Equip button disabled + แสดง error message
- **Drag ไปยัง locked slot**: `isDropDisabled={true}` ใน Droppable
- **Drag skill ที่ยังไม่ได้ซื้อ**: `isDragDisabled={true}` ใน Draggable
- **Slot 2-3 ยังล็อก**: แสดง 🔒 + streak requirement
