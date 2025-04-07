import os
import time
import requests
import base64
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from progress_bar.show_progress_bar import show_progress_bar


def get_images(url):
    if url is None:
        raise ValueError("URL cannot be empty.")
    custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--user-agent={custom_user_agent}')
    # 创建 ChromeDriver 实例并发出请求
    driver = webdriver.Chrome(options=chrome_options)

    # 打开网页
    driver.get(url)

    # 等待页面完全加载（包括异步加载的内容）
    # 这里可以根据需要调整等待时间，或者等待特定元素出现
    time.sleep(5)  # 简单等待 5 秒，确保所有内容加载完成

    def get_page_height():
        return driver.execute_script("return document.body.scrollHeight")

    def get_window_height():
        return driver.execute_script("return window.innerHeight")

    def scroll_to_bottom():
        page_height = get_page_height()  # 获取当前页面高度
        innerHeight = get_window_height()
        sumHeight = 0
        while sumHeight < page_height:
            # 滚动一屏
            driver.execute_script(f"window.scrollBy(0, {innerHeight});")
            sumHeight += innerHeight
            time.sleep(1)  # 等待 1 秒

    # 开始滚动
    scroll_to_bottom()

    # 获取网页的 title 作为文件夹名
    folder_name = driver.title.strip() if driver.title else 'images'
    folder_name = ''.join(c for c in folder_name if c.isalnum()
                          or c in (' ', '_')).rstrip()

    # 创建文件夹
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 获取页面源代码（此时包含异步加载的内容）
    page_source = driver.page_source

    # 使用 BeautifulSoup 解析页面源代码
    soup = BeautifulSoup(page_source, 'html.parser')

    # 查找所有的图片标签
    img_tags = soup.find_all('img')
    image_num = len(img_tags)

    # 下载并保存图片
    for i, img in enumerate(img_tags):
        style = img.get('style', '')
        if 'display: none' in style:
            continue
        time.sleep(0.5)
        img_url = img.get('src')
        if not img_url:
            continue

        try:
            # 判断是否是 Data URL（Base64 编码）
            if img_url.startswith('data:image'):
                # 提取 Data URL 的头部和数据部分
                header, data = img_url.split(',', 1)

                # 提取图片格式
                if ';' in header:
                    img_format = header.split(';')[0].split(
                        '/')[-1]  # 提取格式，例如 "svg+xml" 或 "png"
                else:
                    img_format = header.split('/')[-1]  # 如果没有分号，直接提取格式

                # 如果格式包含 "+"，取第一部分（例如 "svg+xml" -> "svg"）
                img_format = img_format.split('+')[0]

                # 如果是 Base64 编码，解码数据
                if 'base64' in header:
                    img_data = base64.b64decode(data)
                else:
                    # 如果不是 Base64 编码，直接使用原始数据
                    img_data = data.encode('utf-8')

                # 图片文件名
                img_name = f'{i+1:04d}.{img_format}'  # 例如 0001.svg, 0002.png
            else:
                # 处理普通图片 URL
                img_url = urljoin(url, img_url)
                # 发送 HTTP 请求下载图片
                img_data = requests.get(img_url).content
                # 提取图片格式（从 URL 或 Content-Type）
                img_format = img_url.split('.')[-1].lower()  # 从 URL 中提取扩展名
                if img_format not in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:  # 如果无法从 URL 中提取格式
                    img_format = 'jpg'  # 默认格式
                # 图片文件名
                img_name = f'{i+1:04d}.{img_format}'  # 例如 0001.jpg, 0002.png

            # 保存图片到文件夹
            with open(os.path.join(folder_name, img_name), 'wb') as img_file:
                img_file.write(img_data)

        except Exception as e:
            print(f'Failed to process {img_url}: {e}')

        show_progress_bar(i + 1, image_num, f'{img_name}')

    # 关闭浏览器
    driver.quit()
    return folder_name


if __name__ == '__main__':
    # 目标网页的URL
    url = 'https://mp.weixin.qq.com/s/6S7R-zc5sOorc9bL4kv_PQ'
    forder_name = get_images(url)
