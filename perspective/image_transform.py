import cv2
import numpy as np
from pathlib import Path


class image_transform:
    image_src = None
    result_src = None
    out_dir_name = 'images_result'
    file_name = None
    image_origin = None
    image_resize = None
    image_result = None
    click_coords = []
    coord_result = {}
    w, h = 1600, 900
    width, height = 1600, 900
    pts_dst = np.array([
        [0, 0],
        [w, 0],
        [0, h],
        [w, h],
    ], dtype='float32')
    suffix = ('.png', '.jpg', '.jpeg', '.bmp')

    def set_image_size(self, w, h):
        """
        设置图像尺寸并更新目标点坐标。

        Args:
            w (int): 图像宽度。
            h (int): 图像高度。

        Returns:
            None

        """
        self.w, self.h = w, h
        self.pts_dst = np.array([
            [0, 0],
            [w, 0],
            [0, h],
            [w, h],
        ], dtype='float32')

    def read_image(self, image_src):
        """
        从给定路径读取图像文件，并进行缩放处理。

        Args:
            image_src (Path): 图像文件路径。

        Returns:
            None

        """
        self.click_coords = []
        self.image_src = image_src
        self.file_name = image_src.name

        dir_name = self.image_src.parent.name+"_result"
        output_dir = self.image_src.parent.parent / dir_name
        self.out_dir_name = output_dir

        if image_src.exists() and image_src.suffix in self.suffix:
            self.image_origin = cv2.imread(str(image_src))
            self.image_resize = cv2.resize(self.image_origin, (self.w, self.h))
        else:
            print(f'{image_src} is not exist')
            exit(0)

    def add_coord(self, x, y):
        """
        添加点击的坐标点。

        Args:
            x (float): 点击位置的 x 坐标，相对于图像的宽度比例。
            y (float): 点击位置的 y 坐标，相对于图像的高度比例。

        Returns:
            None

        """
        x_origin = int(x * self.image_origin.shape[1]/self.w)
        y_origin = int(y * self.image_origin.shape[0]/self.h)
        self.click_coords.append({'x': x_origin, 'y': y_origin})
        if len(self.click_coords) == 4:
            self.check_coord()
            self.transform()
            self.save_result()

    def save_result(self):
        """
        保存识别结果到指定目录，并显示识别后的图片。

        Args:
            无

        Returns:
            无

        """
        if self.image_result is not None:
            Path(self.out_dir_name).mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(Path(self.out_dir_name) / self.file_name),
                        self.image_result)
            img_tmp = cv2.resize(self.image_result, (self.w, self.h))
            cv2.imshow(self.file_name, img_tmp)
            cv2.moveWindow(self.file_name, 320, 0)
            pts = np.array([
                [self.coord_result['top_left']['x'],
                    self.coord_result['top_left']['y']],
                [self.coord_result['bottom_left']['x'],
                    self.coord_result['bottom_left']['y']],
                [self.coord_result['bottom_right']['x'],
                    self.coord_result['bottom_right']['y']],
                [self.coord_result['top_right']['x'],
                    self.coord_result['top_right']['y']],
            ], np.int32)
            image_with_quadrilateral = cv2.polylines(
                self.image_origin, [pts], True, (255, 0, 0), 5)
            image_with_quadrilateral = cv2.resize(
                image_with_quadrilateral, (self.w, self.h))
            cv2.imshow('origin', image_with_quadrilateral)

    def click_event(self, event, x, y, flags, param):
        """
        处理鼠标点击事件

        Args:
        - self: 当前对象的实例
        - event: 事件类型，整数类型，取值为OpenCV中定义的事件类型常量
        - x: 鼠标在，图像整数上的类型横坐标
        ，-整数 param类型: 用户
        定义的-参数 y，:整数 鼠标类型在图像上的

        纵Returns坐标:，整数
        类型- None
        - flags

        :"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.add_coord(x, y)

    def show_image(self):
        """
        显示经过缩放后的图像，并监听鼠标点击事件。

        Args:
            无

        Returns:
            无

        """
        cv2.imshow('origin', self.image_resize)
        cv2.moveWindow('origin', 0, 0)
        cv2.setMouseCallback('origin', self.click_event)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def check_coord(self):
        """
        根据点击的坐标点，计算矩形框的四个角点坐标，以及矩形的宽和高。

        Args:
            无

        Returns:
            无

        """
        coords = sorted(self.click_coords,
                        key=lambda coord: (coord['x']+coord['y']))
        top_left = coords[0]
        bottom_right = coords[-1]
        remaining_coords = coords[1:-1]
        bottom_left = next(c for c in remaining_coords if c['y'] == max(
            c['y'] for c in remaining_coords))
        top_right = next(c for c in remaining_coords if c not in [bottom_left])

        self.coord_result = {
            'top_left': top_left,
            'bottom_right': bottom_right,
            'bottom_left': bottom_left,
            'top_right': top_right
        }

        self.width = max(top_right['x']-top_left['x'],
                         bottom_right['x']-bottom_left['x'])
        self.height = max(bottom_left['y']-top_left['y'],
                          bottom_right['y']-top_right['y'])
        self.pts_dst = np.array([
            [0, 0],
            [self.width, 0],
            [0, self.height],
            [self.width, self.height],
        ], dtype='float32')

    def transform(self):
        """
        根据四个坐标点进行仿射变换

        Args:
            无

        Returns:
            无

        """
        pts_src = np.array([
            [self.coord_result['top_left']['x'],
                self.coord_result['top_left']['y']],
            [self.coord_result['top_right']['x'],
                self.coord_result['top_right']['y']],
            [self.coord_result['bottom_left']['x'],
                self.coord_result['bottom_left']['y']],
            [self.coord_result['bottom_right']['x'],
                self.coord_result['bottom_right']['y']]
        ], dtype='float32')
        M = cv2.getPerspectiveTransform(pts_src, self.pts_dst)
        self.image_result = cv2.warpPerspective(
            self.image_origin, M, (self.width, self.height))

    def run(self, image_src):
        """
        运行函数，用于读取并显示图像。

        Args:
            image_src (str): 图像文件路径。

        Returns:
            None

        """
        self.read_image(image_src)
        self.show_image()


if __name__ == '__main__':
    """
    生成测试函数
    """
    image_src = Path(u'images/test.jpg')
    it = image_transform()
    it.run(image_src)
