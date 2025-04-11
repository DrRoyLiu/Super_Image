import tkinter as tk
from tkinter import messagebox, filedialog
import threading

import server
from perspective.image_transform import image_transform
from get_images import traverse
from wechat.wechat_images_2_pdf import wechat_images_2_pdf
from wechat.stick_images_pdf import images_to_pdf
from yolo_client.get_yolo_result import get_yolo_result


# 打开YOLO服务器
def start_server():
    thread = threading.Thread(target=server.run_server, daemon=True)
    thread.start()


# 选择目录
def select_directory():
    global image_group, output_dir, select_dir
    image_group, output_dir, select_dir = traverse()
    text_box.delete(0, tk.END)
    if output_dir:
        text_box.insert(0, output_dir)
    select_text_box.delete(0, tk.END)
    if select_dir:
        select_text_box.insert(0, select_dir)
    if image_group:
        warning_label.config(text=f"已选择{len(image_group)}张图片")
    else:
        warning_label.config(text="未选择任何图片")


# 获取微信文章
def get_article():
    warning_label.config(text="操作完成前，本界面会卡死")
    wechat_images_2_pdf()
    warning_label.config(text="获取微信文章已完成")


# 照片透视变换
def photo_transform():
    global image_group
    if image_group is None:
        warning_label.config(text="请先选择图片目录")
        return
    warning_label.config(text="操作完成前，本界面会卡死")
    for image_src in image_group:
        img_trans.run(image_src)
    warning_label.config(text="透视变换操作已完成")


# 图像转PDF
def make_pdf(resize=False):
    global image_group, output_dir
    if image_group is None:
        warning_label.config(text="请先选择图片目录")
        return
    warning_label.config(text="操作完成前，本界面会卡死")
    pdf_path = images_to_pdf(output_dir, img_resize=resize)
    warning_label.config(text=f"生成成功，保存至：{pdf_path}")


# YOLO自动识别
def yolo_recognize():
    global image_group
    if image_group is None:
        warning_label.config(text="请先选择图片目录")
        return
    warning_label.config(text="操作完成前，本界面会卡死")
    for image_src in image_group:
        get_yolo_result(image_src)
    warning_label.config(text="YOLO自动识别已完成")


# 创建主窗口
root = tk.Tk()
root.title("SUPER IMAGE")
root.geometry("600x800")
root.resizable(False, False)

# 设置窗口居中
window_width = 600
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

# 初始化变量
image_group = None
output_dir = None
select_dir = None
img_trans = image_transform()

# 创建按钮
button_get_article = tk.Button(
    root, text="获取微信文章", command=get_article, width=20, height=2, bg="green", fg="white")
button_get_article.place(x=200, y=10)

button_select_dir = tk.Button(
    root, text="选择目录", command=select_directory, width=20, height=2, bg="blue", fg="white")
button_select_dir.place(x=200, y=150)

button_photo_transform = tk.Button(
    root, text="照片透视变换", command=photo_transform, width=20, height=2, bg="saddlebrown", fg="white")
button_photo_transform.place(x=200, y=200)

button_yolo_recognize = tk.Button(
    root, text="人工智能识别", command=yolo_recognize, width=20, height=2, bg="saddlebrown", fg="white")
button_yolo_recognize.place(x=200, y=250)

button_pdf_maker_resize = tk.Button(
    root, text="图像转PDF(resize)", command=lambda: make_pdf(True), width=20, height=2, bg="saddlebrown", fg="white")
button_pdf_maker_resize.place(x=200, y=300)

button_pdf_maker = tk.Button(
    root, text="图像转PDF", command=lambda: make_pdf(False), width=20, height=2, bg="saddlebrown", fg="white")
button_pdf_maker.place(x=200, y=350)

button_status = tk.Button(root, text="YOLO服务器：开", width=20,
                          height=2, bg="silver", fg="white")
button_status.place(x=200, y=400)

# 创建文本框和标签
origin_label = tk.Label(root, text="原始目录：", width=10, height=1)
origin_label.place(x=20, y=80)
select_text_box = tk.Entry(root, width=60)
select_text_box.place(x=100, y=80)

select_label = tk.Label(root, text="处理后目录：", width=10, height=1)
select_label.place(x=20, y=100)
text_box = tk.Entry(root, width=60)
text_box.place(x=100, y=100)

# 创建警告标签
warning_label = tk.Label(root, text="请点击选择目录", width=50, height=1, bg="white")
warning_label.place(x=100, y=450)

text_box.insert(0, "请点击选择目录")
select_text_box.insert(0, "请点击选择目录")

# 启动服务器
start_server()


def on_closing():
    root.quit()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

# 运行主循环
root.mainloop()
