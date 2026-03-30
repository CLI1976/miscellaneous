#Requires AutoHotkey v2.0
#SingleInstance Force
#Include <UIA>
; 設定當前腳本適用於 Notepad++
#HotIf WinActive("ahk_class Notepad++")
F2::
{
    try {
        ; 取得 Notepad++ 報告內容
        notepadEl1 := UIA.ElementFromHandle("報告暫存.txt - Notepad++ ahk_exe notepad++.exe")
        RepoN := notepadEl1.ElementFromPath("Y").Name
    } catch {
        MsgBox "無法取得報告內容，請確認 Notepad++ 已開啟「報告暫存.txt」"
        return
    }

    ToolTip "⏳ 報告處理中..."
    RunPythonBrowser(RepoN)
}

; 呼叫 Python Playwright 自動化 Gemini Web 版
RunPythonBrowser(RepoN) {
    pythonScript := A_ScriptDir "\gem_web.py"
    tmpIn   := A_Temp "\gem_in.txt"
    tmpDone := A_Temp "\gem_done.txt"

    ; 將報告寫入暫存檔
    try FileDelete(tmpDone)
    f := FileOpen(tmpIn, "w", "UTF-8")
    f.Write(RepoN)
    f.Close()

    ; 執行 Python（非同步，不等待）
    cmd := 'chcp 65001 >nul && python -X utf8 "' pythonScript '" "' tmpIn '"'
    shell := ComObject("WScript.Shell")
    shell.Run(A_ComSpec ' /c ' cmd, 0, false)

    ; 輪詢完成信號，回應完成後更新 Tooltip
    SetTimer(WaitForDone, 200)

    WaitForDone() {
        tmpError := A_Temp "\gem_error.txt"
        if FileExist(tmpDone) {
            SetTimer(WaitForDone, 0)
            ToolTip "✓ 報告修改完成"
            SetTimer(() => ToolTip(), -3000)
        } else if FileExist(tmpError) {
            SetTimer(WaitForDone, 0)
            errorCode := FileRead(tmpError, "UTF-8")
            errorCode := Trim(errorCode, "`r`n ")
            if (errorCode = "no_chrome")
                msg := "⚠ 請先開啟 Gemini Chrome（port 9222）"
            else if (errorCode = "no_gemini_tab")
                msg := "⚠ 請在 Chrome 登入 Gemini 後再按 F2"
            else
                msg := "❌ 執行錯誤，請查看 gem_web.log"
            ToolTip msg
            SetTimer(() => ToolTip(), -5000)
        }
    }

    return
}

;;================================================
;;================================================
