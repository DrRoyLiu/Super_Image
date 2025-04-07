import time

import tkinter as tk
from tkinter import simpledialog

from wechat.stick_images_pdf import images_to_pdf, delete_folder
from wechat.open_wechat_url import get_images


def wechat_images_2_pdf():
    root = tk.Tk()
    root.withdraw()
    # 显示文本输入框并获取用户输入
    url = simpledialog.askstring("输入框", "请输入文章地址")

    # 打印用户输入的内容
    if url and url.startswith('http'):
        folder_name = get_images(url)
        pdf_path = images_to_pdf(folder_name)
        time.sleep(2)  # 暂停2s等待文件生成
        delete_folder(folder_name)
        return url
    else:
        return "文章地址错误"
