import json
import os
import shutil
from datetime import datetime

from config_reader import OPCODE_CONFIG_PATH


def backup() -> str:
    bak_dir = os.path.join(os.path.dirname(OPCODE_CONFIG_PATH), "backups")
    os.makedirs(bak_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak_path = os.path.join(bak_dir, f"opencode.json.{ts}.bak")
    shutil.copy2(OPCODE_CONFIG_PATH, bak_path)
    return bak_path


def toggle_mcp(name: str, enable: bool) -> str:
    bak = backup()
    with open(OPCODE_CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    if "mcp" not in cfg or name not in cfg["mcp"]:
        raise ValueError(f"找不到 MCP server「{name}」")
    cfg["mcp"][name]["enabled"] = enable
    with open(OPCODE_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    status = "啟用" if enable else "停用"
    return f"已{status}「{name}」\n備份檔：{bak}"


def add_mcp(name: str, command: list[str], env: dict | None = None) -> str:
    bak = backup()
    with open(OPCODE_CONFIG_PATH, encoding="utf-8") as f:
        cfg = json.load(f)
    if "mcp" not in cfg:
        cfg["mcp"] = {}
    cfg["mcp"][name] = {
        "type": "local",
        "command": command,
        "enabled": True,
    }
    if env:
        cfg["mcp"][name]["env"] = env
    with open(OPCODE_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    return f"已新增 MCP server「{name}」\n備份檔：{bak}"
