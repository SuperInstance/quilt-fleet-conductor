"""CLI for quilt-fleet-conductor."""
import argparse
import json
import sys
from pathlib import Path

from .tools import discover_tools, list_tools
from .workflows import WORKFLOWS, run_workflow, run_step, Step


def cmd_list(args):
    tools = discover_tools()
    print(f"Available tools ({len(tools)}):")
    for name, t in tools.items():
        visual = "🎨" if t.has_visual else "  "
        print(f"  {visual} {name}")
        print(f"      {t.description}")


def cmd_workflows(args):
    print("Available workflows:")
    for name, steps in WORKFLOWS.items():
        print(f"\n  • {name} ({len(steps)} steps)")
        for s in steps:
            print(f"      → {s.tool}: {s.description}")


def cmd_run(args):
    name = args.workflow
    print(f"Running workflow: {name}")
    print()
    result = run_workflow(name)
    print()
    print("=" * 60)
    print(f"Workflow: {result.name}")
    print(f"  Steps run:    {result.steps_run}")
    print(f"  Steps failed: {result.steps_failed}")
    if result.errors:
        print(f"  Errors:")
        for e in result.errors:
            print(f"    - {e}")
    if result.steps_failed > 0:
        sys.exit(1)


def cmd_call(args):
    """Call a single tool directly."""
    tools = discover_tools()
    if args.tool not in tools:
        print(f"Unknown tool: {args.tool}")
        print(f"Available: {list(tools.keys())}")
        sys.exit(1)

    step = Step(tool=args.tool, args=args.tool_args)
    print(f"Calling: {args.tool} {' '.join(args.tool_args)}")
    success, stdout, stderr = run_step(step, tools, Path("/workspace/repos"))
    if success:
        print(stdout)
    else:
        print(f"✗ {stderr}")
        sys.exit(1)


def cmd_status(args):
    """Show status of all tools (installed / missing)."""
    tools = discover_tools()
    print(f"Fleet status ({len(tools)} tools discovered):\n")
    for name, t in tools.items():
        # Quick liveness check
        import importlib
        try:
            sys.path.insert(0, str(t.repo))
            mod = importlib.import_module(t.cli_module)
            status = "✓ ready"
        except Exception as e:
            status = f"✗ import error: {type(e).__name__}"
        visual = "🎨" if t.has_visual else "  "
        print(f"  {visual} {name:30s} {status}")


def main():
    p = argparse.ArgumentParser(description="quilt-fleet-conductor — orchestrate all canon tools")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List all available tools").set_defaults(func=cmd_list)
    sub.add_parser("workflows", help="List predefined workflows").set_defaults(func=cmd_workflows)
    sub.add_parser("status", help="Show status of all tools").set_defaults(func=cmd_status)

    p_run = sub.add_parser("run", help="Run a workflow")
    p_run.add_argument("workflow")
    p_run.set_defaults(func=cmd_run)

    p_call = sub.add_parser("call", help="Call a single tool directly")
    p_call.add_argument("tool")
    p_call.add_argument("tool_args", nargs="*")
    p_call.set_defaults(func=cmd_call)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
