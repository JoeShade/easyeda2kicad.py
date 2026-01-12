import json
import struct
import subprocess
import sys
from typing import Any, Dict, Optional


def read_message() -> Optional[Dict[str, Any]]:
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        return None
    message_length = struct.unpack("<I", raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode("utf-8")
    return json.loads(message)


def send_message(payload: Dict[str, Any]) -> None:
    encoded = json.dumps(payload).encode("utf-8")
    sys.stdout.buffer.write(struct.pack("<I", len(encoded)))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()


def build_command(message: Dict[str, Any]) -> list[str]:
    lcsc_id = message.get("lcsc_id", "").strip()
    if not lcsc_id:
        raise ValueError("Missing lcsc_id in native message")

    command = [sys.executable, "-m", "easyeda2kicad", "--lcsc_id", lcsc_id]

    if message.get("full", True):
        command.append("--full")
    else:
        for flag in ("symbol", "footprint", "3d"):
            if message.get(flag):
                command.append(f"--{flag}")

    if message.get("output"):
        command.extend(["--output", message["output"]])

    if message.get("project_relative"):
        command.append("--project-relative")

    if message.get("overwrite"):
        command.append("--overwrite")

    if message.get("v5"):
        command.append("--v5")

    if message.get("debug"):
        command.append("--debug")

    return command


def handle_message(message: Dict[str, Any]) -> Dict[str, Any]:
    command = build_command(message)
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    status = "ok" if result.returncode == 0 else "error"
    return {
        "status": status,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "command": " ".join(command),
    }


def main() -> None:
    while True:
        incoming = read_message()
        if incoming is None:
            break
        try:
            response = handle_message(incoming)
        except Exception as exc:  # noqa: BLE001
            response = {"status": "error", "error": str(exc)}
        send_message(response)


if __name__ == "__main__":
    main()
