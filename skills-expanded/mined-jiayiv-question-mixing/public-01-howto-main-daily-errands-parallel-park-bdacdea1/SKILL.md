---
name: parallel-park
domain: daily
subdomain: errands
locale: [generic]
interface: physical
difficulty: intermediate
est_time: 5min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Park a car parallel to the curb inside a street space without touching another vehicle or blocking traffic.

## Preconditions

- You are legally allowed to park on that side of the street.
- The curb space is about 1.5 times your car length, with clear room at both bumpers.
- Mirrors are adjusted and the rear window is clear enough to see.
- You can pause safely with your turn signal on while traffic passes.

## Steps

1. **Choose a forgiving space.** Pass spaces shorter than 1.5 car lengths or beside fire hydrants, driveways, bus stops, or corners. → *Expect:* a legal space with a clear entry angle and no hidden curb obstruction.
2. **Signal and stop beside the front car.** Pull even with the parked car ahead of the space, about 2 to 3 feet away, with rear bumpers roughly aligned. → *Expect:* your right side mirror is near the other car's left mirror and traffic can see your signal.
3. **Check all directions before reversing.** Look over both shoulders, then use mirrors and the backup camera if present. → *Expect:* no cyclist, pedestrian, or car is entering your path.
4. **Reverse with the wheel turned toward the curb.** Back slowly until your rear inside corner points toward the curb and the rear car appears in the outside mirror. → *Expect:* your car sits at about a 45 degree angle into the space.
5. **Straighten while continuing back.** Turn the wheel back to center and reverse until your front bumper clears the rear bumper of the front car. → *Expect:* the front bumper can swing inward without clipping the car ahead.
6. **Turn away from the curb to tuck in.** Rotate the wheel fully away from the curb and ease back. → *Expect:* the front end swings into the space and the car becomes parallel to the curb.
7. **Center the car with small moves.** [BRANCH: too far from curb | too close to curb] if too far, pull forward with wheel toward curb; if too close, pull forward with wheel away, then straighten. → *Expect:* tires are 6 to 12 inches from the curb and bumpers have space at both ends.
8. **Secure the parked car.** Straighten the wheels unless parking on a hill, shift to park or gear, and set the parking brake. → *Expect:* the car is still, legal, and not sticking into the lane.

## Decision points

- Traffic stacks up behind you → pause with signal on and let the impatient driver pass if there is room.
- The curb disappears from view → use the passenger mirror tilted down, but keep checking the street side.
- The front bumper is not clear → pull forward to reset before turning away from the curb.
- A wheel touches the curb → stop; use a tiny forward correction instead of grinding the tire.

## Failure modes & recovery

- **F1 Space too short:** detect by needing bumper contact to fit, recover by leaving and choosing a longer space.
- **F2 Front corner swinging wide:** detect by front bumper approaching the car ahead, recover by stopping and pulling forward to reset the angle.
- **F3 Rear wheel climbing curb:** detect by a bump or tire scrape, recover by stopping, pulling forward, and re-entering with less inward angle.
- **F4 Blocking traffic too long:** detect by cars unable to pass safely, recover by canceling the attempt and circling back.

## Verification

The car is parallel to the curb, 6 to 12 inches from it, fully inside the marked or legal space, and has visible bumper clearance front and rear.

## Variations

- Left-side parking on a one-way street: reverse the steering directions and mirror checks.
- Backup camera: use it for distance, but rely on mirrors for side clearance and street traffic.
- Hill parking: turn wheels according to local rules before setting the brake.

## Safety & privacy

Medium risk from traffic, cyclists, pedestrians, and low-speed collisions. Never keep reversing if you lose sight of a person, curb, or bumper; stop and rebuild the setup.
