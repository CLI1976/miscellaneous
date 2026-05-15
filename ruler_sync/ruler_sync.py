"""
雙螢幕比例尺同步工具 - 純 Win32 ctypes
用法: python ruler_sync.py
右鍵關閉
"""
import ctypes
import ctypes.wintypes as wt
import sys

# ── 設定區 ────────────────────────────────────────
RULER_W     = 44
RULER_MIN_H = 80
RESIZE_ZONE = 14
TICK_BIG    = 100
TICK_MID    = 50
TICK_SM     = 10
INIT_H      = 400
A_X, A_Y    = 20,   100
B_X, B_Y    = 1940, 100
COLOR_A     = 0xFF901E   # COLORREF (BGR) for #1E90FF
COLOR_B     = 0x71B33C   # COLORREF (BGR) for #3CB371
BG_COLOR    = 0x2E1A1A
DIM_COLOR   = 0x554433
# ─────────────────────────────────────────────────

u32 = ctypes.windll.user32
gdi = ctypes.windll.gdi32
k32 = ctypes.windll.kernel32

# 設定回傳型別
u32.DefWindowProcW.restype  = ctypes.c_ssize_t
u32.DefWindowProcW.argtypes = [wt.HWND, wt.UINT, wt.WPARAM, ctypes.c_ssize_t]
u32.CreateWindowExW.restype = wt.HWND
u32.BeginPaint.restype      = wt.HDC
u32.GetDC.restype           = wt.HDC
gdi.CreateCompatibleDC.restype      = ctypes.c_void_p
gdi.CreateCompatibleBitmap.restype  = ctypes.c_void_p
gdi.SelectObject.restype            = ctypes.c_void_p
gdi.CreateSolidBrush.restype        = ctypes.c_void_p
gdi.CreatePen.restype               = ctypes.c_void_p
gdi.CreateFontW.restype             = ctypes.c_void_p
gdi.SelectObject.argtypes           = [ctypes.c_void_p, ctypes.c_void_p]
gdi.DeleteObject.argtypes           = [ctypes.c_void_p]
gdi.DeleteDC.argtypes               = [ctypes.c_void_p]
gdi.BitBlt.restype                  = ctypes.c_int
gdi.BitBlt.argtypes                 = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
                                        ctypes.c_int, ctypes.c_int, ctypes.c_void_p,
                                        ctypes.c_int, ctypes.c_int, ctypes.c_uint32]
gdi.SetBkMode.argtypes              = [ctypes.c_void_p, ctypes.c_int]
gdi.SetTextColor.argtypes           = [ctypes.c_void_p, ctypes.c_uint32]
gdi.MoveToEx.argtypes               = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
gdi.LineTo.argtypes                 = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
gdi.TextOutW.argtypes               = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
                                        ctypes.c_wchar_p, ctypes.c_int]
gdi.CreateCompatibleBitmap.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
gdi.CreateCompatibleDC.argtypes     = [ctypes.c_void_p]
gdi.CreatePen.argtypes              = [ctypes.c_int, ctypes.c_int, ctypes.c_uint32]
gdi.CreateSolidBrush.argtypes       = [ctypes.c_uint32]
u32.FillRect.argtypes               = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
u32.GetDC.restype                   = ctypes.c_void_p
u32.GetDC.argtypes                  = [wt.HWND]
u32.BeginPaint.restype              = ctypes.c_void_p
u32.ReleaseDC.argtypes              = [wt.HWND, ctypes.c_void_p]

WS_POPUP        = 0x80000000
WS_VISIBLE      = 0x10000000
WS_EX_TOPMOST   = 0x00000008
WS_EX_TOOLWINDOW= 0x00000080
WS_EX_LAYERED   = 0x00080000
CS_HREDRAW = 0x0002
CS_VREDRAW = 0x0001

WM_DESTROY     = 0x0002
WM_PAINT       = 0x000F
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP   = 0x0202
WM_MOUSEMOVE   = 0x0200
WM_RBUTTONUP   = 0x0205
WM_SETCURSOR   = 0x0020
IDC_ARROW      = 32512
IDC_SIZENS     = 32645

LWA_ALPHA = 0x02

def LOWORD(val): return val & 0xFFFF
def HIWORD(val): return (val >> 16) & 0xFFFF
def GET_X(lp):
    v = LOWORD(lp)
    return v - 0x10000 if v > 0x7FFF else v
def GET_Y(lp):
    v = HIWORD(lp)
    return v - 0x10000 if v > 0x7FFF else v

rulers = {}

