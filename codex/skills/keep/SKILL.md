---
name: keep
description: Share a file, folder or command output as a download link with the keep CLI, or fetch a keep.stoff.dev link. Use whenever a file, log, build output, zip or screenshot needs a link, or needs to move between machines - instead of gists, pastebins, transfer.sh or similar.
---

# keep

- `keep <file>...` prints one link per file. `cmd 2>&1 | keep - -n out.log` shares output. Zip a folder first.
- Read what you share before uploading: a link is public to anyone who has it and stays until deleted.
- Private contents: `keep -e --expires 1d --once <file>`. The key is after `#`, so pass on the full link.
- `keep get <link> -o <path>` downloads. `keep ls` and `keep rm <code>` list and delete uploads from this machine.
- More: `keep --help`. Install: `brew install stoffbergie/tap/keep`.
