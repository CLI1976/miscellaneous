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

    ToolTip "正在執行修改報告..."
    RunPythonBrowser(RepoN)
    ; Tooltip 由 Timer 在視窗開啟後自動關閉（見 RunPythonBrowser）
}

; 呼叫 Python 執行瀏覽器自動化
; 參數: patientID, uid, pwd, x, y, width, height
RunPythonBrowser(RepoN) {
    pythonScript := A_ScriptDir "\gem.py"
    tmpIn  := A_Temp "\gem_in.txt"
    tmpOut := A_Temp "\gem_out.txt"

    ; 將報告寫入暫存檔（避免 command line 引號跳脫問題）
    try FileDelete(tmpOut)
    f := FileOpen(tmpIn, "w", "UTF-8")
    f.Write(RepoN)
    f.Close()

    ; 清除舊的 ready signal
    tmpReady := A_Temp "\gem_ready.txt"
    try FileDelete(tmpReady)

    ; 執行 Python（非同步，不等待；PyQt6 視窗開啟後會寫 signal 檔）
    cmd := 'chcp 65001 >nul && python -X utf8 "' pythonScript '" "' tmpIn '"'
    shell := ComObject("WScript.Shell")
    shell.Run(A_ComSpec ' /c ' cmd, 0, false)  ; false = 不等待

    ; 輪詢 signal 檔，視窗開啟後關閉 Tooltip
    SetTimer(WaitForWindow, 300)

    WaitForWindow() {
        if FileExist(tmpReady) {
            ToolTip
            SetTimer(WaitForWindow, 0)
        }
    }

    return
}

;;================================================
;;================================================
