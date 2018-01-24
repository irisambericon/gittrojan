#!/usr/bin/python
#需要pywin32库
import win32gui
import win32ui
import win32con
import win32api

#获取桌面窗口句柄
hdesktop = win32gui.GetDesktopWindow()

#获取桌面窗口像素尺寸
width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

#创建设备描述符表
desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32ui.CreateDCFromHandle(desktop_dc)

#创建内存设备描述符表
mem_dc = img_dc.CreateCompatibleDC()

#创建位图
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)

#将屏幕图像复制到内存描述符表
mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

#位图保存
screenshot.SaveBitmapFile(mem_dc, 'c:\\WINDOWS\\Temp\\screenshot.bmp')

#释放对象
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())