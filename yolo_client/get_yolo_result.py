from PIL import Image
import requests
from pathlib import Path

import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()  # 隐藏主窗口


def get_yolo_result(img_src):
    with open(img_src, 'rb') as f:
        img_byte_arr = f.read()
    path = Path(img_src)
    dir_name = path.parent.name+"_result"
    output_dir = path.parent.parent / dir_name
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    files = {'file': ('image.jpg', img_byte_arr, 'image/jpeg')}
    try:
        response = requests.post('http://localhost:7280/detect', files=files)
        results = response.json()
        if 'status' in results and results['status'] == 'success':
            for result in results["results"]:
                if result['cls'] == 'tv':
                    # orig_shape = result['orig_shape']
                    x1, y1, x2, y2 = result['xyxy']
                    img = Image.open(img_src)
                    cropped_img = img.crop((x1, y1, x2, y2))
                    cropped_img.save(output_dir/path.name)
        else:
            pass
            # messagebox.showwarning("返回值异常", results)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("连接失败", "服务器连接失败")
