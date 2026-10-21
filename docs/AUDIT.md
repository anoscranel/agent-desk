# Case study: the audit behind the desk

A real audit of an opencode setup (October 2026). The full report is not part
of the release; these are the sharable findings and what was learned.

## The failure mode

The desk's prompt promised rules the harness did not enforce.

- The git-commit and git-push ask rules missed 58 of 106 real commit/push
  commands, because they named one spelling and missed the wrappers
  (`git -C`, absolute paths, proxy prefixes).
- A read-all rule (`read: "*": allow`) sat after the built-in `*.env: ask`
  in the resolved rule list, so the secrets file was readable without a
  prompt.
- The "read-only" critic and reviewer agents could edit files and run bash.
  Their markdown frontmatter granted edit rights and set no bash limit, and a
  key in an agent's frontmatter overrides the same key in `opencode.jsonc`,
  so a fix made only in the jsonc would have been ignored.
- A sync job reported "Synced" for 12 days while a stale lock file blocked
  every commit. The script swallowed the failure with `|| true` and logged an
  exit code read after `$(date)` had reset it. At audit time, 7,962 changed
  paths (about 110 MB) had never left the device.
- A telemetry plugin listened on a hook that fires only after a tool
  succeeds, so it logged zero errors while the session database held about
  6,900 failed tool calls from the same period.

## How the fixes were validated

- Every fix was staged, not installed. Each had a test that ran against the
  real binary in a hermetic scratch, so the live config never loaded.
- The permission overlay was tested against 178 fixtures. The same author
  wrote the fixtures and the fix, so three independent validators each
  attacked the previous round's delta with new probes. Two rounds found real
  defects; the third round's findings were all known spellings of the
  blocklist-over-allow-all limit. The fix stops there deliberately.
- A tabletop asked a fresh model to answer 10 scenarios using only the prompt
  file: the old prompt scored 5/10, the new one 10/10. The question key was
  written and hashed before either run.
- The secret scan of uncommitted files looked for key **shapes** and
  never printed a value, so the scan itself could not leak.

## Structural limits (still true after the fixes)

- A same-uid interpreter can read anything your shell can read.
- A blocklist over `bash *: allow` is a tripwire. Turn it into a real wall by
  denying `bash: *` and allowing only the verbs you need.
- If you claim an agent is "read-only", prove it by resolving the rules
  (see docs/HARDENING.md). Descriptions do not enforce anything.
