"""
claude_web.py — Playwright CDP 連接 Claude Chrome 進行報告送出

架構：
  - 使用者手動開啟 Claude Chrome（--remote-debugging-port=9222）並登入
  - claude_web.py 透過 CDP 連入，偵測已登入的 Claude 分頁
  - 若無 Chrome 或無 Claude 分頁，寫 error 退出
  - 瀏覽器頁面保持開啟，可直接繼續對話
"""

import asyncio, sys, os, tempfile, subprocess, traceback
from playwright.async_api import async_playwright, TimeoutError as PWTimeout

# ── 設定 ────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
CLAUDE_URL  = "https://claude.ai/project/019d4d28-2751-77c6-8a88-1ab1ebaf233e"
CDP_URL     = "http://localhost:9222"

TMP_DONE  = os.path.join(tempfile.gettempdir(), "claude_done.txt")
TMP_ERROR = os.path.join(tempfile.gettempdir(), "claude_error.txt")
LOG_FILE  = os.path.join(SCRIPT_DIR, "claude_web.log")

# Claude ProseMirror 輸入框
INPUT_SEL    = 'div[contenteditable="true"]'
# 送出按鈕（Claude.ai 英文介面）
SEND_BTN_SEL = 'button[aria-label="Send message"]'
# 生成中的停止按鈕
STOP_BTN_SEL = 'button[aria-label="Stop"]'

def log(msg: str):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        import datetime
        f.write(f"[{datetime.datetime.now():%H:%M:%S}] {msg}\n")

# ── 剪貼簿（PowerShell）────────────────────────────────────
def set_clipboard(text: str):
    tmp = os.path.join(tempfile.gettempdir(), "claude_clip.txt")
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

        # ── 連接 Claude Chrome（若未執行則報錯退出）──────────
        try:
            browser = await p.chromium.connect_over_cdp(CDP_URL, timeout=2000)
            log("已連接到現有的 Claude Chrome")
        except Exception:
            log("[錯誤] 找不到執行中的 Chrome（port 9222）")
            with open(TMP_ERROR, "w", encoding="utf-8") as f:
                f.write("no_chrome")
            return

        # ── 確認有已登入的 Claude 分頁 ──────────────────────
        ctx = browser.contexts[0]
        all_pages = ctx.pages
        claude_pages = [
            pg for pg in all_pages
            if "claude.ai" in pg.url
            and "login" not in pg.url
            and "sign" not in pg.url
        ]
        if not claude_pages:
            log("[錯誤] 找不到已登入的 Claude 分頁")
            with open(TMP_ERROR, "w", encoding="utf-8") as f:
                f.write("no_claude_tab")
            return
        log(f"找到 {len(claude_pages)} 個 Claude 分頁")

        # ── 選擇分頁：重用 CLAUDE_URL tab，否則開新頁 ────────
        project_pages = [pg for pg in claude_pages if pg.url.startswith(CLAUDE_URL)]
        if project_pages:
            page = project_pages[0]
            log(f"重用現有 Claude Project 分頁：{page.url}")
        else:
            page = await ctx.new_page()
            log("開新分頁")

        # ── 導航至 Claude Project ──────────────────────────
        log(f"導航至 {CLAUDE_URL}")
        await page.goto(CLAUDE_URL, wait_until="domcontentloaded", timeout=30_000)
        await page.wait_for_timeout(2000)

        # ── 等待輸入框 ──────────────────────────────────────
        log("等待輸入框...")
        try:
            await page.wait_for_selector(INPUT_SEL, timeout=20_000)
            log("輸入框已找到")
        except PWTimeout:
            log(f"[錯誤] 找不到輸入框，URL: {page.url}")
            await page.screenshot(path=os.path.join(SCRIPT_DIR, "claude_debug.png"))
            raise

        await page.wait_for_timeout(500)

        # ── 設定剪貼簿並貼上 ────────────────────────────────
        log("設定剪貼簿...")
        set_clipboard(report_text)
        await page.wait_for_timeout(300)

        input_el = page.locator(INPUT_SEL).first
        await input_el.click()
        await page.wait_for_timeout(200)
        await page.keyboard.press("Control+v")
        await page.wait_for_timeout(500)
        log("貼上完成")

        # ── 點擊送出按鈕 ────────────────────────────────────
        send_btn = page.locator(SEND_BTN_SEL)
        await send_btn.click()
        log("已點擊送出按鈕")

        # ── 等待回應完成：偵測 Stop 按鈕出現再消失 ────────────
        log("等待回應完成...")
        try:
            # 等待 Stop 按鈕出現（開始生成）
            await page.wait_for_selector(STOP_BTN_SEL, timeout=15_000)
            log("生成中...")
            # 等待 Stop 按鈕消失（生成結束）
            await page.wait_for_selector(
                f'{STOP_BTN_SEL}', state="hidden", timeout=180_000
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
            f.write(f"error\n{err}")
