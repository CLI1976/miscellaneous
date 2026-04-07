#Requires AutoHotkey v2.0
#SingleInstance Force
#Include <UIA>
; 設定當前腳本適用於 Notepad++
#HotIf WinActive("ahk_class Notepad++")

;#########TRAYICON - Base64 Version;################
;#########步驟 1：線上轉換 .ico 為 Base64;################
;################
;################
Base64ToIcon(base64String) {
    ; Base64 解碼
    size := 0
    DllCall("Crypt32\CryptStringToBinary"
        , "Str", base64String
        , "UInt", 0
        , "UInt", 0x1  ; CRYPT_STRING_BASE64
        , "Ptr", 0
        , "UInt*", &size
        , "Ptr", 0
        , "Ptr", 0)
    
    buf := Buffer(size)
    DllCall("Crypt32\CryptStringToBinary"
        , "Str", base64String
        , "UInt", 0
        , "UInt", 0x1
        , "Ptr", buf
        , "UInt*", &size
        , "Ptr", 0
        , "Ptr", 0)
    
    ; 寫入臨時檔案
    iconPath := A_Temp "\This_icon.png"
    f := FileOpen(iconPath, "w")
    f.RawWrite(buf, size)
    f.Close()
    
    return iconPath
}

; 在這裡貼上你的 Base64 字串（可以分多行）
iconBase64 := "
(
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAsQAAALEBxi1JjQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAATqSURBVFiFrZd7TBRXFIe/dZedXZ/ISlG05e0L0VIkVARCLKhYxcSikUZRG7EWi2JEo6ZFpWIqvkBEKSpIomhtq219oTXFKsa2VtSgiKBULAZTRRHYhZ3dZfsHhQICu0v3l0wyc+7vnvPdM5M7M2CZ5IJSmSKXCzVyQXgpKJW7ALmFOdpJaolZUCq3O7t5LFm2PrFfYOg0xePysrHq+jo7g15/vqcAEkvMckGoWb9tzwBbOxUANdXP2bImtkbUagf2FEDW5txoyixqtbQUB7BVDULUam3NmUsXi20bNN4sefCawXukO8bkaCRr9pNy+ESnmePmzWr1dJWjKwBZx8C/5i4LmVLH+Z0BdQsAYHyU2HouuG+iWtOIMTm620TVmkYEGymNZRtaYxLnBFO8nQO0Vfxifxw35yLqDd365DIpq6MnmixoMUDS2lCS1oZanNhqAC2qV4vsPXyd42dLKSmrQqc34DRsEFMCXVm+cDweLirTSTpRL3NMV/94zPBJ6Vy5I2Ppqs2cyS/gyvVbJO3aT4MwBv+IQ+w4cK1HACY78PvtSmZ98i0btuxE2bs36RkZlBYXIzZqcPX0IiI8nKzcE8THLkErGlgfE2A9AFFnYG7s96zb+CV/VVaSmrabgYsTGLIqE4lcgfrOb6Rlb2FcQQFpmTnMnx3O1CA33hkzxGyAbm/BsR+LcHzLFTcPD1J27WTovp+xnbEQmWow0n629J0wBce0PG5XVXPu3FkWRMew9atfzS5uEuCHiw8JC5/NwawsBsxdjtzRud34JJWM/T522MUmk5NziLDp4eRduo/B0GQdgNJHL3B1c+NuyX16+wS3G/O3lbHRXUHKIxHF8HFo1GoMBj2CQuDvarV1AFrUqFFDUxM+/aWkjlISMFDG1hEKYosbuFtvAIkEqY0coxGM5ryWzAUY4aKi/OFDxnl5oSn8hdt1zbthykgFcfcaWq+15cUIchtkMhnaxkbeUPWxDsDMEDdOn/yaBVFR1H2XgaaijFUlDcwv0nCjtrm4USfyMjWemGWfknfmFFODRyCVmtVY0wBzpnvyrKqCP8vLiY+P5+nKGTw7eYCix1U0qWupv3aBJx8H4+fiyHshIRzct5uVH/maXdwkgCCXcSRlJtuTEnCwtycjfQ/D712iMsqXB+GuSHMSWbloHnHLV6ATdfgHBvHZjsuoNSL3y5+bBWByJ/R7exgn9n1A5IrVeHn7EhkRyaaEBCS9JDyprCT/Qh5ztm5mkErF3uxc9uz8EtfAVBoatNYBAAjwdaL4p6Vk5t7gUHoixaVVaEUdTm/aMzXIhcJT0Rw7fZeYRR/iOWo0o1X9iZvgSeTRfG4V3ug292ufZN4j3dt9kJirpiYjfuGZ9BXhdNRk+shlXCx7QuTxAp6/qu1Yq1WmO+D0effjFV8AUKfWotfpGT90MH3kzWlDPIZydE4A72dfaBL1+onA1Y7TrdYBgJraRkLnZhPsYM+2ML/W+OXyKqZl5anVon46cMkyADM70FMIq3bgdQgHtoX9ty90BmH+lmWBbPsryDuygO35t1h3vrA1HuQ6hIixLgqljSyVTh5K482SB0aa/3KsdozycDeumeStNyZHGxMn+4h9BZsKYHBLUZN/Rv9Xr2pqCH53PBOcHcSiqhdP67U6P+BpZ16rr77tIZNKvqHNylv0D0maIY9V2CgeAAAAAElFTkSuQmCC
)"

