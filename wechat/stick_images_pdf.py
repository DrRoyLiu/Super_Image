import os
import shutil
from datetime import datetime
from PIL import Image


def images_to_pdf(folder_path, target_path=None, img_resize=False):
    # 获取文件夹名称
    folder_name = os.path.basename(folder_path)

    # 获取文件夹内所有图片文件
    images = [img for img in os.listdir(folder_path) if img.lower().endswith(
        ('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    # 按名称排序
    images.sort()

    if target_path:
        pdf_folder_path = target_path
    else:
        pdf_folder_path = folder_path

    # 创建文件夹
    if not os.path.exists(pdf_folder_path):
        os.makedirs(pdf_folder_path)

    # 打开所有图片并转换为PDF
    pdf_path = os.path.join(pdf_folder_path, f"{folder_name}.pdf")

    # 判断文件是否存在，如果存在则重新生成新的pdf_path
    while os.path.exists(pdf_path):
        # 获取当前时间
        now = datetime.now()
        # 格式化时间为年月日时分秒，不带间隔符
        time_str = now.strftime('%Y%m%d%H%M%S')
        pdf_path = os.path.join(
            pdf_folder_path, f"{folder_name}-{time_str}.pdf")

    # 创建一个空列表，用于存储所有图片对象
    image_list = []

    for img in images:
        img_path = os.path.join(folder_path, img)
        img_obj = Image.open(img_path)
        # 判断图片的宽是否大于等于800，高是否大于等于400
        if (img_obj.width < 800 and img_obj.height < 500) or (img_obj.width < 600 and img_obj.height < 1000):
            continue
        if img_resize:
            img_obj = resize(img_obj)
        if img_obj.mode != 'RGB':
            img_obj = img_obj.convert('RGB')  # 转换为RGB模式
        image_list.append(img_obj)

    # 保存为PDF，保持分辨率不变
    if image_list:
        image_list[0].save(pdf_path, save_all=True,
                           append_images=image_list[1:], resolution=100.0)
        print(f"PDF文件已生成: {pdf_path}")
    else:
        print("文件夹内没有图片文件。")

    return pdf_path


def resize(img, width=1600, height=900):
    return img.resize((width, height))


def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"文件夹已删除: {folder_path}")
    except OSError as e:
        print(f"无法删除文件夹: {e}")


if __name__ == "__main__":
    folder_path = r"../images"  # 替换为你的文件夹路径
    pdf_path = images_to_pdf(folder_path)
