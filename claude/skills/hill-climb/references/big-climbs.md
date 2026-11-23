# Big, slow or noisy climbs

Read this when the goal takes more than an hour, the check is slow or noisy,
or the work spans repos. `CLIMB` is the absolute path of `scripts/climb.py`.

## First score fast

Aim for a first real score within 15 minutes. Sharpen the check later with
`relock`.

- Search for an existing harness before you write one: `bench`, `perf`,
  `e2e`, `fixture`, `mock`.
- Start slow setup (installs, builds, seed data) in the background at once.
- Use a small synthetic fixture. Copy real data only when its shape matters,
  keep it under 100 MB, and put it under `.hill-climb/<name>/data/`.
- Profile once before the first step and attack the biggest part first.

## Helpers

Use subagents only when I asked for them or the climb is long enough to pay
for them.

- Only you write in the climb tree. `try` resets it, so a helper reads, or
  drafts a fix in its own worktree and returns a patch for you to `try`.
- Use the cheapest model that can answer, and brief it tight: the goal, the
  files, and the answer shape.
- Good moments: mapping the code during setup, a fresh view at PLATEAU, and
  the final review of the whole branch diff.

## A check you can trust

- **Steady.** Run it 3 to 5 times. If the score drifts with no code change,
  replace the clock with a count. Otherwise init with `--runs 3` or more and
  a `--min-gain` above the drift (a percent like `3%` when the score will
  shrink a lot), and add `--paired` on a shared machine.
- **Fast.** A 40-minute check gets 4 tries in 3 hours; a 1-minute one gets
  180. Get a step under 2 minutes: a sample or a count per step, with the
  full suite or the timed run as a guard or the holdout. See "Fast checks"
  in `checks.md`.
- **Not gameable.** Vary the input on each run and compare against the
  reference. Try one cheat by hand, like hard-coding the answer, and confirm
  a guard catches it.
- **Reachable.** Work out the floor: the best this design can reach. If the
  bar sits below it, ask me, with a bar you can reach or the design change
  that lowers the floor.

**Several repos:** add `--repo <path>` for each other checkout the climb
edits. Each gets the same `climb/<name>` branch, and `try` keeps or undoes
the step in all of them. Lock their check files with a path from this repo,
like `--lock ../web/tests/e2e`. Repeat `--check` to run several commands at
once; their scores add up. Give one `--score` for all, or one per `--check`
in the same order.

**Audits and open goals:** before init, list what the goal covers as
scenarios in `.hill-climb/<name>/notes.md`. Write one failing test per real
finding, from the spec or the bug report. When a step finds a new bug, add
its test and run `relock --why "found <bug>"`. A finding that needs my
answer goes in the notes and the report, not in the score.

**Holdout:** cases you never train on, under `.hill-climb/<name>/holdout/`,
passed as `--holdout` and locked. Don't open those files again. If the
visible score goes up and the holdout doesn't, the climb is overfitting.
Stop and say so.

## The card

Put this at the top of the report. Don't ask me to approve it.

> ### Climb card: `build-speed`
> **Goal:** cold build of the app 2x faster, same output
>
> | Score | Now | Bar |
> | --- | --- | --- |
> | Median build seconds, lower is better | **47.0s** | **23.5s** (2x) |
>
> | Setting | Value | Why |
> | --- | --- | --- |
> | Check | `./scripts/bench-build.sh` | Builds from clean, prints seconds |
> | Runs per score | 3, paired | Score drifts 1.2s; shared machine |
> | Min gain | 3% | Above the drift, so luck can't win |
> | Guards | `npm test`, `npm run typecheck` | Faster must still be correct |
> | Holdout | 3 of the 12 sample apps | Catches overfitting |
> | Locked | `scripts/bench-build.sh`, `test/`, `samples/` | So no step can edit the check |
> | Budget | no limit | About 2 min a step |

```
python3 "$CLIMB" init build-speed --goal "cold build 2x faster" \
  --check ./scripts/bench-build.sh --direction min --target 2x --after stop \
  --runs 3 --paired --min-gain 3% --guard "npm test" --guard "npm run typecheck" \
  --holdout ./scripts/bench-holdout.sh --lock scripts --lock test \
  --lock .hill-climb/build-speed/holdout
```

An audit over a backend and a frontend:

```
python3 "$CLIMB" init billing-audit --goal "every billing finding fixed" \
  --check "pytest tests/billing -q" --check "cd ../web && npx vitest run billing" \
  --score '(\d+) failed' --direction min --target 0 --repo ../web \
  --guard "cd ../web && npx tsc --noEmit" \
  --lock tests/billing --lock ../web/src/billing/__tests__
```

Set `--max-hours` or `--max-steps` only when I name a limit. A limit is
soft: past it, `try` goes on while a step was kept in the last hour and in
the last 5 steps. Add `--hard` only when I say the limit is strict. Change
it later with `budget --hours <more>`, `budget --steps <more>`, or
`budget --off`.

## Keep everything working

An undone step never lands. The risk is a kept step that breaks something no
guard checks.

- **Guard what people rely on.** Before init, list what the code you will
  change touches: callers, other platforms, saved data, public APIs. Give
  each a fast guard, and put the slow full suite in the milestone check.
- **Milestone check.** Every 10 kept steps and at the bar, run the full test
  suite and the holdout. Find a breaking step with
  `git bisect run <the failing command>`.
- **Fix forward.** `try --fix "<what broke>"` keeps a repair that holds the
  score. If the only fix gives up that step's gain, `git revert` its commit
  and run `relock --why "reverted step N: broke X"`.

## When it stalls

`status` prints PLATEAU after 5 steps with no gain. Stop and measure before
you guess: profile, time each stage of the check, and find the floor.

- Where does the time go: the check, a queue, a slow build, or thinking?
- Is the check flaky, too coarse to see small wins, or blind to what's wrong?
- What tool, access, data, or compute would change the next ten steps?
- Is there a bigger idea the small steps can't reach?

Log it with `python3 "$CLIMB" review "<what you found>"`, which quiets
PLATEAU for 5 steps. Fix what you can yourself. A blocker that is a climb of
its own goes under "Next climb" in the report. Two reviews with no gain
between them is STUCK.

## Raising the bar

When `try` prints BAR REACHED, the script runs the holdout. A visible win
with a flat holdout is not a win. With `--after raise`, check the floor from
your last profile, then `python3 "$CLIMB" raise 2x --why "..."`. It takes a
number or a factor of the current best; for a lower-is-better score, 2x
means half. The next bar is a bigger version of the same claim, never a new
goal.

## Housekeeping

- The script refuses files over 10 MB in a commit and prints STORAGE when
  `.hill-climb/` passes 200 MB. Shrink `data/` before the next step, and
  overwrite screenshots instead of keeping one per step.
- Wrong card, like a bad `--min-gain` or the wrong check:
  `python3 "$CLIMB" drop <name>` goes back to the base branch, keeps the old
  climb on a renamed branch, and restores the check files for a new `init`.
