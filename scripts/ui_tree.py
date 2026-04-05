"""
Computer Use - UI 元素树获取工具
使用 Windows UI Automation API 获取当前窗口的所有可交互元素
"""
import sys
import json
import os

def get_ui_tree(max_depth=3, window_name=None):
    """
    获取当前前台窗口的 UI 元素树
    """
    try:
        import uiautomation as auto
    except ImportError:
        print("ERROR: uiautomation 未安装，请运行: pip install uiautomation")
        return

    try:
        if window_name:
            window = auto.WindowControl(searchDepth=1, Name=window_name)
        else:
            # 获取焦点控件，然后向上找窗口
            focused = auto.GetFocusedControl()
            window = focused
            # 向上找到顶层窗口
            while window and window.ControlTypeName != "WindowControl" and window.ControlTypeName != "PaneControl":
                parent = window.GetParentControl()
                if parent and parent != window:
                    window = parent
                else:
                    break

        win_name = getattr(window, 'Name', 'Unknown') or 'Unknown'
        print(f"窗口: {win_name}")

        try:
            rect = window.BoundingRectangle
            print(f"位置: left={rect.left}, top={rect.top}, right={rect.right}, bottom={rect.bottom}")
        except:
            pass

        print(f"{'='*60}")

    except Exception as e:
        # 备选方案：直接列出所有顶层窗口
        print(f"获取前台窗口失败({e})，列出所有顶层窗口：")
        print(f"{'='*60}")
        root = auto.GetRootControl()
        window = root

    elements = []

    def traverse(control, depth=0):
        if depth > max_depth:
            return

        try:
            name = getattr(control, 'Name', '') or ''
            control_type = getattr(control, 'ControlTypeName', '') or ''
            automation_id = getattr(control, 'AutomationId', '') or ''

            # 只记录有意义的元素
            if name or automation_id:
                try:
                    rect = control.BoundingRectangle
                    element = {
                        "index": len(elements),
                        "type": control_type,
                        "name": name[:100],
                        "id": automation_id[:50],
                        "x": (rect.left + rect.right) // 2,
                        "y": (rect.top + rect.bottom) // 2,
                        "w": rect.right - rect.left,
                        "h": rect.bottom - rect.top,
                    }
                    elements.append(element)

                    indent = "  " * depth
                    print(f"{indent}[{element['index']}] {control_type}: \"{name[:60]}\" @ ({element['x']}, {element['y']})")
                except:
                    pass
        except:
            pass

        # 遍历子元素
        try:
            children = control.GetChildren()
            if children:
                for child in children:
                    traverse(child, depth + 1)
        except:
            pass

    traverse(window)

    print(f"\n{'='*60}")
    print(f"共找到 {len(elements)} 个可交互元素")

    # 输出 JSON
    os.makedirs(os.path.expanduser("~/.openclaw/workspace"), exist_ok=True)
    json_path = os.path.expanduser("~/.openclaw/workspace/ui_tree.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(elements, f, ensure_ascii=False, indent=2)
    print(f"元素树已保存: {json_path}")

    return elements

if __name__ == "__main__":
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    window = sys.argv[2] if len(sys.argv) > 2 else None
    get_ui_tree(max_depth=depth, window_name=window)
