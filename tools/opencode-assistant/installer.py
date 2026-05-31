STEP = 0


def get_guide() -> str:
    return (
        "安裝 OpenCode 很簡單的，我教你～\n\n"
        "步驟 1：去 https://opencode.ai 下載安裝檔\n"
        "步驟 2：安裝後開啟，登入你的 GitHub 帳號\n"
        "步驟 3：在專案目錄執行 opencode 就會啟動了\n\n"
        "需要更詳細的某一步嗎？直接問我～"
    )


def get_step_detail(step: int) -> str:
    details = {
        1: "到 https://opencode.ai 下載對應你系統的版本，Windows 選 .exe，Mac 選 .dmg",
        2: "安裝完第一次啟動會請你授權 GitHub 登入，按指示走就好",
        3: "在終端機進到你的專案資料夾，輸入 opencode 就會啟動對話了",
    }
    return details.get(step, "沒有這一步啦～重新說一次「安裝引導」吧")
