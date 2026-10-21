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
- The "read-only" critic and reviewer agents could edit files and run bash,
  because their permission lived in their markdown frontmatter and wasn't
  recognized as overriding the config in `opencode.jsonc`.
- A dashboard reported "Synced" for 12 days while a stale lock file blocked
  every commit; the notification used `|| true` and ignored the real exit
  code. At the time of audit, 7,962 paths (about 110 MB) had not left the
  device.
- A telemetry plugin attacked the same class of event it was supposed to
  record, so it recorded zero errors while the backing database held six
  thousand errored tool calls.

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
- The vulnerability scan of un-committed files looked for key **shapes** and
  never printed a value, so the scan itself could not leak.

## Structural limits (still true after the fixes)

- A same-uid interpreter can read anything your shell can read.
- A blocklist over `bash *: allow` is a tripwire. Turn it into a real wall by
  denying `bash: *` and allowing only the verbs you need.
- If you claim an agent is "read-only", prove it by resolving the rules
  (see docs/HARDENING.md). Descriptions do not enforce anything.
