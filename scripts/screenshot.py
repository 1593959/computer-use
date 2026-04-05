"""
Computer Use - 屏幕截图工具
截取当前屏幕并保存到指定路径
"""
import sys
import os
import mss
from PIL import Image

def screenshot(output_path=None, region=None, scale=0.5):
    """
    截取屏幕
    :param output_path: 保存路径，默认 ~/tmp/screenshot.png
    :param region: 截取区域 (left, top, width, height)，默认全屏
    :param scale: 缩放比例，默认0.5（减小图片大小，省token）
    """
    if output_path is None:
        os.makedirs(os.path.expanduser("~/tmp"), exist_ok=True)
        output_path = os.path.expanduser("~/tmp/screenshot.png")

    with mss.mss() as sct:
        if region:
            monitor = {"left": region[0], "top": region[1], "width": region[2], "height": region[3]}
        else:
            monitor = sct.monitors[1]  # 主显示器

        img = sct.grab(monitor)
        pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")

        if scale != 1.0:
            new_size = (int(pil_img.width * scale), int(pil_img.height * scale))
            pil_img = pil_img.resize(new_size, Image.LANCZOS)

        pil_img.save(output_path, "PNG", optimize=True)
        print(f"截图已保存: {output_path} ({pil_img.width}x{pil_img.height})")
        return output_path

if __name__ == "__main__":
    scale = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    output = sys.argv[2] if len(sys.argv) > 2 else None
    screenshot(output_path=output, scale=scale)
