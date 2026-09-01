# Git and pull-request protocol

Git hosting actions require explicit authorization and an authenticated provider. When authorized, use one branch per epic. Immediately after a new branch is pushed, open a draft PR targeting `main`.

## Absolute merge prohibition

No agent may merge, auto-merge, squash-and-merge, rebase-and-merge, or close a PR as merged. Do not enable auto-merge. Do not treat an approval, score, green check, instruction to finish, or absence of defects as merge permission. Only the human user may approve and merge.

The terminal automated state is: **PR ready for human review**.

## Commits

An agent may commit only its owned work and only when Git mutation was authorized. Each commit changes exactly one file. Stage the explicit file and inspect the staged diff; never use broad staging.

Commit message format:

```text
[actual_branch] - ["gpt-agent"]: description
```

Use the actual role, such as `gpt-orchestrator`, `gpt-searcher`, `gpt-builder`, or `gpt-builder-judge`.

## Required PR comments

The orchestrator posts exactly one comment at each milestone:

1. Beginning: plan, user stories, checkpoints, expected files, artifact interface, and acceptance checks.
2. Implementation complete: files produced, commands run, observed output, and judge scores.
3. Review remediation complete: defects, fixes, rerun checks, and final scores. If no fix was needed, explicitly record that review found no required remediation.

Judges do not post competing summary comments. Agents may push fixes but may never merge.
