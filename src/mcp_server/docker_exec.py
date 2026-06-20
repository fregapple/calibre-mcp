import subprocess
from typing import List, Dict, Any

from .config import CALIBRE_CONTAINER


class DockerExecutionError(Exception):
    """Raised when a docker exec command fails."""
    pass


def run_docker_command(cmd: List[str]) -> Dict[str, Any]:
    """
    Runs a command inside the Calibre Docker container.
    Returns a dict containing stdout, stderr, returncode, and the full command.
    Raises DockerExecutionError on failure.
    """

    full_cmd = ["docker", "exec", CALIBRE_CONTAINER] + cmd

    result = subprocess.run(
        full_cmd,
        capture_output=True,
        text=True
    )

    output = {
        "cmd": " ".join(full_cmd),
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "returncode": result.returncode
    }

    # Optional: raise on non-zero exit
    if result.returncode != 0:
        raise DockerExecutionError(
            f"Docker command failed: {output['cmd']}\n"
            f"stderr: {output['stderr']}"
        )

    return output
