import cv2

def select_contour(image, prompt="请选择轮廓"):
    cv2.imshow('Select Contour', image)
    print(prompt)
    while True:
        point = cv2.selectROI('Select Contour', image)
        if point is not None:
            break
    cv2.destroyAllWindows()
    return point

def find_card_size(image_path, a4_width_cm=29.7, a4_height_cm=21.0, ppi=500):
    # 加载图像
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("图像文件未找到")

    # 用户选择A4纸和卡片的轮廓
    a4_point = select_contour(image, "请选择A4纸的轮廓")
    card_point = select_contour(image, "请选择卡片的轮廓")

    # 从图像中裁剪出A4纸和卡片的区域
    a4_cropped = image[a4_point[1]:a4_point[1]+a4_point[3], a4_point[0]:a4_point[0]+a4_point[2]]
    card_cropped = image[card_point[1]:card_point[1]+card_point[3], card_point[0]:card_point[0]+card_point[2]]

    # 计算A4纸和卡片的像素尺寸
    a4_px_width = a4_point[2]
    a4_px_height = a4_point[3]
    card_gray = cv2.cvtColor(card_cropped, cv2.COLOR_BGR2GRAY)
    _, card_thresh = cv2.threshold(card_gray, 127, 255, cv2.THRESH_BINARY)
    card_contour, _ = cv2.findContours(card_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    card_contour = cv2.boundingRect(max(card_contour, key=cv2.contourArea))

    # 计算PPC（每厘米的像素数）
    ppc_width = a4_px_width / a4_width_cm
    ppc_height = a4_px_height / a4_height_cm
    ppc = (ppc_width + ppc_height) / 2

    # 计算卡片的实际尺寸
    card_width_cm = (card_contour[2] - card_contour[0]) / ppc
    card_height_cm = (card_contour[3] - card_contour[1]) / ppc

    print(f"卡片的宽度为: {card_width_cm:.2f} 厘米")
    print(f"卡片的高度为: {card_height_cm:.2f} 厘米")

# 使用示例
find_card_size("输入你的图片路径")