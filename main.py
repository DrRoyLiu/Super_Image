import pygame
import sys
import os
import threading

import server
from perspective.image_transform import image_transform
from get_images import traverse
from wechat.wechat_images_2_pdf import wechat_images_2_pdf
from wechat.stick_images_pdf import images_to_pdf
from yolo_client.get_yolo_result import get_yolo_result

# 初始化pygame
pygame.init()

# 设置窗口大小和标题
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("功能选择界面")

# 设置窗口居中
os.environ['SDL_VIDEO_CENTERED'] = '1'

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (145, 145, 145)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 加载支持中文的字体
font_path = r"C:\Windows\Fonts\simhei.ttf"
font = pygame.font.Font(font_path, 26)

# 图像透视变换类
img_trans = image_transform()

# 打开YOLO12服务器
thread = threading.Thread(target=server.run_server)
thread.start()


class Button:
    '''按钮类'''

    def __init__(self, text, x, y, width, height, color, text_color=WHITE):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_color = text_color
        self.text_surface = font.render(text, True, text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.text_surface, self.text_rect)


# 创建按钮
button_get_article = Button("获取微信文章", 300, 200, 200, 50, BROWN)
button_photo_transform = Button("照片透视变换", 300, 300, 200, 50, BROWN)
button_yolo_recognize = Button("人工智能识别", 300, 400, 200, 50, BROWN)
button_pdf_maker = Button("图像转PDF", 300, 500, 200, 50, BROWN)
button_select_dir = Button("选择目录", 10, 10, 120, 30, BLUE)
button_status = Button("YOLO服务器", 10, 760, 200, 30, GREEN)

# 文本框
text_box = pygame.Rect(150, 10, 600, 30)
text_box_text = ""
Warning_box = pygame.Rect(250, 760, 600, 30)
Warning_box_text = ""

# 状态变量
server_status = False

# 图像路径和输出文件夹
image_group = None
output_dir = None


def draw_text():
    # 绘制文本框
    pygame.draw.rect(screen, WHITE, text_box, 2)
    text_surface = font.render(text_box_text, True, WHITE)
    screen.blit(text_surface, (text_box.x + 5, text_box.y + 5))
    pygame.draw.rect(screen, WHITE, Warning_box, 2)
    Warning_surface = font.render(Warning_box_text, True, WHITE)
    screen.blit(Warning_surface, (Warning_box.x + 5, Warning_box.y + 5))
    pygame.display.flip()


# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_select_dir.rect.collidepoint(event.pos):
                image_group, output_dir = traverse()
                text_box_text = output_dir
                draw_text()
                Warning_box_text = f"已选择{len(image_group)}张图片"
            elif button_get_article.rect.collidepoint(event.pos):
                Warning_box_text = f"操作完成前，本界面会卡死"
                draw_text()
                wechat_images_2_pdf()
                Warning_box_text = "获取微信文章已完成"
            elif button_photo_transform.rect.collidepoint(event.pos):
                if image_group is None:
                    Warning_box_text = "请先选择图片目录"
                else:
                    Warning_box_text = f"操作完成前，本界面会卡死"
                    draw_text()
                    for image_src in image_group:
                        img_trans.run(image_src)
                    Warning_box_text = "透视变换操作已完成"
            elif button_pdf_maker.rect.collidepoint(event.pos):
                if image_group is None:
                    Warning_box_text = "请先选择图片目录"
                else:
                    Warning_box_text = f"操作完成前，本界面会卡死"
                    draw_text()
                    pdf_path = images_to_pdf(output_dir, img_resize=True)
                    Warning_box_text = f"生成成功，保存至：{pdf_path}"
            elif button_yolo_recognize.rect.collidepoint(event.pos):
                if image_group is None:
                    Warning_box_text = "请先选择图片目录"
                else:
                    Warning_box_text = f"操作完成前，本界面会卡死"
                    draw_text()
                    for image_src in image_group:
                        get_yolo_result(image_src)
                    Warning_box_text = "YOLO自动识别已完成"

    # 绘制背景
    screen.fill(BLACK)

    # 绘制按钮
    button_get_article.draw(screen)
    button_photo_transform.draw(screen)
    button_yolo_recognize.draw(screen)
    button_pdf_maker.draw(screen)
    button_select_dir.draw(screen)
    button_status.draw(screen)

    draw_text()

    # 更新屏幕
    pygame.display.flip()

# 退出pygame
pygame.quit()
sys.exit()
