# quilt-fleet-conductor

**Orchestrates all Quilt canon tools as a single workflow.**

## Quick start

```bash
pip install -e .

# List every tool the conductor can call
quilt-fleet-conductor list

# See predefined workflows
quilt-fleet-conductor workflows

# Run a workflow
quilt-fleet-conductor run explore    # build index + search + graph
quilt-fleet-conductor run publish   # full canon-to-book pipeline
quilt-fleet-conductor run verify    # smoke-test all build steps

# Call a single tool directly
quilt-fleet-conductor call quilt-canon-search list-doctrines
quilt-fleet-conductor call quilt-canon-graph export --output /tmp/g.json

# Status
quilt-fleet-conductor status
```

## Pre-defined workflows

### `explore` — discover canon
1. `quilt-canon-search list-doctrines` — list the 5 bedrock doctrines
2. `quilt-canon-search query "scar witness canon"` — search canon
3. `quilt-canon-graph build` — build the knowledge graph

### `publish` — full canon to book
1. `quilt-canon-search index` — build the search index
2. `quilt-canon-graph export` — export graph as JSON
3. `quilt-canon-book build` — compile canon into a book

### `verify` — smoke-test everything
1. `quilt-canon-search index` — verify search builds
2. `quilt-canon-search query substrate` — verify queries work
3. `quilt-canon-graph build` — verify graph builds
4. `quilt-canon-book summary` — verify book compiles

## Why this matters

When you have 6+ canon tools (mcp, search, graph, radio, game, book, plus 30+ others), running them individually is friction. The conductor treats them as a **single substrate**.

- **Discover**: scan `/workspace/repos/` for `quilt-*` tools
- **Orchestrate**: chain them as workflows
- **Status**: live liveness check on every tool

## Adding a new workflow

Edit `quilt_fleet_conductor/workflows.py` and add a workflow:

```python
WORKFLOWS["my_workflow"] = [
    Step(tool="quilt-canon-search", args=["index"], description="Index canon"),
    Step(tool="quilt-canon-graph", args=["build"], description="Build graph"),
    Step(tool="quilt-canon-book", args=["build"], description="Compile book"),
]
```

The conductor auto-discovers the tool's CLI module from its repo layout.

## Fleet integration

- **`quilt-canon-search`** — search canon
- **`quilt-canon-graph`** — knowledge graph
- **`quilt-canon-book`** — print-ready book
- **`quilt-canon-mcp`** — MCP server
- **`quilt-canon-radio`** — TTS broadcast
- **`quilt-canon-game`** — browser game
- **`quilt-multi-oracle`** — multi-model chord

## The 5 bedrock doctrines

1. `cells_are_scars` — every cell records an attempted entry
2. `witness_log_is_prediction` — the log IS the prediction
3. `canon_gate_is_chord` — canon passes when multiple agents agree
4. `oracle_is_heard` — JEV probes canon with multi-model consensus
5. `substrate_quantum` — the substrate is the walker; canon is substrate-aware

## Polyformalism canary

```bash
python -m quilt_fleet_conductor.canary
# → 0x24a555471370b18d
```

## License

MIT
