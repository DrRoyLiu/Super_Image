from pathlib import Path
from PIL import Image

from ultralytics import YOLO


class detector:
    def __init__(self):
        self.model = YOLO(Path(__file__).resolve().parent/"yolov12m.pt")
        self.cls_names = self.model.names

    def detect(self, image, imgsz=800):
        if isinstance(image, Image.Image):
            results = self.model.predict(source=image, imgsz=imgsz)
            rst = []
            for result in results:
                t = result.boxes
                cls_list = t.cls.tolist()
                conf_list = t.conf.tolist()
                xywh_list = t.xywh.tolist()
                xyxy_list = t.xyxy.tolist()
                cls_name = [self.cls_names[i] for i in cls_list]
                for i in range(len(cls_list)):
                    rst.append({
                        "cls": cls_name[i],
                        "conf": round(conf_list[i]),
                        "xywh": [round(r) for r in xywh_list[i]],
                        "xyxy": [round(r) for r in xyxy_list[i]],
                        "orig_shape": t.orig_shape
                    })
            return {
                "status": "success",
                "results": rst
            }
        else:
            return {
                "status": "error", "message": "image is not Image"}


if __name__ == "__main__":
    d = detector()
    image = Image.open(Path(__file__).resolve().parent/'images/test0.jpg')
    result = d.detect(image)
    print(result)
