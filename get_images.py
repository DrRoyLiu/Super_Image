from pathlib import Path
import tkinter as tk
from tkinter import filedialog


def traverse():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    # 定义常见图片格式
    image_formats = ['*.jpg', '*.png', '*.bmp',
                     '*.gif', '*.jpeg', '*.webp', '*.tif', '*.tiff']
    # 弹出文件夹选择对话框
    src = filedialog.askdirectory()
    out_dir_name = f"{Path(src).name}_result"
    out_dir = Path(src).parent / out_dir_name

    file_group = []

    # 遍历选定文件夹中的所有图片
    # glob方法不会遍历子目录
    # rglob方法可以遍历子目录
    for image_format in image_formats:
        for f in Path(src).glob(image_format):
            file_group.append(f.absolute())

    return file_group, str(out_dir)
