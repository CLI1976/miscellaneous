# gem_setup.py — 一次性登入設定
# 由使用者手動開啟 Chrome（無 --enable-automation），登入後擷取 cookie

import asyncio, os, sys
from playwright.async_api import async_playwright

SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
STORAGE_STATE = os.path.join(SCRIPT_DIR, "gem_storagestate.json")
CDP_URL       = "http://localhost:9222"
DEBUG_PROFILE = r"C:\Temp\chrome-debug"
CHROME_EXE    = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CHROME_CMD = (
    f'& "{CHROME_EXE}"'
    f' --remote-debugging-port=9222'
    f' --remote-allow-origins=*'
    f' --user-data-dir="{DEBUG_PROFILE}"'
)

async def main():
    print("=" * 62)
    print("Step 1：開一個新的 PowerShell，執行以下指令：")
    print()
    print(CHROME_CMD)
    print()
    print("Step 2：在開啟的 Chrome 中登入 Google 帳戶")
    print("        （這個 Chrome 是乾淨的新 profile，需要重新登入一次）")
    print()
    print("Step 3：登入完成後，回到這裡按 Enter")
    print("=" * 62)
    input(">>> 已登入，按 Enter 儲存... ")

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp(CDP_URL)
        except Exception:
            print()
            print("[錯誤] 無法連接 Chrome，請確認：")
            print("  - Chrome 是否已用上方指令開啟？")
            print("  - 可在瀏覽器開 http://localhost:9222/json 確認")
            sys.exit(1)

        ctx = browser.contexts[0]
        await ctx.storage_state(path=STORAGE_STATE)
        # 不呼叫 browser.close()，Chrome 繼續運行

    print()
    print(f"✓ 已儲存：{STORAGE_STATE}")
    print("設定完成！日後直接用 gem_web.py 即可。")
    print("（cookie 失效時重跑此腳本即可，不需要再修改 Chrome 捷徑）")

asyncio.run(main())
