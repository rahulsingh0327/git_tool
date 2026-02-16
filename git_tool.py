import subprocess
from typing import Any, Dict, List


def git_status(repo_path: str) -> Dict[str, Any]:
    """
    Return `git status --porcelain` lines for a repo.

    Args:
        repo_path: Path to local git repository.

    Returns:
        Dict with list of status lines.

    Notes:
        Read-only: does not execute destructive commands.
    """
    try:
        out = subprocess.check_output(["git", "-C", repo_path, "status", "--porcelain"], universal_newlines=True, stderr=subprocess.STDOUT, timeout=10)
        lines = [l for l in out.splitlines()]
        return {"status_lines": lines}
    except subprocess.CalledProcessError as e:
        return {"error": e.output}
    except Exception as e:
        return {"error": str(e)}


def git_log_recent(repo_path: str, n: int = 5) -> List[Dict[str, Any]]:
    """
    Return the most recent `n` commits as dicts with hash, author, date, message.

    Args:
        repo_path: Path to repository.
        n: Number of commits.

    Returns:
        List of commit dictionaries.
    """
    try:
        fmt = "%H%x1f%an%x1f%ad%x1f%s"
        out = subprocess.check_output(["git", "-C", repo_path, "log", f"-n{n}", f"--pretty=format:{fmt}", "--date=iso"], universal_newlines=True, stderr=subprocess.STDOUT, timeout=10)
        commits = []
        for line in out.splitlines():
            parts = line.split("\x1f")
            if len(parts) >= 4:
                commits.append({"hash": parts[0], "author": parts[1], "date": parts[2], "message": parts[3]})
        return commits
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
def git_tool(action: str, repo_path: str, n: int = 5) -> Dict[str, Any]:
    """
    Git helper tool with actions: 'status', 'log'.

    Args:
        action: 'status' or 'log'
        repo_path: Path to local git repo
        n: Number of commits for 'log' action.

    Returns:
        Dict with results or error message.
    """
    action = action.lower()
    if action == "status":
        return git_status(repo_path)
    if action == "log":
        return {"commits": git_log_recent(repo_path, n)}
    raise ValueError("Unsupported git action. Use 'status' or 'log'.")
