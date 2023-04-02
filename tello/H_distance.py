import numpy as np  # 导入numpy库
import cv2  # 导入Opencv库

KNOWN_DISTANCE = 170  # 测量时目标距离（cm）
KNOWN_WIDTH = 20  # 目标宽度（cm）
KNOWN_PERWIDTH = 0.108  # 测量时图像像素尺寸（归一化后）

focalLength_value = KNOWN_PERWIDTH * KNOWN_DISTANCE / KNOWN_WIDTH


# 定义距离函数
def distance_to_camera(knownWidth, focalLength, perWidth):
    return (knownWidth * focalLength) / perWidth


# 计算摄像头到物体的距离
def calculate_distance(img, info):
    # cv2.imshow(“原图”, image)
    width = info[0][2]
    print("width: ", width)
    if width != 0:
        distance = distance_to_camera(KNOWN_WIDTH, focalLength_value, width)
        cv2.putText(img, "%.2fcm" % (distance), (0, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)
        cv2.imshow("单目测距", img)
        return distance
    else:
        return -1


if __name__ == "main":

    # img_path = "Picture1.jpg"
    #
    # focalLength = calculate_focalDistance(img_path)
    #
    # for image_path in IMAGE_PATHS:
    #
    #     calculate_Distance(image_path, focalLength)

    cap = cv2.VideoCapture(0)
    i = 0
    focalLength = 10
    while (1):
        _, img = cap.read()
        print(i)
        i += 1
        calculate_distance(img, focalLength)
        if cv2.waitKey(1) & 0xFF == ord('Q'):
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()
