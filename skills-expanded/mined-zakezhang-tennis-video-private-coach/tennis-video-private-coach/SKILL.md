---
name: tennis-video-private-coach
description: Review a tennis practice video and produce a coaching report. Detects every swing, separates forehands and backhands, picks the best and worst shots and renders annotated slow-motion clips with the swing path drawn on the player, counts net/out when the ball is visible, checks knees and footwork, compares with past sessions, and writes a concrete plan for the next practice. Use when someone uploads a practice video, asks for a session review, or asks what to practice next.
---

# Tennis Video Private Coach

Turn an amateur player's practice video into a review they can act on: **which part of the stroke breaks down, which shots prove it, and exactly what to practice next**. Built for beginner to intermediate players hitting against a wall, a ball machine, a coach, or a hitting partner.

Requirements: an environment that can run Python 3 and ffmpeg and install pip packages (ultralytics, opencv-python, numpy, scipy, Pillow). A GPU helps but is not needed.

## 0. Ask first (only what you don't already know)

1. **Which person in the frame is the player**: clothing colors, hair, position. Coaches, partners and people on the next court are often in shot.
2. **Dominant hand**, and whether the backhand is **one-handed or two-handed** (or both, while learning).
3. **Level and goal**: how long they have played and what they want to reach (for example, "rally and play a set by year end").
4. **Setting**: practice wall / ball machine / coach feeding / rallying; indoor or outdoor.
5. **Camera**: behind, side or front; phone height; frame rate.
6. **Injuries**: recent soreness in knees, shoulder, elbow or back. If so, footwork and landings get extra attention.
7. **The one problem they most want solved** (for example, "lots of balls fly long" or "my contact point is inconsistent"). The report must answer it at the top.
8. **Previous reports**, if any, for comparison.

## 1. What the report must do

- **Lead with the conclusion.** One sentence on the biggest problem and the biggest improvement, then the detail. Be specific and back every criticism with evidence; don't only praise. If a previous review got something wrong, say so explicitly.
- **Back every claim with video.** Each case gets an annotated slow-motion clip, drawn on the player's real footage, not a stick-figure animation.
- **Default to 4 categories × 3 shots**: best forehands, worst forehands, best backhands, worst backhands (12 clips). Each category gets a 3-column comparison table and one sentence on what the three shots have in common. If a category has fewer than 3 usable shots, say how many were found.
- **Keep one-handed and two-handed backhands apart.** If the player is practicing both, one-handers get their own section and are excluded from two-hander statistics.
- **Name the broken phase**: take-back / racket drop / contact point / follow-through direction / footwork / preparation timing / handling high balls / forehand-backhand decision.
- **Always check knees and footwork**: hitting while airborne, landing on one leg, pivoting on a locked straight leg.
- **State the limits of the data**: sample size, how many shots were unreadable, camera-angle bias. If something can't be seen, say so instead of guessing a number.
- **End with a plan they can follow**: 2–4 drills with reps or minutes, plus the condition for moving to the next stage.

## 2. Pipeline

### 2.1 Transcode and extract audio

- 4K HEVC phone footage is heavy. Make a 960-wide H.264 analysis copy:
  `ffmpeg -i IN.MOV -vf scale=960:-2 -r 30 -an -c:v libx264 -preset veryfast -crf 24 p.mp4`
  (Some phones record 29.97 fps; forcing 30 keeps time conversions simple.)
- Extract audio separately to locate contact:
  `ffmpeg -i IN.MOV -vn -ac 1 -ar 22050 a.wav`
- Process long videos in 4–5 minute chunks to avoid timeouts. For many short clips, grab one frame from each into an overview sheet first, and decide which clips are usable behind-the-player angles and which are too far away (use those only to look at technique).
- For practice-wall sessions, also crop a zoomed "wall" copy around the net line to judge net/out.

### 2.2 Pose estimation

- Use an Ultralytics YOLO pose model (`yolo11n-pose.pt`; `yolo11m-pose.pt` for more accuracy). Indoors, every 4th frame at imgsz 640, conf 0.3 is enough. Outdoors, where people are smaller and more numerous, use every 2nd frame, imgsz 960, conf 0.25.
- **Track the right person.** With one person in frame, take the largest box. With coaches or others around, score each detection by clothing: median HSV brightness and saturation inside the torso polygon (shoulders + hips), and the color of the hip-to-knee region for shorts/pants. Add a penalty for jumping far from the previous frame so the track doesn't switch people.
- **Decide left and right by image x-coordinate**, not the model's left/right labels. From behind, the player's right side is the right side of the image.

