import cv2
import albumentations as A
import numpy as np
import torch
from pathlib import Path
from src.transforms.pair_transform import PairedTransformForDimma  # noqa: I900
from src.transforms.mdn_transform import MDNTransform  # 替换为您的实际导入路径

def process_single_image(image_path):
    # 加载图片
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    train_transform = A.Compose(
            [
                A.RandomCrop(256, 256),
                A.HorizontalFlip(),
                A.ISONoise(),
            ])

    # 创建MDNTransform实例
    mdn_transform = MDNTransform(
        dim_factor= 1.0,
        path= "dimmers/UIEB/10shot",
        transforms=train_transform ,
        mdn=True,
        )

    

    # 应用transform
    processed = mdn_transform(image)
    # 假设processed包含MDNTransform处理后的结果
    processed_image = processed["image"].detach().cpu().numpy()

    # 转换回HWC格式
    processed_image = np.moveaxis(processed_image, 0, -1)
    processed_image = (processed_image * 255).astype(np.uint8)

    # 假设您只对原始的'dark'图像感兴趣，提取出前3个通道（假设这是RGB图像）
    if processed_image.shape[2] >= 3:
        rgb_image = processed_image[:, :, :3]  # 提取前三个通道

        # 将RGB转换为BGR，以便在OpenCV中正确显示
        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

        # 显示图像
        #cv2.imshow('Processed Image', bgr_image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        # 或者保存图像
        cv2.imwrite('333_processed_image.JPEG', bgr_image)


    return processed_image

# 假设您已经有了一个transform_config对象
# image_path是您要处理的图片的路径
image_path = "333.png"
processed_image = process_single_image(image_path)

