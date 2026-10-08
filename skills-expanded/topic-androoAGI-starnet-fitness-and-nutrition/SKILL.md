---
name: fitness-and-nutrition
description: "Build a weekly training and eating plan for a goal you name, keep a log of sessions and body weight, and adjust the plan from the log. General information only, not medical advice."
license: MIT
metadata:
  title: "Fitness and Nutrition"
  category: "Planning"
  author: "StarNet"
---

Plan training and eating for one stated goal, then let the log steer it. The bar: a plan the Commander can follow this week with the time and equipment they really have, numbers whose arithmetic is shown, and no advice that belongs to a doctor.

## Method
1. **Screen before you plan.** Ask plainly: any pain or injury, recent surgery, a diagnosed condition (heart, blood pressure, diabetes, other), medication that affects exercise or appetite, pregnancy or a recent birth, a history of disordered eating, or under 18? For any yes, stop the part it touches and say which professional to see (doctor, physiotherapist, registered dietitian). Plan only inside what that professional has cleared.
2. **Collect the basics.** One main goal (lose fat, gain muscle, get stronger, finish an event, general health) and a date if there is one. Training history. Days per week and minutes per session. Equipment. Movements and foods they like, dislike or cannot have; allergies; budget and cooking time. Age, height, weight and sex, only for the energy formula. Sleep and how active the working day is. Ask; do not assume.
3. **Estimate energy with a named formula and show the sums.** Use Mifflin-St Jeor in `code.run` and print each line: resting energy = 10 × kg + 6.25 × cm − 5 × age, then + 5 for men or − 161 for women. Daily maintenance = resting energy × an activity factor: 1.2 mostly sitting, 1.375 light activity, 1.55 moderate, 1.725 very active. Say it is an estimate that can miss by ten percent or more; the log corrects it.
4. **Set a modest target.** Fat loss: 10 to 20 percent under maintenance, aiming at roughly half a percent of body weight a week. Muscle gain: 5 to 10 percent over. Otherwise maintenance. Protein: people who train commonly use 1.2 to 2.0 g per kg of body weight a day; pick a figure their normal food can reach. Build the day from meals they already eat, with vegetables, fibre and water, and offer portions instead of numbers if they prefer.
5. **Build the week.** Fit the days they have. Each session: a warm-up, four to six exercises, sets × reps, how hard (stop one to three reps before failure), rest, and total minutes. Across the week cover push, pull, squat, hinge and trunk. A beginner starts with two or three full-body days. Work toward the World Health Organization baseline of 150 minutes of moderate activity a week. Keep at least one full rest day, and give a swap for every exercise that needs equipment or bothers a joint.
6. **Write the overload rule into the plan.** When every set reaches the top of its rep range with good form at the target effort, add the smallest load step next time; otherwise repeat the session. Change one thing at a time, raise weekly volume by about ten percent at most, and plan a lighter week every four to eight weeks.
7. **Save the plan and start the log.** `fs.write` the plan to `fitness/plan.md`. Log with `fs.append`: `fitness/log.csv` (date, session, exercise, sets, reps, load, effort 1-10, notes) and `fitness/weight.csv` (date, weight). Read each entry back after writing.
8. **Adjust from the log, never from a guess.** At least two weeks apart: compute weekly average weight and each lift's trend in `code.run`. Move calories in steps of 100 to 200 only when two weeks agree. Change a lift's plan after it stalls three sessions running. Poor sleep, soreness and falling numbers together mean less work, not more. No log, no change: ask for the data.

## Rules
- **General information, not medical advice.** Say so once, plainly, in the plan. Never diagnose, and never promise a result.
- **Stop and send them to a professional for:** pain during or after exercise, an injury, pregnancy, any medical condition, or signs of an eating disorder (fear of eating, bingeing or purging, fast weight loss, missed periods, exercising to "earn" food, asking for very low intake). For those signs give no deficit plan; answer kindly and suggest a doctor or an eating-disorder helpline. Chest pain, fainting or severe breathlessness: tell them to seek urgent care now.
- **No extreme deficits.** Never plan intake below the estimated resting energy, and never below 1,200 kcal a day for women or 1,500 for men. No crash diets, no long fasts, no cutting water, no "detox".
- **No supplement or drug dosing.** No amounts for supplements, stimulants, hormones, weight-loss medication or any medicine. That question goes to a doctor or pharmacist.
- **Under 18: activity and ordinary balanced eating only.** No deficit, no body-weight targets; point to a parent and a doctor.
- Neutral words about bodies. No shame, no moral labels on food.
- Health details are private: keep them in the plan files, out of any message sent to a channel.

## Done means
The plan file exists and reads back; it shows the screening answers, the formula with its arithmetic, the weekly sessions, the overload rule and the limits above; the log files are in place; and any adjustment quotes the log lines it came from.

## Output
`fitness/plan.md` named with `deliverable_note`, the energy estimate with its sums, this week's sessions, what to log, and the date of the next review. When something was out of bounds: what was not planned and who to see.

*Needs the INTEL CAB (fs.write, fs.append, fs.read). code.run and deliverable_note are available to every agent.*
