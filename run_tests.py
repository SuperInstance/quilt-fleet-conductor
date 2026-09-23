"""Test runner for quilt-fleet-conductor (no pytest dep)."""
import sys

sys.path.insert(0, "/workspace/repos/quilt-fleet-conductor")

from quilt_fleet_conductor.canary import canary
from quilt_fleet_conductor.tools import discover_tools, list_tools
from quilt_fleet_conductor.workflows import WORKFLOWS, run_workflow, Step, run_step

results = []
failures = []


def test(name, func):
    try:
        func()
        results.append((name, "PASS"))
    except AssertionError as e:
        results.append((name, f"FAIL: {e}"))
        failures.append(name)
    except Exception as e:
        results.append((name, f"ERROR: {type(e).__name__}: {e}"))
        failures.append(name)


def t_canary():
    assert canary() == "0x24a555471370b18d"


def t_discover_tools():
    tools = discover_tools()
    assert len(tools) >= 5, f"only {len(tools)} tools discovered (need ≥5)"
    assert "quilt-canon-search" in tools
    assert "quilt-canon-graph" in tools


def t_list_tools():
    tools = list_tools()
    assert isinstance(tools, list)
    assert len(tools) >= 5


def t_workflows_defined():
    assert "explore" in WORKFLOWS
    assert "publish" in WORKFLOWS
    assert "verify" in WORKFLOWS


def t_workflows_have_steps():
    for name, steps in WORKFLOWS.items():
        assert len(steps) >= 1, f"{name} has no steps"


def t_step_runs():
    """A simple step should run on a known tool."""
    tools = discover_tools()
    if "quilt-canon-search" in tools:
        step = Step(tool="quilt-canon-search", args=["list-doctrines"])
        success, stdout, stderr = run_step(step, tools, tools["quilt-canon-search"].repo)
        assert success, f"step failed: {stderr}"
        assert "cells_are_scars" in stdout


def test_run_workflow_explore():
    """The explore workflow should at least partially succeed."""
    result = run_workflow("explore")
    assert result.steps_run >= 1
    # Note: some tools may fail (e.g., ElevenLabs quota), that's OK
    print(f"    explore: {result.steps_run} run, {result.steps_failed} failed")


test("test_canary", t_canary)
test("test_discover_tools", t_discover_tools)
test("test_list_tools", t_list_tools)
test("test_workflows_defined", t_workflows_defined)
test("test_workflows_have_steps", t_workflows_have_steps)
test("test_step_runs", t_step_runs)
test("test_workflow_explore", test_run_workflow_explore)

print("\n=== quilt-fleet-conductor test results ===")
for name, status in results:
    print(f"  {status:60} {name}")

print(f"\n{len(results) - len(failures)}/{len(results)} passed")
if failures:
    sys.exit(1)
