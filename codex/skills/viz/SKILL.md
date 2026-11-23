---
name: viz
description: House style for anything that shows data or a system as a picture - charts, graphs, benchmarks, before/after comparisons, stat cards, dashboards, and flow, pipeline, architecture or timeline diagrams, interactive by default. Use before drawing any of them, in chat or for a PR, doc or post, and when the user says "viz", "visualise", "chart this", "diagram this" or "show me". Also use it, unasked, to draw a PR map whenever the user asks to see their PRs or work, and right after you open or update several PRs. Its look wins over any other chart or diagram styling guidance.
---

# viz

Black, gray and white. One idea per picture. The thing that matters is solid
white; everything else is outlined, hatched, dashed or dim. Colour appears
only to report state.

## 1. Decide what it says

Write the one sentence the picture proves, such as "v2 starts 7× faster". If
you can't, there is no chart yet: get the numbers, or answer in text.

- Shorten that sentence to a number and a word. It is the takeaway, set at
  the right of the heading.
- Drop every series, label and section that does not support it. A second
  point gets a second block, not a busier first one.
- Use real numbers only. Never invent, smooth or pad data. If a value is an
  estimate, draw it dashed.

## 2. Pick the form

| The point is | Draw | Start from |
| --- | --- | --- |
| Before and after, A against B | Two or three bars with big values | `assets/chart.html`, first block |
| Change over time | One solid line, the comparison dashed | `assets/chart.html`, second block |
| Ranking of several things | Thin bars, the subject solid | `assets/chart.html`, third block |
| How a process, pipeline or system works | Nodes and wires, with tokens moving through if things flow | `assets/flow.html` |
| Open PRs: how they group, land and what they risk | A PR map, see "PR map" below | `assets/pr-map.html` |
| One number | The number, big, with its unit. No chart | |
| Exact values to look up | A table. No chart | |

Never a pie, donut, gauge, radar, 3D, stacked area or second y-axis.

### PR map

Draw one, without being asked, when the user wants to see their PRs or work,
and as the last step after you open or update several PRs. List them with the
workspace's PR tooling (for example every open PR by the user, plus any
stranded by a wrong-base merge and any review requested of them).

- One block per mission: PRs that ship one outcome together, across repos.
  Order the blocks by blast radius, widest first. The heading names the
  mission; the takeaway says what a mistake reaches, such as "every
  dashboard call".
- One lane per repo, nodes in merge order joined by wires. Node classes:
  `start` (solid) is what to review or merge first; `wait` (hatched) is
  blocked on the node before it; `bad` (red) is a conflict, a PR stranded
  off the default branch, or failing tests; `plan` (dashed, no link) is not
  pushed or not written yet; `step` (no box) is a release, deploy or
  "ships with" note.
- Under the lanes, three lines: `for` (what the PRs achieve together),
  `blast radius` (what breaks and for whom, plus any ordering hazard between
  repos) and `owner`. Get these from the PR bodies and the work you did, not
  from guesses; a guessed risk is said as one.
- Every PR node is a link to its diff with a hover card: repo, title,
  +/− lines with a bar, files changed, state and checks. Fill it with
  `scripts/pr-data.py --into page.html owner/repo#123 ...` (set
  `GH_CMD="ws gh"` where the workspace wraps gh). The `data-pr` keys are
  `repo#number`.
- Before showing it, preview once with a hover forced on a node near the top
  (call `show(...)` in a throwaway copy) to check the card.

## 3. Draw it

Copy the asset, swap in the data and delete the blocks you don't need. One
self-contained HTML file: hand-written HTML, CSS and SVG, no chart library,
nothing loaded from the network. Keep the tokens and classes as they are.

Emphasis, strongest first:

- **Solid white**: the subject, the new version, the result.
- **Gray outline with hatching**: the baseline, the old version, the others.
- **Dashed and dim**: planned, estimated, not built yet.
- **Green, red, amber**: passed, failed, in flight. Never to tell series
  apart and never as decoration. If nothing has a state, nothing has a colour.

