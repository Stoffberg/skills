---
name: reach
description: Run shell commands on another machine over HTTPS with reach.stoff.dev. Use whenever you need to run or check something on a machine you can't SSH into - a server, a VM, a teammate's laptop, a Windows box - instead of asking the user to paste commands and output back and forth.
---

# reach

- Ask the user to run `curl -sS https://reach.stoff.dev | sh` (or `irm https://reach.stoff.dev | iex` on Windows) on the target and send you the 8-character code.
- `curl https://reach.stoff.dev/<code>` first: `shell` says whether to write sh or PowerShell.
- Run: `curl https://reach.stoff.dev/<code> -H 'Accept: application/json' -d '<command>'` returns `exitCode`, `stdout` and `stderr`. Add `?cwd=/path&timeout=50` as needed; 124 means it timed out.
- Scripts: `--data-binary @script.sh`, since `-d` strips newlines.
- The code is the only key. End the session with `curl -X DELETE https://reach.stoff.dev/<code>` when done.
- More: `curl https://reach.stoff.dev`.
