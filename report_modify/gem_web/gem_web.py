"""
gem_web.py — Playwright CDP 連接 Gemini Chrome 進行報告修改

架構：
  - 一個專用的「Gemini Chrome」始終在背景執行（C:\Temp\chrome-debug profile）
  - gem_web.py 透過 CDP 連入，不啟動新 Chrome，不加 automation flags
  - Google 完全認得這個 Chrome session，不會被強制登出
  - 瀏覽器頁面保持開啟，可直接繼續對話
"""

import asyncio, sys, os, tempfile, subprocess, traceback
from playwright.async_api import async_playwright, TimeoutError as PWTimeout

# ── 設定 ────────────────────────────────────────────────────
SCRIPT_DIR     = os.path.dirname(os.path.abspath(__file__))
GEM_URL        = "https://gemini.google.com/gem/ecabec39c76d"
CHROME_EXE     = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_PROFILE = r"C:\Temp\chrome-debug"
CDP_URL        = "http://localhost:9222"

TMP_DONE  = os.path.join(tempfile.gettempdir(), "gem_done.txt")
TMP_ERROR = os.path.join(tempfile.gettempdir(), "gem_error.txt")
LOG_FILE  = os.path.join(SCRIPT_DIR, "gem_web.log")

INPUT_SEL = 'rich-textarea div[role="textbox"]'

def log(msg: str):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        import datetime
        f.write(f"[{datetime.datetime.now():%H:%M:%S}] {msg}\n")

# ── 剪貼簿（PowerShell）────────────────────────────────────
def set_clipboard(text: str):
    tmp = os.path.join(tempfile.gettempdir(), "gem_clip.txt")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    subprocess.run(
        ["powershell", "-NonInteractive", "-Command",
         f'Get-Content -Path "{tmp}" -Encoding UTF8 -Raw | Set-Clipboard'],
        check=False, capture_output=True
    )

# ── 主流程 ──────────────────────────────────────────────────
async def run(report_text: str):
    async with async_playwright() as p:

        # ── 連接 Gemini Chrome（若未執行則自動啟動）──────────
        browser = None
        try:
            browser = await p.chromium.connect_over_cdp(CDP_URL, timeout=2000)
            log("已連接到現有的 Gemini Chrome")
        except Exception:
            log("Gemini Chrome 未執行，正在啟動...")
            subprocess.Popen([
                CHROME_EXE,
                "--remote-debugging-port=9222",
                "--remote-allow-origins=*",
                f"--user-data-dir={CHROME_PROFILE}",
            ])
            await asyncio.sleep(4)
            browser = await p.chromium.connect_over_cdp(CDP_URL, timeout=10_000)
            log("Gemini Chrome 已啟動並連接")

        # 使用現有的登入 context（第一個 context = 使用者的 session）
        ctx = browser.contexts[0]
        page = await ctx.new_page()

        # ── 導航至 Custom Gem ──────────────────────────────
        log(f"導航至 {GEM_URL}")
        await page.goto(GEM_URL, wait_until="domcontentloaded", timeout=30_000)
        await page.wait_for_timeout(2000)

        # ── 確認已登入 ──────────────────────────────────────
        if "accounts.google.com" in page.url or "signin" in page.url:
            log("[錯誤] 未登入 Google，請重新執行 gem_setup.py")
            with open(TMP_ERROR, "w", encoding="utf-8") as f:
                f.write("not_logged_in")
            await page.close()
            return

        # ── 等待輸入框 ──────────────────────────────────────
        log("等待輸入框...")
        try:
            await page.wait_for_selector(INPUT_SEL, timeout=20_000)
            log("輸入框已找到")
        except PWTimeout:
            log(f"[錯誤] 找不到輸入框，URL: {page.url}")
            await page.screenshot(path=os.path.join(SCRIPT_DIR, "gem_debug.png"))
            raise

        await page.wait_for_timeout(500)

        # ── 設定剪貼簿並貼上 ────────────────────────────────
        log("設定剪貼簿...")
        set_clipboard(report_text)
        await page.wait_for_timeout(300)

        input_el = page.locator(INPUT_SEL)
        await input_el.click()
        await page.wait_for_timeout(200)
        await page.keyboard.press("Control+v")
        await page.wait_for_timeout(500)
        log("貼上完成")

        # ── 點擊送出按鈕 ────────────────────────────────────
        send_btn = page.locator('button[aria-label="傳送訊息"]')
        await send_btn.click()
        log("已點擊送出按鈕")

        # ── 等待回應完成 ─────────────────────────────────────
        log("等待回應完成...")
        await page.wait_for_timeout(1500)
        try:
            await page.wait_for_function(
                'document.querySelector(\'button[aria-label="傳送訊息"]\')?.disabled',
                timeout=15_000, polling=300
            )
            log("生成中...")
            await page.wait_for_function(
                '!document.querySelector(\'button[aria-label="傳送訊息"]\')?.disabled',
                timeout=180_000, polling=1000
            )
            log("回應完成")
        except PWTimeout:
            log("等待逾時，繼續...")

        # ── 完成信號 ─────────────────────────────────────────
        with open(TMP_DONE, "w", encoding="utf-8") as f:
            f.write("done")
        log("信號已寫入")

        # ── 頁面保持開啟，供後續對話 ─────────────────────────
        log("頁面保持開啟，等待使用者關閉...")
        loop = asyncio.get_running_loop()
        closed = loop.create_future()
        page.on("close", lambda: closed.set_result(None) if not closed.done() else None)
        await closed
        log("頁面已關閉")


# ── Entry Point ─────────────────────────────────────────────
if __name__ == "__main__":
    for f in [TMP_DONE, TMP_ERROR]:
        try: os.remove(f)
        except FileNotFoundError: pass

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        text = open(arg, encoding="utf-8").read().strip() if os.path.isfile(arg) else arg
    else:
        text = "Test: 請回覆『收到測試訊息』"

    log(f"輸入文字長度：{len(text)} 字元")

    try:
        asyncio.run(run(text))
    except Exception:
        err = traceback.format_exc()
        log(f"[例外]\n{err}")
        with open(TMP_ERROR, "w", encoding="utf-8") as f:
            f.write(err)
