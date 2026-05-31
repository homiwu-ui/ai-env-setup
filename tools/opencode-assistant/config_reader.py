import json
import os

OPCODE_CONFIG_PATH = os.path.expanduser(
    r"C:\Users\88690\.config\opencode\opencode.json"
)


def load_config() -> dict:
    if not os.path.exists(OPCODE_CONFIG_PATH):
        return {}
    with open(OPCODE_CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def get_mcp_summary() -> str:
    cfg = load_config()
    mcps = cfg.get("mcp", {})
    if not mcps:
        return "目前沒有設定任何 MCP server 耶，好空虛～"

    lines = []
    enabled = []
    disabled = []
    for name, info in mcps.items():
        status = "✅ 啟用" if info.get("enabled", False) else "❌ 停用"
        if info.get("enabled", False):
            enabled.append(name)
        else:
            disabled.append(name)

    lines.append(f"你總共設定了 {len(mcps)} 個 MCP server：")
    if enabled:
        lines.append(f"   啟用中：{'、'.join(enabled)}")
    if disabled:
        lines.append(f"   已停用：{'、'.join(disabled)}")
    return "\n".join(lines)


def get_mcp_detail(name: str) -> dict | None:
    cfg = load_config()
    return cfg.get("mcp", {}).get(name)


def list_mcp_names() -> list[str]:
    cfg = load_config()
    return list(cfg.get("mcp", {}).keys())


def get_config_preview() -> str:
    cfg = load_config()
    return json.dumps(cfg, indent=2, ensure_ascii=False)
