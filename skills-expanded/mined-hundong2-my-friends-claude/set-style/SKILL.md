# set-style

Change the active output style for my-friends-claude plugin.

## Usage
`/my-friends-claude:set-style [style-name]`

Available styles: `friendly-korean`, `concise`, `mentor`

## Instructions

When this skill is invoked:

1. If a style name is provided as an argument, update `config/config.json` field `activeStyle` to the given style name
2. If no argument is provided, list available styles and ask the user to choose
3. After updating, confirm the change

Available styles:
- **friendly-korean**: 친구같은 한국어 스타일 (반말, 이모지, 친근한 톤)
- **concise**: 간결한 스타일 (존댓말, 핵심만 전달, 이모지 없음)
- **mentor**: 멘토 스타일 (존댓말, 설명 중심, 학습 유도)

Read the selected style file from `styles/` directory and apply it as the current output style.

Update `config/config.json` by changing the `activeStyle` field to the chosen style name using the Edit tool.

Confirm to the user: "스타일이 [style-name]으로 변경되었습니다!" (or equivalent in the active language).
