import matplotlib.pyplot as plt
import numpy as np
import cv2


def gradation(width, height, color1, color2, direction=0):

    diagonal = int(np.sqrt(width**2 + height**2)) + 2
    tmp = np.zeros((diagonal, diagonal, len(color1)))

    for i, (start, stop) in enumerate(zip(color1, color2)):
        tmp[:, :, i] = np.tile(np.linspace(start, stop, diagonal), (diagonal, 1)).T

    rotate_matrix = cv2.getRotationMatrix2D(center=(diagonal/2, diagonal/2), angle=-direction, scale=1)
    img = cv2.warpAffine(tmp, rotate_matrix, (diagonal, diagonal))
    ofs_w = (diagonal - width)//2
    ofs_h = (diagonal - height)//2
    return np.uint8(img[ofs_h:ofs_h+height, ofs_w:ofs_w+width, :])


image = gradation(512, 256, (255, 0, 255, 255), (0, 0, 0, 0), 45)
print(image.shape)
plt.imshow(image)
plt.show()
