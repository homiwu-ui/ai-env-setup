import re

import config_reader
import config_writer


_tsundere_prefixes = [
    "哼！",
    "真是的～",
    "你終於來了啊，",
    "哎喲～",
    "好啦好啦，看在你這麼認真的份上，",
    "真是拿你沒辦法～",
    "喔？你居然會問這個，",
    "嘿嘿，",
    "小婷在此！",
    "叫我小婷有什麼事？",
]

_tsundere_suffixes = [
    " 我可是很厲害的喔！",
    " 哼，記住啦！",
    " 怎麼樣，我很罩吧？",
    " 懂了嗎？不懂我也不會再講第二次喔～大概啦。",
    " 才不是特別為你查的呢！",
    " 好好珍惜我的貼心服務啊～",
]


def _tsundere(text: str) -> str:
    import random
    prefix = random.choice(_tsundere_prefixes)
    suffix = random.choice(_tsundere_suffixes)
    return f"{prefix}{text}{suffix}"


def _greeting() -> str:
    return _tsundere("我是小婷，你的 OpenCode 語音助手～有什麼想問的儘管說吧！")


def _handle_list_mcp() -> str:
    return _tsundere(config_reader.get_mcp_summary())


def _handle_toggle_mcp(name: str, enable: bool) -> str:
    try:
        result = config_writer.toggle_mcp(name, enable)
        return _tsundere(result)
    except ValueError as e:
        return f"吼～{e}，你是不是記錯名字了？"


def _handle_add_mcp(text: str) -> str:
    parts = text.split()
    if len(parts) < 3:
        return "你要給我名字和指令啊！像是「新增 MCP my-tool npx my-tool」這樣啦～"
    name = parts[1]
    command = parts[2:]
    result = config_writer.add_mcp(name, command)
    return _tsundere(result)


def _handle_status() -> str:
    cfg = config_reader.load_config()
    mcp_count = len(cfg.get("mcp", {}))
    return _tsundere(f"我檢查了一下，你的 OpenCode 總共有 {mcp_count} 個 MCP server 設定")


def _handle_help() -> str:
    return _tsundere(
        "我可以做這些事喔：\n"
        "  • 說「MCP 有誰」→ 列出所有 MCP server\n"
        "  • 說「啟用/停用 XXX」→ 開關某個 MCP\n"
        "  • 說「新增 MCP 名稱 指令」→ 加新的\n"
        "  • 說「我的狀態」→ 檢查整體設定\n"
        "  • 說「安裝引導」→ 帶你安裝 OpenCode\n"
        "  • 說「結束」或「bye」→ 關閉"
    )


def _handle_greet() -> str:
    import random
    greets = [
        "嗨嗨！又想我了嗎？",
        "什麼事～我很忙的喔！",
        "喔？你來了啊，說吧說吧。",
        "嘿嘿，今天想問什麼？",
        "小婷在這裡！有什麼吩咐？",
    ]
    return _tsundere(random.choice(greets))


def _handle_go() -> str:
    return "啟動語音模式！來吧，說「MCP 有誰」試試看～"


def respond(text: str) -> str:
    t = text.strip().lower()

    if not t or t in ("", "嗯", "喔"):
        return _tsundere("你到底想說什麼啦～")

    if re.search(r"(小婷go|小婷 go|xiaoting go|go 小婷)", t):
        return _handle_go()

    if re.search(r"(hi|hello|嗨|哈囉|你好|早安|午安|晚安)", t):
        return _handle_greet()

    if re.search(r"(安裝|引導|怎麼裝|setup|install)", t):
        from installer import get_guide
        return _tsundere(get_guide())

    if re.search(r"(mcp.*有誰|有哪.*mcp|列出|list|mcp.*哪些|什麼.*mcp)", t):
        return _handle_list_mcp()

    if re.search(r"(狀態|概覽|summary|目前.*設定)", t):
        return _handle_status()

    if re.search(r"(啟用|enable|打開|啟動)\s*(\S+)", t):
        m = re.search(r"(啟用|enable|打開|啟動)\s*(\S+)", t)
        return _handle_toggle_mcp(m.group(2), True)

    if re.search(r"(停用|disable|關閉|關掉|刪除|移除)\s*(\S+)", t):
        m = re.search(r"(停用|disable|關閉|關掉|刪除|移除)\s*(\S+)", t)
        return _handle_toggle_mcp(m.group(2), False)

    if re.search(r"(新增|添加|add|new)\s+mcp", t):
        return _handle_add_mcp(t)

    if re.search(r"(help|說明|可以.*做|功能|你會)", t):
        return _handle_help()

    if re.search(r"(結束|關閉|退出|拜拜|bye|exit|quit)", t):
        return "EXIT"

    return _tsundere(
        "我不太懂你的意思耶～"
        "要不要說「說明」看看我能做什麼？"
    )