### 2.3 Find every swing

- A swing is a peak in wrist speed: frame-to-frame displacement of whichever wrist moves more, divided by box height, smoothed over 2 samples, threshold about 0.16 (for every-4th-frame sampling; scale down for denser sampling).
- **Require at least 1.6 s between peaks.** A 1.0 s gap counts the recovery after the follow-through as a second swing. Normal rhythm is one swing every 3–4 s.
- **Forehand or backhand**: in the window from 1.1 s to 0.25 s before the peak, which side of the hip midline the midpoint of both hands is on. The dominant-hand side means forehand. A few will be wrong; confirm frame by frame for any shot you feature.
- Anchor every metric below to the wrist-speed peak (call it tp) so sessions stay comparable.

### 2.4 Locate contact from sound

- High-pass at 1500 Hz; compute an energy envelope over 110-sample windows; find peaks at least 10 dB above the median of the surrounding 401 windows and at least 50 windows apart.
- **Convert to seconds with `window_index × 110 / 22050`.** Multiplying by 0.005 as a shortcut drifts about half a second every 4 minutes and ruins the second half of long videos.
- Practice wall: take the loudest peak at least 15 dB above background within [tp−0.1, tp+0.55] s, usually 0.2–0.35 s after tp. The ball hitting the wall about 0.45 s after contact is also loud; don't pick it.
- Outdoors: the coach's shots and other courts add noise. Search [tp−0.45, tp+0.25] s; if nothing qualifies, use tp.
- For every shot that ends up in a clip, confirm the real contact frame by looking at the frames.

### 2.5 Detect one-handed backhands (if the player is learning one)

- Among backhands, take the maximum wrist-to-wrist distance (divided by torso length) within 0.7 s after tp. Two-handers keep both hands together through the finish (usually under 1.5); one-handers open the non-hitting arm back (usually 2.0–2.5). The gap is clear; a threshold around 1.95 works.
- Close camera angles produce false positives; confirm every candidate visually.
- For each one-hander, record: whether the hand goes above the head on the take-back, whether the take-back is late (set up like a two-hander, then pulled up at the last moment), whether the arm is straight at contact, follow-through height, and the result.
- One-hander checklist (for each item: what correct looks like / this session / verdict): unit turn with the off hand on the throat, take-back height between chest and shoulder with the racket head pointing back, racket drops low then swings low-to-high, contact in front with a straight arm, off arm opens backward, finish high and held without the chest squaring early, knees bent and stepping in. Grip can't be seen from behind; suggest the player confirm it with a coach.

### 2.6 Net / out counting (only when the ball is visible)

- **Practice wall**: mark the net line in the zoomed wall video. For each shot, make one tile: moving yellow blobs over the 30 frames after contact, plotted red→green by time, plus motion of the curtain above the net line in a second color. Judge each tile by eye: curtain moves or ball hits above the line = in; ball hits the board and the curtain doesn't move = net; blocked by the player = unreadable. Fully automatic judging agrees with a human only about 60% of the time, so use it as a hint only.
- **Sampling**: judge 100 shots spread evenly across the session, exclude unreadable ones, and report forehand / two-hander / one-hander separately. Then review the 20 most suspicious remaining shots to see whether errors cluster in one period (usually after fatigue sets in).
- **Outdoors**: with trees moving in the background or many players around, color-and-motion ball detection mostly fails. Don't report a percentage. Say why in the report, pick best/worst by technique instead, and give camera advice that would make counting possible.

### 2.7 Technique metrics (measured on every swing)

| Metric | How | What it reveals |
|---|---|---|
| Forehand hand above nose | Share of frames in [tp−1.1, tp−0.25] with the hitting wrist above the nose | Take-back too high, loopy swing |
| Both hands above shoulders | Share of the same window with both wrists above shoulder center | Backhand racket held up too high |
| Deepest knee bend | Minimum hip-knee-ankle angle of the front-side leg in [tp−0.6, tp+0.3], median across swings | Legs too straight (a camera behind underestimates forward flexion; compare only with yourself) |
| Stance width | Horizontal ankle distance at tp ÷ torso length | Narrow stance often goes with hopping |
| Planted and straight | One ankle moves less than 0.4 torso lengths within 0.7 s after tp, and that knee is straighter than 155° | Twisting load on the knee (common when pivoting on backhands) |
| Contact height | Hitting hand position between hip (0) and shoulder (1), 0.07–0.2 s before tp | How many balls are high and whether the player adjusts position |
| Hopping / one-leg landing | Counted by eye on the shots you review frame by frame | No reliable automatic metric yet |

