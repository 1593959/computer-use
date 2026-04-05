"""
Computer Use - Windows 兼容版
跨平台屏幕操控脚本（Windows/Linux/Mac）
"""

import platform
import os
import sys
import json
import time

# 根据平台导入不同库
SYSTEM = platform.system()

if SYSTEM == "Windows":
    import ctypes
    from ctypes import wintypes
    try:
        import pyautogui
        import pygetwindow as gw
        import pyperclip  # Windows 中文输入需要
    except ImportError:
        print("请先安装依赖: pip install pyautogui pygetwindow pyperclip")
        sys.exit(1)
elif SYSTEM == "Darwin":  # macOS
    try:
        import pyautogui
    except ImportError:
        print("请先安装依赖: pip install pyautogui")
        sys.exit(1)
else:  # Linux
    try:
        import pyautogui
    except ImportError:
        print("请先安装依赖: pip install pyautogui")
        sys.exit(1)

def get_screen_size():
    """获取屏幕尺寸"""
    if SYSTEM == "Windows":
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    else:
        return pyautogui.size()

def screenshot(output_path=None, scale=1.0):
    """截图"""
    if output_path is None:
        tmp_dir = os.environ.get('TEMP', '/tmp') if SYSTEM == "Windows" else '/tmp'
        output_path = os.path.join(tmp_dir, f"screenshot_{int(time.time())}.png")
    
    try:
        img = pyautogui.screenshot()
        
        # 缩放
        if scale != 1.0:
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size)
        
        img.save(output_path)
        print(f"截图已保存: {output_path} ({img.width}x{img.height})")
        return output_path
    except Exception as e:
        print(f"截图失败: {e}")
        return None

def click(x, y, button='left', clicks=1):
    """点击"""
    try:
        pyautogui.click(x, y, button=button, clicks=clicks)
        print(f"点击: ({x}, {y})")
        return True
    except Exception as e:
        print(f"点击失败: {e}")
        return False

def move_to(x, y):
    """移动鼠标"""
    try:
        pyautogui.moveTo(x, y)
        return True
    except Exception as e:
        print(f"移动失败: {e}")
        return False

def type_text(text, interval=0.01):
    """输入文字 - Windows下使用剪贴板粘贴避免编码问题"""
    try:
        # Windows 下中文编码问题处理
        if SYSTEM == "Windows" and any(ord(c) > 127 for c in text):
            # 使用剪贴板粘贴中文
            import pyperclip
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')
            print(f"输入(粘贴): {text[:50]}...")
        else:
            pyautogui.typewrite(text, interval=interval)
            print(f"输入: {text[:50]}...")
        return True
    except Exception as e:
        print(f"输入失败: {e}")
        return False

def press(key):
    """按键"""
    try:
        pyautogui.press(key)
        print(f"按键: {key}")
        return True
    except Exception as e:
        print(f"按键失败: {e}")
        return False

def hotkey(*keys):
    """快捷键"""
    try:
        pyautogui.hotkey(*keys)
        print(f"快捷键: {'+'.join(keys)}")
        return True
    except Exception as e:
        print(f"快捷键失败: {e}")
        return False

def scroll(amount, x=None, y=None):
    """滚动"""
    try:
        if x is not None and y is not None:
            pyautogui.scroll(amount, x=x, y=y)
        else:
            pyautogui.scroll(amount)
        print(f"滚动: {amount}")
        return True
    except Exception as e:
        print(f"滚动失败: {e}")
        return False

def drag(start_x, start_y, end_x, end_y, duration=0.5):
    """拖拽"""
    try:
        pyautogui.moveTo(start_x, start_y)
        pyautogui.dragTo(end_x, end_y, duration=duration)
        print(f"拖拽: ({start_x},{start_y}) -> ({end_x},{end_y})")
        return True
    except Exception as e:
        print(f"拖拽失败: {e}")
        return False

def wait(seconds):
    """等待"""
    print(f"等待 {seconds} 秒...")
    time.sleep(seconds)
    return True

def get_window_list():
    """获取窗口列表（仅Windows）"""
    if SYSTEM != "Windows":
        print("获取窗口列表仅在 Windows 支持")
        return []
    
    try:
        windows = gw.getAllWindows()
        result = []
        for w in windows:
            if w.title:
                result.append({
                    'title': w.title,
                    'left': w.left,
                    'top': w.top,
                    'width': w.width,
                    'height': w.height
                })
        return result
    except Exception as e:
        print(f"获取窗口失败: {e}")
        return []

def find_window(title_contains):
    """查找窗口（仅Windows）"""
    if SYSTEM != "Windows":
        return None
    
    try:
        windows = gw.getWindowsWithTitle(title_contains)
        if windows:
            return windows[0]
        return None
    except Exception as e:
        print(f"查找窗口失败: {e}")
        return None

def activate_window(title_contains):
    """激活窗口（仅Windows）"""
    if SYSTEM != "Windows":
        print("激活窗口仅在 Windows 支持")
        return False
    
    window = find_window(title_contains)
    if window:
        try:
            if window.isMinimized:
                window.restore()
            window.activate()
            print(f"激活窗口: {window.title}")
            return True
        except Exception as e:
            print(f"激活窗口失败: {e}")
    return False

def main():
    """CLI 入口"""
    if len(sys.argv) < 2:
        print("""
用法: python action.py '<json_action>'

示例:
  python action.py '{"type":"screenshot","scale":0.5}'
  python action.py '{"type":"click","x":500,"y":300}'
  python action.py '{"type":"type","text":"Hello"}'
  python action.py '{"type":"hotkey","keys":["ctrl","c"]}'
  python action.py '{"type":"press","key":"enter"}'
  python action.py '{"type":"scroll","amount":-3}'
  python action.py '{"type":"wait","seconds":2}'
  python action.py '{"type":"activate","title":"飞书"}'
        """)
        return
    
    try:
        action = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return
    
    action_type = action.get('type')
    
    if action_type == 'screenshot':
        output = action.get('output')
        scale = action.get('scale', 1.0)
        screenshot(output, scale)
    
    elif action_type == 'click':
        click(action['x'], action['y'], 
              action.get('button', 'left'), 
              action.get('clicks', 1))
    
    elif action_type == 'move':
        move_to(action['x'], action['y'])
    
    elif action_type == 'type':
        type_text(action['text'], action.get('interval', 0.01))
    
    elif action_type == 'press':
        press(action['key'])
    
    elif action_type == 'hotkey':
        hotkey(*action['keys'])
    
    elif action_type == 'scroll':
        scroll(action['amount'], action.get('x'), action.get('y'))
    
    elif action_type == 'drag':
        drag(action['start_x'], action['start_y'],
             action['end_x'], action['end_y'],
             action.get('duration', 0.5))
    
    elif action_type == 'wait':
        wait(action['seconds'])
    
    elif action_type == 'activate':
        activate_window(action['title'])
    
    elif action_type == 'list_windows':
        windows = get_window_list()
        print(json.dumps(windows, indent=2, ensure_ascii=False))
    
    else:
        print(f"未知操作类型: {action_type}")

if __name__ == '__main__':
    main()
