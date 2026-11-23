---
name: full-send
description: Trigger this if the user says 'full send'. Takes work - a ticket link, a PR, a branch, or the change in this thread - to a merged PR with nobody watching - scope, build, prove, sol-loop, file, babysit, merge.
---

# Full Send

The user handed you work and walked away. Own it from its current state to a
merged PR, and finish everything the goal needs to land without checking in.
Do not assume this autonomy unless the user clearly asked for "full send".

## What the request covers

Authorized: branches, commits, pushes, opening and editing PRs, rebasing and
`--force-with-lease` on this task's own branches, moving a linked ticket's
status, merging once the gate passes, releasing to dev or staging, and
whatever testing the proof needs (running the app, temporary servers,
browser, simulator, device or computer-use checks), even where a project
file says to ask first.

Not authorized: comments or replies on PRs or tickets, closing or assigning
them, migrations, production, deleting data, force-pushing other branches,
changes outside the workspace, and any release beyond dev or staging: UAT,
demo, preprod, prod, a published package or image, or a Terraform apply on
another stack. A merge that triggers such a release counts, so before every
merge check what it sets off: default-branch workflows, release and deploy
config, and recent merges. The exception is a repo whose AGENTS.md or
CLAUDE.md pre-authorises merges that release: merge there as
soon as the gate passes and follow that file's deploy rules.

## Ask only when stuck

Decide everything else yourself and list the decisions in the report. Never
ask permission for work the goal needs to land: a follow-up PR in a consumer
repo, a version bump after a publish, a rebase, waiting for a workflow.

Ask with `AskUserQuestion` only when you cannot prove the change, the next
step is not authorized above, the goal is ambiguous in a way that changes the
result, the work is someone else's ticket or PR, or another PR or the default
branch already solves it. Unwatch first, and put the links, the blocker and
your recommended option in the question. With no question tool, leave every
PR unmerged and start the final message with the question.

## Steps

1. **Scope.** Read what you were given: the ticket in its tracker
   (`ws jira curl`, `ws gh issue view`, `ws az boards work-item show`), the
   PR's diff, threads and checks, or the branch and its ticket key. Check the
   default branch does not already solve it. State the goal and what is out
   of scope in a sentence or two. The goal is the outcome landing, including
   the follow-up PRs, bumps and releases it needs. Move an unstarted ticket
   to In Progress.
2. **Build** the smallest change that completes the goal.
3. **Prove** every behaviour change with evidence you observed this session:
   reproduce the problem on the default branch, apply the change, and watch
   the same user workflow pass. Mocked tests do not prove it. For UI, capture
   matched Before/After screenshots, or short videos for interactions, of the
   real UI with action/result captions and no dead time. Verify them with a
   fresh-context subagent given only neutrally labelled evidence and generic
   questions. Attach them to the PR; never commit them.
4. **Review.** Run `sol-loop` on the full diff, unless the change is docs,
   copy or config only.
5. **File.** Write the PR title and description with the `writing` skill:
   the problem, the fix, one line on proof. Link the ticket the way the
   repo's recent PRs do and move it to In Review. Open a real PR, not a
   draft.
6. **Babysit.** Handle existing checks and threads, then
   `watch_pull_request` (or `pr-wait` where the workspace file says T3
   cannot read the repo) and end the turn with one line: what you are waiting
   on, its link, and when you check next. On each wake, act only on checks
   and comments newer than the latest push. Verify each finding against the
   source and tell real failures from flakes. Fix real ones, prove the fix,
   re-run `sol-loop` and push. Decline edge-case guards, extra tests,
   compatibility shims and small performance tweaks, and draft a short reply
   with the reason for the report. Keep the branch rebased on the default
   branch; the watcher does not report BEHIND. Never wait for reviews, and
   never re-watch in a tight loop. With no PR watcher, go to the report.
7. **Merge** when all of this is true on the latest head: proof covers the
   whole diff; for code, Sol approved the current diff (any change since,
   including conflict fixes, needs another round; a clean rebase does not);
   required checks are green; every review comment is fixed or has a drafted
   reply; no human review requests changes; and the branch is up to date and
   mergeable after a fresh `git fetch`. Use the repo's usual merge method,
   never `--admin` or another bypass, and confirm it merged. If a required
   approval is missing, go to the report.
8. **After the merge,** do the follow-up work the goal needs through the same
   steps. Once the change is verified in dev, move the ticket to the
   next state the workspace's AGENTS.md names for that, without a comment.

## Report

Unwatch every PR, then send:

- Every PR link on its own line with its state: merged (with the merge
  commit), ready to merge, waiting for approval, or blocked.
- Ticket links, what changed, the proof, the `sol-loop` result, the
  decisions you made, and any follow-ups left.

If you drafted replies, ask with `AskUserQuestion` instead, giving the exact
text and destination of each: post them and resolve their threads
(`ws gh pr reply-thread`, `ws gh pr resolve-thread`), or skip them.