- For long sessions, report the first and second halves separately to see what breaks down with fatigue.
- If the camera, venue or method changes, either re-measure old videos the new way or say clearly that numbers aren't comparable.

### 2.8 Choose 3 best and 3 worst

- **Best**: good result (clears the net comfortably, lands deep) and a complete stroke (take-back in position, racket head drops below the ball, full finish, both feet on the ground). Spread them across the session.
- **Worst**: net, sky balls or clear errors; if there aren't enough, take the shots where the technical fault is clearest. Prefer shots that show different causes, or that together prove one common cause.
- Shortlist from the result tiles, then confirm the cause from per-frame player sheets (0.9 s before to 0.5 s after contact). When picking the worst backhands, make sure they aren't one-handers.

### 2.9 Render annotated slow-motion clips

- Cut about 3 s from the original (starting 1.1–1.5 s before contact), crop around the player to roughly 16:10 with the player about 60% of frame height, and scale to 1280 wide.
- Run pose on every frame. Choose four frames by hand: top of the take-back, contact, and start and end of the drawn path (excluding the ready position and recovery). Automatic contact frames are often wrong; always check visually.
- Clip structure:
  1. **Real speed** once.
  2. **Quarter speed**, drawing the hitting-hand path frame by frame (forehand = hitting wrist; two-hander = midpoint of both wrists; one-hander = midpoint before contact, hitting wrist after), orange→cyan gradient, with captions for each phase at the bottom.
  3. **Freeze at the top of the take-back** for about 3 s, circle it (green = correct, red = problem) with a short headline.
  4. **Freeze at contact** for about 3 s: white circle on the contact point (the auto position often misses the ball, so set it by hand), yellow circle on the front knee with its angle (skip for one-handers, where the legs overlap side-on).
  5. **Freeze on the full path.** On the worst clips, overlay the session's best shot of the same type, from path start to contact, scaled by torso length and aligned at shoulder center, as an animated green dashed line with a black outline, plus one sentence on the fix.
- Encode H.264, yuv420p, faststart, 960 wide, about 1–2.5 MB per clip. Contact-sheet 4 frames from each clip to check that captions don't cover anything and circles land in the right place.
- Avoid ✓ and ✗ in captions; many CJK fonts lack them and show boxes.

## 3. Report structure

Produce an HTML page (or the format the user asks for), in this order:

1. **Verdict**: answer the player's question directly; biggest improvement, biggest problem, key numbers; corrections to the previous review. Below it, a stats strip (swings by stroke, sampled net rate or "not counted" with the reason, one or two key metrics).
2. **Causes**: group the problems into 2–3 causes, each with a timestamped example.
3. **Best vs worst**: 4 groups, each with 3 clips, a 3-column table (take-back, drop, contact, finish, feet, knee angle) and one sentence on the pattern.
4. **Compared with last time**: what changed in the best and the worst shot, as a table plus side-by-side clips.
5. **One-handed backhand** (if practicing): stats, checklist, 3 good and 3 bad clips, shot-by-shot list, and advice on whether to keep training it now.
6. **Knees and footwork**: metrics table and risks sorted into "priority / watch / improving", each with a fix. State clearly that this is not medical advice, and suggest seeing a sports-medicine doctor for swelling, locking, giving way, or soreness lasting more than a week.
7. **What to practice next**: see section 5.
8. **Camera advice** (if the footage had gaps).
9. **Footer**: data source, sample size, measurement definitions, camera limitations.

Optional design direction: a tennis palette, with hard-court blue as the main color, ball yellow only for key numbers and highlights, grass green for "good" and clay red for "problem". Condensed numerals for a scoreboard feel. Make it readable in both light and dark mode, with no horizontal scrolling on a phone.

## 4. Common faults and fixes

Classify what you see with this table first, then prove it with specific shots.

