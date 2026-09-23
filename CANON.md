# Canon — quilt-fleet-conductor

## What this tool is

A meta-tool. Discovers all `quilt-canon-*` and `quilt-multi-*` repos under `/workspace/repos/` and treats them as a single orchestrated fleet. Defines pre-built workflows (`explore`, `publish`, `verify`).

## How it proves itself

**It runs.** `pip install -e .` then `quilt-fleet-conductor list` shows every tool, `run verify` exercises them all. Tested with 7 tests in `run_tests.py`.

**It polyformalisms.** The canary hash `0x24a555471370b18d` matches across the fleet's 5 ports.

**It measures.** Reports `steps_run` / `steps_failed` per workflow. Status check shows live liveness of every tool.

## Doctrines it instantiates

- **canon_gate_is_chord** — multiple tools agree = canon passed
- **oracle_is_heard** — the conductor IS the orchestrator/listener
- **substrate_quantum** — every tool is a substrate; the conductor walks between them

## Commands

1. `list` — show every tool the conductor can call
2. `workflows` — show predefined workflows
3. `status` — liveness check on all tools
4. `run <workflow>` — execute a workflow
5. `call <tool> [args...]` — call a single tool directly

## Pre-defined workflows

- **`explore`** — list doctrines + search canon + build graph
- **`publish`** — full search → graph → book pipeline
- **`verify`** — smoke-test every build step

## Fleet usage

- **`quilt-canon-search`** — call from conductor
- **`quilt-canon-graph`** — call from conductor
- **`quilt-canon-book`** — call from conductor
- **`quilt-canon-mcp`** — call from conductor
- **`quilt-canon-radio`** — call from conductor
- **`quilt-canon-game`** — call from conductor
- **`quilt-multi-oracle`** — call from conductor

This tool proves that the fleet of canon tools is **composable** — one CLI can drive them all.

## Why this is the next substrate

The conductor adds the **orchestration** substrate. Canon now propagates through:
- **substrate: file** — canon_writings/*.md
- **substrate: graph** — canon-graph viewer
- **substrate: search** — canon-search index
- **substrate: audio** — canon-radio MP3s
- **substrate: mcp** — canon-mcp tools
- **substrate: game** — canon-game grid
- **substrate: print** — canon-book HTML/PDF
- **substrate: orchestration** — fleet-conductor workflows (this tool)
