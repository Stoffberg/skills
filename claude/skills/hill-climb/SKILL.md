---
name: hill-climb
description: Reach any goal that a command can score (faster, fewer bugs, an audit, "make X stable", a port, a UI, a text) in small steps, keeping wins and undoing losses, across one or many repos. Use for "hill climb", "/hill-climb", "climb this", "keep going until it passes", "until the council approves", or to resume or report on a climb.
metadata:
  source: https://github.com/Bil0000/Hill-Climb/blob/main/skills/hill-climb/SKILL.md
---

# Hill climb

You work toward a goal in many small steps. A check scores each step with no
human in the loop. `scripts/climb.py` keeps the score: you edit code, it runs
the check, commits a win or undoes a loss, and writes the log. Never write a
score down yourself, and never decide a step "basically" passed.

Every goal becomes a command that prints a number, so never skip the script
because a goal "feels too open".

I start a climb and leave:

- Don't send updates or ask me to approve anything you can decide. Start at
  once. I read a question I must answer (money, access, hardware, a bar no
  design can reach) and the report.
- Keep the state on disk (`status`, `notes.md`), not in chat.
- Never wait with a sleep loop. Run long commands in the background.
- Other threads share this machine. Run one heavy check at a time.

`CLIMB` is the absolute path of `scripts/climb.py` next to this file. Write
the full path into each command and run it from inside the target repo. The
climb gets its own branch, and an undone step deletes untracked files, so
climb in a separate worktree.

**Goal over an hour, a slow or noisy check, several repos, or a stall?** Read
`references/big-climbs.md` first: holdouts, guards, the card, helpers,
budgets and blocker reviews. Check recipes are in `references/checks.md`.

## 1. Resume or reuse

```
python3 "$CLIMB" list; python3 "$CLIMB" kits "<two or three goal words>"
```

A climb for this goal exists: switch to its branch, run `status <name>`,
read `.hill-climb/<name>/notes.md`, and carry on. A kit fits:
`python3 "$CLIMB" reuse <kit>`, then make its check fail and pass once
before you trust it.

## 2. Build the check

The climb is only as good as its check. Write it, and the reference it
compares with, before `init`:

- **Fix or audit:** tests that fail today, written from the spec or the bug
  report, not from your fix. Score with `--score '<failure count regex>'
  --direction min --target 0`. Guard with the tests that pass today, in
  their own files, so a fix can't break old behavior and a crash can't pass
  as fewer failures.
- **Faster or smaller:** a script that times or, better, counts the work on
  fresh random input. Keep the old code as the reference and guard that the
  new output matches it. Score with `--direction min --target <N>x --runs 3`,
  plus `--paired` for a timer.
- **Look, feel, writing:** `scripts/judge.py` with a rubric and good
  examples.
- **"Until the council approves":** a review is not a command, so score with
  `judge.py`, a rubric written from the request and the council's models
  (`--panel claude,codex --model codex=<latest Sol>`), with a bar of 9. Run
  the real `council` skill once, at the bar. Never run it on every step.
- **Anything else:** whatever prints how close you are as a number.

`--score '<regex>'` reads the last matching line of any test runner's output
and adds up the numbers it captures. Without it, the check's last line must
be a bare number.

Before you trust the check, break the code on purpose and see the score get
worse. Keep a step under 2 minutes: a sample per step, the full suite as a
guard.

## 3. Start

```
python3 "$CLIMB" init <name> --goal "..." --check "<command>" \
  --direction min --target <bar> --guard "<command>" --lock <check files>
```

`init` makes the branch, commits the check files, measures the baseline and
refuses to start if a guard already fails. Add a `--check` and a `--repo`
for each other repo the work touches. If I named no bar, pick one that is
ambitious and checkable, like "2x faster".

## 4. Climb

Each step is one idea, one change, one `try`:

1. Read `status`. Don't retry an idea the log already undid unless you can
   say what is different, and never more than twice.
2. Make one change for one reason, with your guess in the idea, like
   `"cache the parser (expect -10%)"`. A guess far off means your model of
   the code is wrong: profile before the next step.
3. `python3 "$CLIMB" try "<idea>"` commits a win or resets the tree. The
   step's check output is in `.hill-climb/<name>/last.txt`; don't rerun the
   check to read it. Don't edit the tree while a check runs.
4. Every 5 steps, put what works, what doesn't and what's next in
   `.hill-climb/<name>/notes.md`. Every 10 kept steps, look at the real
   thing yourself. If the score and what I want drift apart, fix the check
   with `relock --why "..."`.

**Never cheat the check.** Special-casing the check's inputs, hard-coding or
caching expected outputs, skipping or weakening tests, hiding errors, making
the benchmark do less work, or editing a locked file is a failed climb even
if `try` keeps it. If that is the only way forward, the check is wrong. Say
so.

Stop when the bar is reached, `status` prints STUCK, a limit I set is spent,
or the next step needs something only I can give.

## 5. Report

Before it, review `git diff <start>..HEAD` as a whole for removed tests,
swallowed errors, a feature turned off and changed defaults. Fix with
`try --fix`, run the check once more, and run `python3 "$CLIMB" save`.

Make the report scannable in ten seconds:

> ### Climb `build-speed`: bar reached
> **47.1s → 18.7s**, 2.5x faster (bar 23.5s, reached at step 41)
>
> | | |
> | --- | --- |
> | Steps | 19 kept of 52 |
> | Safety | Guards passed on every kept step. Full suite and final review clean |
> | Time | 1h 50m, about 2 min a step |
> | Branch | `climb/build-speed`, 19 commits |
>
> **What worked**
> - Incremental type cache: −12s
>
> **Tried and undone**
> - swc swap: broke 3 guards
>
> **Your move**
> - Review: `git log --oneline 1a2b3c4..climb/build-speed`

The headline status is one of: bar reached, budget spent, stuck, holdout
disagrees, needs you. Biggest wins first. At most 3 bullets a section.

## Commands

| Command | Does |
| --- | --- |
| `init <name> --goal --check --direction min\|max` | Baseline, branch, kit. Options: `--check` (repeat), `--score '<regex>'`, `--repo` (repeat), `--guard` (repeat), `--target` (number or `2x`), `--after stop\|raise`, `--runs`, `--paired`, `--min-gain`, `--timeout`, `--holdout`, `--lock` (repeat), `--max-hours`, `--max-steps`, `--hard`, `--here` (no new branch) |
| `try "<idea>" [--fix]` | Score the edit, keep or undo it. `--fix` keeps a repair that holds the score |
| `status [name]` | Score, trail, last steps, PLATEAU or STUCK |
| `relock [name] --why "..."` | Accept a fixed check and measure again |
| `holdout --why "..."` / `raise <bar> --why "..."` | Run the holdout now / set a harder bar |
| `review "<found>"` | Log a blocker review |
| `budget [name] [--hours N] [--steps N] [--off]` | Add hours or steps, or remove the limits |
| `drop [name]` | Abandon the climb, keep its branch |
| `list` / `save [name]` | Climbs in this repo / save the kit now |
| `kits [words]` / `reuse <name>` | Find saved kits / restore one and print its `init` |