class Ruler:
    def __init__(self, name, color):
        self.name  = name
        self.color = color
        self.h     = INIT_H
        self.hwnd  = None
        self.other = None
        self._drag = None
        self._sx = self._sy = self._wax = self._way = self._sh = 0

    def get_rect(self):
        r = wt.RECT()
        u32.GetWindowRect(self.hwnd, ctypes.byref(r))
        return r

    def paint(self, hdc, w, h):
        mdc = gdi.CreateCompatibleDC(hdc)
        bm  = gdi.CreateCompatibleBitmap(hdc, w, h)
        old = gdi.SelectObject(mdc, bm)

        # 背景
        br = gdi.CreateSolidBrush(BG_COLOR)
        rc = wt.RECT(0, 0, w, h)
        u32.FillRect(mdc, ctypes.byref(rc), br)
        gdi.DeleteObject(br)

        # 字型
        font = gdi.CreateFontW(8,0,0,0,400,0,0,0,1,0,0,0,0,"Courier New")
        gdi.SelectObject(mdc, font)
        gdi.SetBkMode(mdc, 1)

        # 刻度
        c = self.color
        pen = gdi.CreatePen(0, 1, c)
        dim_pen = gdi.CreatePen(0, 1, DIM_COLOR)

        py = 0
        while py <= h:
            if py % TICK_BIG == 0:
                gdi.SelectObject(mdc, pen)
                gdi.SetTextColor(mdc, c)
                gdi.MoveToEx(mdc, 0, py, None)
                gdi.LineTo(mdc, w, py)
                gdi.TextOutW(mdc, 2, py+1, f"{py}px", len(f"{py}px"))
            elif py % TICK_MID == 0:
                gdi.SelectObject(mdc, pen)
                gdi.MoveToEx(mdc, w//2, py, None)
                gdi.LineTo(mdc, w, py)
            elif py % TICK_SM == 0:
                gdi.SelectObject(mdc, dim_pen)
                gdi.MoveToEx(mdc, w-8, py, None)
                gdi.LineTo(mdc, w, py)
            py += TICK_SM

        # 外框
        gdi.SelectObject(mdc, pen)
        gdi.MoveToEx(mdc, 0,   0,   None); gdi.LineTo(mdc, w-1, 0)
        gdi.MoveToEx(mdc, w-1, 0,   None); gdi.LineTo(mdc, w-1, h-1)
        gdi.MoveToEx(mdc, w-1, h-1, None); gdi.LineTo(mdc, 0,   h-1)
        gdi.MoveToEx(mdc, 0,   h-1, None); gdi.LineTo(mdc, 0,   0)

        # 底部高度文字
        gdi.SetTextColor(mdc, c)
        gdi.TextOutW(mdc, 2, h-12, f"{h}px", len(f"{h}px"))

        # drag 把手
        drag_br = gdi.CreateSolidBrush(c)
        drc = wt.RECT(1, h-RESIZE_ZONE, w-1, h-1)
        u32.FillRect(mdc, ctypes.byref(drc), drag_br)
        gdi.DeleteObject(drag_br)
        gdi.SetTextColor(mdc, BG_COLOR)
        gdi.TextOutW(mdc, 5, h-RESIZE_ZONE+3, "drag", 4)

        gdi.BitBlt(hdc, 0, 0, w, h, mdc, 0, 0, 0xCC0020)
        gdi.SelectObject(mdc, old)
        gdi.DeleteObject(bm)
        gdi.DeleteObject(font)
        gdi.DeleteObject(pen)
        gdi.DeleteObject(dim_pen)
        gdi.DeleteDC(mdc)


WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_ssize_t, wt.HWND, wt.UINT, wt.WPARAM, ctypes.c_ssize_t)
_procs  = []   # 防止 GC

