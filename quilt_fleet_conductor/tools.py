"""Tool registry — what tools the conductor can call."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional


@dataclass
class Tool:
    name: str
    description: str
    repo: Path
    cli_module: str
    cli_func: str = "main"
    has_visual: bool = False  # HTML viewer, player, etc.


# Built-in tools — discover them in /workspace/repos/
def discover_tools(repos_dir: Path = Path("/workspace/repos")) -> Dict[str, Tool]:
    """Discover all quilt-canon-* and quilt-multi-* repos as tools."""
    tools = {}
    for repo_dir in sorted(repos_dir.iterdir()):
        if not repo_dir.is_dir():
            continue
        if not (repo_dir.name.startswith("quilt-canon-") or repo_dir.name.startswith("quilt-multi-")):
            continue
        # Find the Python CLI module
        candidates = list(repo_dir.glob("*/__init__.py")) + list(repo_dir.glob("*.py"))
        cli_module = None
        for c in candidates:
            parts = c.relative_to(repo_dir).parts
            if c.name == "__init__.py":
                cli_module = parts[0]
                break
        if not cli_module:
            continue
        # Check for HTML output
        has_visual = any(repo_dir.rglob("*.html"))
        tools[repo_dir.name] = Tool(
            name=repo_dir.name,
            description=_infer_description(repo_dir.name),
            repo=repo_dir,
            cli_module=cli_module,
            has_visual=has_visual,
        )
    return tools


def _infer_description(name: str) -> str:
    return {
        "quilt-canon-mcp": "MCP server exposing canon as tools for AI agents",
        "quilt-canon-search": "TF-IDF search over canon lore",
        "quilt-canon-graph": "Knowledge graph of canon lore + vis-network viewer",
        "quilt-canon-radio": "TTS broadcast via ElevenLabs",
        "quilt-canon-game": "Interactive browser game — walk the substrate",
        "quilt-canon-book": "Compile canon lore into a print-ready book",
        "quilt-canon-cli": "CLI for canon exploration",
        "quilt-canon-explorer": "HTML canon archive browser",
        "quilt-canon-gen": "ZAI canon generation",
        "quilt-canon-iterator": "Self-improving canon iteration",
        "quilt-multi-oracle": "Multi-model JEV chord",
    }.get(name, f"{name}")


def list_tools(repos_dir: Path = Path("/workspace/repos")) -> List[str]:
    """List all available tools."""
    return sorted(discover_tools(repos_dir).keys())