Type:

- Bold tight sans for headings and big values. Mono for every label, tick,
  unit and note.
- Sentence case everywhere. No uppercase labels.
- Real characters: × − ≈ → ·. Round to what the reader can use: 7.5×, not
  7.529×.

Layout:

- Each block is a heading on the left, the takeaway on the right, a hairline,
  then the marks. Left-aligned, never centred.
- Label the thing itself. No legend, no key.
- No gridlines. An axis is one hairline and at most its first and last tick.
- Bars start at zero and share one scale within a block.

Diagrams:

- A diagram is a block like any chart: the same heading, takeaway and
  hairline. No status banner such as "live" or "running now" above it.
- Same marks as the charts. A node is a 1px outlined box with square corners.
  It is hatched when it holds waiting work and solid white while it is doing
  the work. A wire is a 1px line with square corners.
- Name each part in white, then ` · ` and a gray clause saying what it does:
  `worker · one job at a time`.
- Time runs left to right. A stage that is planned gets its own block below,
  drawn dashed.
- Motion only when something really moves through the system. Tokens are
  small solid white squares that ride the wires, red only when they fail. The
  footer says what one loop stands for, and Pause and speed controls are
  always there. Nothing else animates.

Interaction (every new visualization is interactive):

- Details go in a tooltip: one floating box with square corners, a 1px dim
  border and the page background, mono 12px, the item's name and numbers
  in white. It is `position: fixed` and `pointer-events: none`, sits 14px
  off the pointer, flips to stay inside the viewport, and closes on leave,
  a tap elsewhere, scroll or Esc. Keyboard focus opens it under the item.
- Nothing moves when you interact. No readout lines, no text that grows or
  wraps, no hover borders or padding. Value columns get a fixed width, sort
  arrows always reserve their space, and toggled labels keep their length.
  Highlight with colour, opacity or a cursor line only.
- Hover areas are generous and contiguous, so the pointer never falls into a
  gap and the tooltip never flickers:
  - A chart over time has one transparent hit rect on top, covering every
    lane plus 8px each side. The pointer's x picks the point, clamped to
    the first and last. ← → step a 1px white cursor.
  - A bar row is one element across label, bar and value. Rows are
    separated by padding, not gaps.
  - A diagram part is one group with a transparent rect padded around its
    label and node.
  - A table row is the whole `tr`.
- Several comparable slices (incidents, environments, weeks, measures) get
  one block with a row of square outlined buttons, the active one solid,
  instead of near-identical blocks. Heading and takeaway follow the choice,
  and every slice draws at the same height.
- Interaction adds detail and never hides the answer: the takeaway and key
  values stay printed. Mouse, touch (pointer events) and keyboard
  (`tabindex`, a 1px focus outline) all work. Plain script in the file.

## 4. Never

Gradients, glows, shadows, glass. Cards inside cards, coloured borders or
stripes. Emoji or decorative icons. Rainbow or brand palettes. Rounded
corners or bar ends. Legends. A title that names the chart type. Subtitles, captions,
footnotes or a "key insights" box. Values that need a hover to read. Layout
that shifts on hover, click or toggle. Entrance animations.

## 5. Show it

- In T3 Code: `html_preview` the file, look at the PNG, fix what is wrong,
  then `html_render`. Set no page background; the tokens follow the thread's
  theme.
- For a file to post elsewhere: `scripts/png.sh <file.html> <out.png>` writes
  a 2× PNG on the black background.
- Inside an app's own code: port the tokens and the rules into its styling.
  Do not embed these HTML files.

Before showing it, check the render: the first thing the eye lands on is the
answer, no text overlaps or is cut off, and every colour is a state.
Then, in a throwaway copy, script one check per block and log the results:
record every block's, row's and button's box, run each toggle, sort and
hover, and confirm the boxes are unchanged. Use `elementFromPoint` at
gaps and edges (scroll the target into view first) to confirm they hit the
target. Open one tooltip, preview at 728 and 390 wide, then delete the copy.
