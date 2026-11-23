#!/usr/bin/env python3
"""Fetch the PR facts a PR map shows in its tooltips.

usage: pr-data.py [--into page.html] owner/repo#123 [owner/repo#124 ...]

Prints JSON keyed by "repo#number" (repo without the owner), the same key the
page's data-pr attributes use. With --into, replaces __DATA__ in that file
instead. Set GH_CMD to wrap gh, e.g. GH_CMD="ws gh" in a workspace.
"""
import json
import os
import shlex
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

FIELDS = "number,title,additions,deletions,changedFiles,isDraft,state,mergeable,baseRefName,statusCheckRollup,url"
FAILED = {"FAILURE", "ERROR", "TIMED_OUT"}
PASSED = {"SUCCESS", "NEUTRAL", "SKIPPED"}


def check_state(check):
    return (check.get("conclusion") or check.get("state") or "").upper()


def describe_checks(checks):
    failing = sorted({c.get("name") or c.get("context") or "?" for c in checks if check_state(c) in FAILED})
    if failing and all("snyk" in name.lower() for name in failing):
        return "snyk only"
    if failing:
        return "failing · " + ", ".join(failing)
    if any(check_state(c) in PASSED for c in checks):
        return "green"
    return "none run"


def describe_state(pr):
    if pr["state"] == "MERGED":
        return "merged into " + pr["baseRefName"]
    if pr["state"] == "CLOSED":
        return "closed"
    if pr["mergeable"] == "CONFLICTING":
        return "conflict with " + pr["baseRefName"]
    kind = "draft" if pr["isDraft"] else "open"
    return kind + " · base " + pr["baseRefName"]


def fetch(ref):
    repo, number = ref.split("#")
    gh = shlex.split(os.environ.get("GH_CMD", "gh"))
    result = subprocess.run(
        gh + ["pr", "view", number, "--repo", repo, "--json", FIELDS],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(f"{ref}: {result.stderr.strip()}\n")
        return None
    pr = json.loads(result.stdout)
    key = repo.split("/")[-1] + "#" + str(pr["number"])
    return key, {
        "repo": repo.split("/")[-1],
        "t": pr["title"],
        "a": pr["additions"],
        "d": pr["deletions"],
        "f": pr["changedFiles"],
        "s": describe_state(pr),
        "c": describe_checks(pr["statusCheckRollup"] or []),
        "u": pr["url"],
    }


def main(argv):
    into = None
    if argv[:1] == ["--into"]:
        into, argv = argv[1], argv[2:]
    if not argv:
        sys.exit(__doc__)
    with ThreadPoolExecutor(max_workers=8) as pool:
        found = [item for item in pool.map(fetch, argv) if item]
    data = json.dumps(dict(found), separators=(",", ":"))
    if into is None:
        print(data)
        return
    with open(into) as page:
        html = page.read()
    if "__DATA__" not in html:
        sys.exit(f"{into}: no __DATA__ placeholder")
    with open(into, "w") as page:
        page.write(html.replace("__DATA__", data))
    print(f"{len(found)} PRs written into {into}")


if __name__ == "__main__":
    main(sys.argv[1:])