; 設定圖示
iconPath := Base64ToIcon(iconBase64)
TraySetIcon(iconPath)

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

F3::
{
    try {
        notepadEl1 := UIA.ElementFromHandle("報告暫存.txt - Notepad++ ahk_exe notepad++.exe")
        RepoN := notepadEl1.ElementFromPath("Y").Name
    } catch {
        MsgBox "無法取得報告內容，請確認 Notepad++ 已開啟「報告暫存.txt」"
        return
    }

    ToolTip "⏳ 傳送至 Claude 中..."
    RunClaudeBrowser(RepoN)
}

; 呼叫 Python Playwright 自動化 Claude Web 版
RunClaudeBrowser(RepoN) {
    pythonScript := A_ScriptDir "\claude_web.py"
    tmpIn   := A_Temp "\claude_in.txt"
    tmpDone := A_Temp "\claude_done.txt"

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
    SetTimer(WaitForClaudeDone, 200)

    WaitForClaudeDone() {
        tmpError := A_Temp "\claude_error.txt"
        if FileExist(tmpDone) {
            SetTimer(WaitForClaudeDone, 0)
            ToolTip "✓ Claude 回應完成"
            SetTimer(() => ToolTip(), -3000)
        } else if FileExist(tmpError) {
            SetTimer(WaitForClaudeDone, 0)
            errorCode := FileRead(tmpError, "UTF-8")
            errorCode := Trim(errorCode, "`r`n ")
            if (errorCode = "no_chrome")
                msg := "⚠ 請先開啟 Chrome（port 9222）"
            else if (errorCode = "no_claude_tab")
                msg := "⚠ 請在 Chrome 登入 Claude 後再按 F3"
            else
                msg := "❌ 執行錯誤，請查看 claude_web.log"
            ToolTip msg
            SetTimer(() => ToolTip(), -5000)
        }
    }

    return
}

F5::
{
    try {
        notepadEl1 := UIA.ElementFromHandle("報告暫存.txt - Notepad++ ahk_exe notepad++.exe")
        RepoN := notepadEl1.ElementFromPath("Y").Name
    } catch {
        MsgBox "無法取得報告內容，請確認 Notepad++ 已開啟「報告暫存.txt」"
        return
    }

    ToolTip "⏳ 同時送出至 Gemini & Claude..."
    RunBothBrowsers(RepoN)
}

; 同時呼叫兩個 Python，單一 Timer 追蹤雙邊完成
RunBothBrowsers(RepoN) {
    gemScript   := A_ScriptDir "\gem_web.py"
    claudeScript := A_ScriptDir "\claude_web.py"
    gemIn    := A_Temp "\gem_in.txt"
    gemDone  := A_Temp "\gem_done.txt"
    claudeIn   := A_Temp "\claude_in.txt"
    claudeDone := A_Temp "\claude_done.txt"

    try FileDelete(gemDone)
    try FileDelete(claudeDone)

    f := FileOpen(gemIn, "w", "UTF-8")
    f.Write(RepoN)
    f.Close()
    f := FileOpen(claudeIn, "w", "UTF-8")
    f.Write(RepoN)
    f.Close()

    shell := ComObject("WScript.Shell")
    shell.Run(A_ComSpec ' /c chcp 65001 >nul && python -X utf8 "' gemScript '" "' gemIn '"', 0, false)
    shell.Run(A_ComSpec ' /c chcp 65001 >nul && python -X utf8 "' claudeScript '" "' claudeIn '"', 0, false)

    SetTimer(WaitForBothDone, 200)

    WaitForBothDone() {
        gemErr   := A_Temp "\gem_error.txt"
        claudeErr := A_Temp "\claude_error.txt"
        gemOk    := FileExist(gemDone)
        claudeOk := FileExist(claudeDone)
        gemFail  := FileExist(gemErr)
        claudeFail := FileExist(claudeErr)

        ; 兩邊都結束才停 Timer
        if ((gemOk || gemFail) && (claudeOk || claudeFail)) {
            SetTimer(WaitForBothDone, 0)
            if (gemOk && claudeOk)
                msg := "✓ Gemini & Claude 均完成"
            else if (gemOk && claudeFail)
                msg := "✓ Gemini 完成　❌ Claude 失敗"
            else if (gemFail && claudeOk)
                msg := "❌ Gemini 失敗　✓ Claude 完成"
            else
                msg := "❌ Gemini & Claude 均失敗"
            ToolTip msg
            SetTimer(() => ToolTip(), -4000)
            return
        }

        ; 其中一邊先完成時顯示進度
        if (gemOk && !claudeOk && !claudeFail)
            ToolTip "✓ Gemini 完成，等待 Claude..."
        else if (claudeOk && !gemOk && !gemFail)
            ToolTip "✓ Claude 完成，等待 Gemini..."
    }

    return
}

;;================================================
;;================================================