| Symptom | Usual cause | How it shows on video | Fix |
|---|---|---|---|
| Forehand into the net, swiping down | Take-back above the head, big loop, racket can't drop in time | Hitting hand above the nose at the top, racket head behind the head | Stop the take-back at shoulder height with the racket pointing back; shorten it for fast balls |
| Balls fly long or into the sky | Swing path too vertical; standing still on high bounces and lifting from the knees; finishing straight up | Racket finishes directly above the head; contact near shoulder height | Swing through toward the target, finishing over the opposite shoulder (forehand) or behind the hitting-side shoulder (two-hander); on high balls step back and let them drop to waist height, or step in and take them before they rise |
| Contact point too far back one shot, crowded the next | Late preparation: reaching for wide balls (late, far from the body), flicking fast balls from the side | Arm fully extended with the body falling away, or the racket barely taken back | Split-step as the opponent hits; be turned with the racket back by the time the ball bounces; big steps to get there, small steps to adjust |
| Two-handed backhand into the net or pushed | Racket held upright in front of the chest or on the shoulder, so the drop is late | Both hands above the shoulders on the take-back, racket head up | Rest the racket flat at the non-dominant hip while waiting; let the head drop below the hands before contact |
| Hopping, landing on one leg | Narrow stance; swinging before the feet stop | Narrow ankle spacing; both feet off the ground at contact; a straight leg catching the landing | Brake on the last step, swing with both feet down, step out afterward |
| Knee discomfort on backhands | Front foot locked while turning on a straight leg | Front foot doesn't move after contact and the knee is straighter than 155° | Let the front foot pivot on the ball of the foot, knee tracking the toes |
| Late or high one-handed take-back | Starting in a two-hander set-up then switching; hand above the head | Contact frame clearly late; hand above the head at the top | Decide which backhand as the ball leaves the opponent's racket; stop the take-back behind you at chest height; practice one-handers in a dedicated block, not by switching mid-rally |
| Much worse outdoors than indoors | Outdoor balls are faster and bounce higher; used to low, slow indoor balls | Higher contact points; later preparation | Use a ball machine or coach to feed high-bouncing balls; drill "step back" and early preparation |

## 5. Writing the practice plan

- **Match the setting**:
  - **Practice wall**: fixed position and rhythm first, then add side-to-side movement.
  - **Ball machine**: fixed target first, then patterned variation (alternating forehand/backhand, alternating short/deep), and random only last. Random placement trains reading direction. If the player's problem is late preparation, unsettled feet, or misjudging height and depth, going random too early just makes them rush and grooves the faults. To simulate outdoor balls, raise the launch angle and add moderate topspin so the ball bounces to chest height; start at 3.5–4 s between balls and shorten as they improve.
  - **Coach feeding**: ask the coach to feed exactly the balls that expose the problem (high, wide, fast).
  - **Rallying**: focus on one or two cues only.
- **Each drill states**: what to do, the single cue to focus on, how many balls or minutes, and what counts as success.
- **Give a countable target**, for example "out of 50 balls, how many with both feet down and the finish held at the shoulder". Use that number in the next review.
- **Give a gate for progression**, for example "8 out of 10 before adding speed or random placement".
- **Reference one-hour session**: warm-up and shadow swings 5 min → fixed balls on the main problem 15 min → fixed balls on the other side 10 min → patterned depth or width changes 10 min → alternating forehand/backhand 10 min → random 10 min only if the gate is met.
- **Weekly plans must allow recovery.** With an injury history, don't schedule several hard days in a row; alternate with light days or rest.
- **Ask for a side-on video next time** (5 minutes, waist height, outside the net) so the next review can see contact depth and knee angles.

## 6. Camera advice (ready to send to the player)

- **Behind**: phone 1.2–1.5 m high, centered on the middle of the court, whole body and the net in frame. Good for counting net/out and side-to-side position.
- **Side-on (most useful)**: outside the net on the hitting-hand side, 3–4 m away, waist height, camera perpendicular to the shot direction. Shows contact in front or behind, how low the racket drops, knee angles, and whether the player leaves the ground.
- **Front diagonal**: front corner outside the net, low camera, to check that knees track the toes.
- **Settings**: landscape, whole body in frame with space below the feet; 4K 60 fps or 1080p 120 fps (30 fps blurs the racket); lock focus and exposure; record a few continuous minutes rather than many 10-second clips.
- **Outdoors**: frame less sky and trees and more of the far court, or the ball will be nearly impossible to find.

## 7. Replying to the player

Give the verdict and the direct answer to their question first. Then summarize causes → what the best and worst shots have in common → change since last time → knees and footwork → what to practice next, without repeating the whole report. Mention the sample size and anything that couldn't be seen. Be direct and specific, like a coach who has actually watched the footage.