def make_window(ruler, x, y):
    hinstance = k32.GetModuleHandleW(None)
    cls_name  = f"RulerCls{ruler.name}"

    class WNDCLASSEXW(ctypes.Structure):
        _fields_ = [
            ("cbSize",        ctypes.c_uint),
            ("style",         ctypes.c_uint),
            ("lpfnWndProc",   WNDPROC),
            ("cbClsExtra",    ctypes.c_int),
            ("cbWndExtra",    ctypes.c_int),
            ("hInstance",     wt.HANDLE),
            ("hIcon",         wt.HANDLE),
            ("hCursor",       wt.HANDLE),
            ("hbrBackground", wt.HANDLE),
            ("lpszMenuName",  wt.LPCWSTR),
            ("lpszClassName", wt.LPCWSTR),
            ("hIconSm",       wt.HANDLE),
        ]

    def wndproc(hwnd, msg, wp, lp):
        r = rulers.get(hwnd)

        if msg == WM_PAINT:
            ps  = ctypes.create_string_buffer(72)  # PAINTSTRUCT = 72 bytes
            hdc = u32.BeginPaint(hwnd, ps)
            if hdc and r:
                rc = wt.RECT()
                u32.GetClientRect(hwnd, ctypes.byref(rc))
                w = rc.right  if rc.right  > 0 else RULER_W
                h = rc.bottom if rc.bottom > 0 else r.h
                r.paint(hdc, w, h)
            u32.EndPaint(hwnd, ps)
            return 0

        elif msg == WM_LBUTTONDOWN:
            if r:
                cx = GET_X(lp)
                cy = GET_Y(lp)
                pt = wt.POINT(cx, cy)
                u32.ClientToScreen(hwnd, ctypes.byref(pt))
                wr = r.get_rect()
                r._sx  = pt.x;  r._sy  = pt.y
                r._wax = wr.left; r._way = wr.top
                r._sh  = wr.bottom - wr.top
                r._drag = "resize" if cy >= r._sh - RESIZE_ZONE else "move"
                u32.SetCapture(hwnd)
            return 0

        elif msg == WM_MOUSEMOVE:
            if r and r._drag:
                pt = wt.POINT(GET_X(lp), GET_Y(lp))
                u32.ClientToScreen(hwnd, ctypes.byref(pt))
                dx = pt.x - r._sx
                dy = pt.y - r._sy
                wr  = r.get_rect()

                if r._drag == "move":
                    nx = r._wax + dx
                    ny = r._way + dy
                    u32.SetWindowPos(hwnd, 0, nx, ny, 0, 0, 0x0015)
                    if r.other:
                        owr = r.other.get_rect()
                        u32.SetWindowPos(r.other.hwnd, 0,
                                         owr.left, ny, 0, 0, 0x0015)

                elif r._drag == "resize":
                    new_h = max(r._sh + dy, RULER_MIN_H)
                    ww = wr.right - wr.left
                    u32.SetWindowPos(hwnd, 0,
                                     wr.left, r._way, ww, new_h, 0x0014)
                    u32.InvalidateRect(hwnd, None, False)
                    r.h = new_h
                    if r.other:
                        owr = r.other.get_rect()
                        ow  = owr.right - owr.left
                        u32.SetWindowPos(r.other.hwnd, 0,
                                         owr.left, r._way, ow, new_h, 0x0014)
                        u32.InvalidateRect(r.other.hwnd, None, False)
                        r.other.h = new_h
            return 0

        elif msg == WM_LBUTTONUP:
            if r:
                r._drag = None
                u32.ReleaseCapture()
            return 0

        elif msg == WM_SETCURSOR:
            # 根據滑鼠位置決定游標
            pt = wt.POINT()
            u32.GetCursorPos(ctypes.byref(pt))
            wr = wt.RECT()
            u32.GetWindowRect(hwnd, ctypes.byref(wr))
            win_h = wr.bottom - wr.top
            local_y = pt.y - wr.top
            if local_y >= win_h - RESIZE_ZONE:
                hc = u32.LoadCursorW(None, ctypes.c_void_p(IDC_SIZENS))
            else:
                hc = u32.LoadCursorW(None, ctypes.c_void_p(IDC_ARROW))
            u32.SetCursor(hc)
            return 1

        elif msg == WM_RBUTTONUP:
            u32.PostQuitMessage(0)
            return 0

        elif msg == WM_DESTROY:
            u32.PostQuitMessage(0)
            return 0

        return u32.DefWindowProcW(hwnd, msg, wp, lp)

    proc = WNDPROC(wndproc)
    _procs.append(proc)

    wcx = WNDCLASSEXW()
    wcx.cbSize       = ctypes.sizeof(WNDCLASSEXW)
    wcx.style        = CS_HREDRAW | CS_VREDRAW
    wcx.lpfnWndProc  = proc
    wcx.hInstance    = hinstance
    wcx.hbrBackground= gdi.CreateSolidBrush(BG_COLOR)
    wcx.lpszClassName= cls_name
    u32.RegisterClassExW(ctypes.byref(wcx))

    hwnd = u32.CreateWindowExW(
        WS_EX_TOPMOST | WS_EX_TOOLWINDOW | WS_EX_LAYERED,
        cls_name, f"Ruler {ruler.name}",
        WS_POPUP | WS_VISIBLE,
        x, y, RULER_W, ruler.h,
        None, None, hinstance, None
    )
    u32.SetLayeredWindowAttributes(hwnd, 0, 220, LWA_ALPHA)
    u32.InvalidateRect(hwnd, None, True)
    u32.UpdateWindow(hwnd)

    ruler.hwnd = hwnd
    rulers[hwnd] = ruler
    return hwnd


def main():
    a = Ruler("A", COLOR_A)
    b = Ruler("B", COLOR_B)
    a.other = b
    b.other = a

    make_window(a, A_X, A_Y)
    make_window(b, B_X, B_Y)

    # 訊息迴圈開始前強制重繪
    for ruler in [a, b]:
        u32.InvalidateRect(ruler.hwnd, None, True)
        u32.UpdateWindow(ruler.hwnd)

    msg = wt.MSG()
    while u32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
        u32.TranslateMessage(ctypes.byref(msg))
        u32.DispatchMessageW(ctypes.byref(msg))

if __name__ == "__main__":
    main()
