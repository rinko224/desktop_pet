from PIL import Image
from io import BytesIO
from PySide2.QtGui import QPixmap, QImage

def picture_spilt(image_bytes: bytes):
    image = Image.open(BytesIO(image_bytes))
    
    # PIL的crop参数格式为: (左, 上, 右, 下)
    # 对应你提供的 x(min), y(min), x(max), y(max)
    
    # 左上：x: 83~413, y: 127~566
    top_left = image.crop((83, 127, 413, 566))
    
    # 右上：x: 413~801, y: 127~566
    top_right = image.crop((413, 127, 801, 566))
    
    # 左下：x: 83~413, y: 566~1024
    bottom_left = image.crop((83, 566, 413, 1024))
    
    # 右下：x: 413~801, y: 566~1024
    bottom_right = image.crop((413, 566, 801, 1024))
    
    return top_left, top_right, bottom_left, bottom_right


def pil_to_pixmap(pil_image):
    # 转成 RGBA 模式
    pil_image = pil_image.convert("RGBA")
    
    # 将 PIL Image 转成 bytes
    data = pil_image.tobytes("raw", "RGBA")
    
    # 创建 QImage
    qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGBA8888)
    
    # 转 QPixmap
    return QPixmap.fromImage(qimage)