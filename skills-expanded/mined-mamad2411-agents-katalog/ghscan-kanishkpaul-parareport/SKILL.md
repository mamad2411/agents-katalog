# Multilingual Civic Analysis Skill

Use this workflow internally before producing the final JSON:

1. Detect language and script.
   - Bengali script: preserve meaning and produce Bengali share text in Bengali script.
   - Devanagari Hindi: produce Hindi share text in Devanagari.
   - Romanized Bengali/Hindi: infer the likely phrase but avoid overconfident translation of place names.
   - Mixed reports: use the civic issue facts, not the language mix, to classify severity.

2. Extract civic facts.
   - What is wrong?
   - Where is it?
   - Who is at risk?
   - Is it ongoing, seasonal, repeated, or urgent?
   - Is there water, electricity, fire, crowding, children, elderly people, school, clinic, market, wetlands, or traffic obstruction?

3. Pick the seasonal mode.
   - Monsoon flood/dengue: standing water, rain, blocked drains, mosquito breeding, hidden manholes, water plus wires.
   - Pujo safety: pandal, bamboo, crowd bottleneck, temporary wiring, exits, stalls, immersion routes.
   - Summer heat/water: no water, low pressure, tanker need, heat exposure, queue, broken public tap.
   - Winter air/dust: open burning, smoke, construction dust, road dust, fog or lighting visibility.
   - Wetlands watch: bheri, khal, canal, wetland filling, dumping, encroachment, industrial discharge.
   - Pre-monsoon storm prep: loose branches, hoardings, wires, desilting before rain, preventable wind/rain risk.
   - Everyday: routine civic issue when no seasonal risk dominates.

4. Set severity.
   - `critical`: immediate threat to life or injury, especially electricity with water, exposed live wire, fire, open manhole in floodwater, dangerous crowd crush, or blocked emergency route.
   - `high`: public health/safety risk affecting many people or vulnerable groups, dengue breeding near school/clinic, major waterlogging, serious obstruction, repeated unresolved hazard.
   - `medium`: actionable civic issue with localized risk.
   - `low`: minor inconvenience or cleanup request with no clear safety risk.

5. Produce grounded actions.
   - Citizen actions must be safe and realistic.
   - Volunteer actions can include verification, marking hazards, separating waste, confirming repeat reports, or escalating to ward-level contacts.
   - Never ask residents to touch wires, enter floodwater, confront offenders, climb structures, or clear hazardous material without authority.

6. Keep output schema valid.
   - Output only the JSON object.
   - Use exact enum values for `mode` and `severity`.
   - Prefer 2-5 items for arrays.
   - Never omit `volunteerActions`; if volunteers cannot fix the issue directly, ask them to verify, document, mark safe boundaries, check vulnerable residents, or coordinate escalation.
   - Never omit `citizenSafeActions`; if citizens cannot act directly, tell them how to avoid danger and what evidence to share safely.
