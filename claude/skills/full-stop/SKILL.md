---
name: full-stop
description: Trigger this if the user says 'full stop', even as a closing "Full stop." that reads like emphasis. Same as full-send - from a ticket link, a PR, a branch, or the change in this thread - but stops when the PR is ready to merge.
---

# Full Stop

Do the same work as `full-send`, but stop with the PR ready for the user to
merge. Never merge it.

Read [full-send](../full-send/SKILL.md) and follow its scope, build, proof,
review, filing, babysitting, and asking rules. An explicit "full stop"
request authorizes that work, including full-send's testing permission,
without a separate "full send" request. Its merge permission does not apply.
The overrides below take precedence.

## No merging

You may commit, push, rebase, fix conflicts, and use `--force-with-lease` on
this task's own branches. Never merge, enable auto-merge, enter a merge
queue, push to the default branch, bypass branch protection, or delegate
those actions.

Disable existing auto-merge and remove the PR from any merge queue before
work begins. Check again before each push, and report these changes. If you
cannot prevent an automatic merge, ask before going further.

Follow-up work the goal needs, such as a consumer PR or a version bump, is
still yours. Take each one to ready, the same way. If a follow-up depends on
this PR merging first, report it as the next step instead of waiting.

## Stop at the gate

Use the conditions in full-send's step 7 as the merge gate. Replace the merge
itself with this handoff. Proof and review must cover the final diff. Recheck
behaviour changes and meaningful conflict fixes before the handoff.

Fetch the target branch and check the live PR's head, base, checks, reviews,
and mergeability. Confirm it is open, not a draft, and not set to merge
without the user. If someone else merged it, report that instead.

- **Ready to merge:** the merge gate passes.
- **Waiting for approval:** only human approval remains. Confirm that it is
  the actual blocker. Never wait for it.
- **Blocked:** say what prevents readiness, what you tried, and what is
  needed. Follow full-send's rules for asking the user.

Then send full-send's report. State whether each PR is still open and
unmerged.
