"""Workflow runner — orchestrate multiple tools as a single pipeline."""
import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from .tools import Tool, discover_tools


@dataclass
class Step:
    tool: str
    args: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class WorkflowResult:
    name: str
    steps_run: int
    steps_failed: int
    artifacts: List[Path] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def run_step(step: Step, tools: dict, cwd: Path, timeout: int = 60) -> tuple:
    """Run a single tool step. Returns (success, output, error)."""
    tool = tools.get(step.tool)
    if not tool:
        return False, "", f"Tool not found: {step.tool}"

    cmd = ["python3", "-m", tool.cli_module, *step.args]
    try:
        result = subprocess.run(
            cmd,
            cwd=str(tool.repo),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return (
            result.returncode == 0,
            result.stdout,
            result.stderr if result.returncode != 0 else "",
        )
    except subprocess.TimeoutExpired:
        return False, "", f"Timeout after {timeout}s"
    except Exception as e:
        return False, "", str(e)


# Pre-built workflows — each one demonstrates the fleet acting as a unit
WORKFLOWS = {
    "explore": [
        Step("quilt-canon-search", ["list-doctrines"], "List the 5 bedrock doctrines"),
        Step("quilt-canon-search", ["query", "scar witness canon"], "Search for canon about scars and witness"),
        Step("quilt-canon-graph", ["build"], "Build the canon knowledge graph"),
    ],
    "publish": [
        Step("quilt-canon-search", ["index"], "Build the search index"),
        Step("quilt-canon-graph", ["export", "--output", "/tmp/fleet-graph.json"], "Export the graph"),
        Step("quilt-canon-book", ["build"], "Compile canon to a book"),
    ],
    "verify": [
        Step("quilt-canon-search", ["index"], "Build the search index"),
        Step("quilt-canon-search", ["query", "substrate"], "Verify substrate canon is searchable"),
        Step("quilt-canon-graph", ["build"], "Verify graph builds"),
        Step("quilt-canon-book", ["summary"], "Verify book compiles"),
        Step("quilt-canon-witness", ["verify"], "Verify witness chain integrity"),
    ],
    "witness": [
        Step("quilt-canon-search", ["query", "substrate walker"], "Find substrate walker canon"),
        Step("quilt-canon-witness", ["stats"], "Show witness log statistics"),
        Step("quilt-canon-witness", ["verify"], "Verify witness chain integrity"),
    ],
    "trace": [
        Step("quilt-canon-trace", ["stats"], "Show canon graph stats"),
        Step("quilt-canon-trace", ["walk", "--start", "11_canon_that_runs", "--steps", "8", "--seed", "42", "--mode", "weight"], "Walk canon for 8 steps"),
        Step("quilt-canon-trace", ["summary"], "Summarize the trace"),
    ],
}


def run_workflow(name: str, repos_dir: Path = Path("/workspace/repos")) -> WorkflowResult:
    """Run a named workflow."""
    if name not in WORKFLOWS:
        return WorkflowResult(name=name, steps_run=0, steps_failed=0,
                              errors=[f"Unknown workflow: {name}. Options: {list(WORKFLOWS.keys())}"])

    tools = discover_tools(repos_dir)
    steps = WORKFLOWS[name]

    result = WorkflowResult(name=name, steps_run=0, steps_failed=0)

    for step in steps:
        if step.tool not in tools:
            result.errors.append(f"Tool missing: {step.tool}")
            result.steps_failed += 1
            continue

        print(f"  → {step.tool} {step.description}")
        success, stdout, stderr = run_step(step, tools, repos_dir)
        result.steps_run += 1
        if success:
            print(f"    ✓ {stdout.strip()[:80]}")
        else:
            print(f"    ✗ {stderr.strip()[:80]}")
            result.errors.append(f"{step.tool}: {stderr.strip()[:200]}")
            result.steps_failed += 1

    return result
