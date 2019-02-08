import cv2
import matplotlib
matplotlib.use('pdf')
from matplotlib import pyplot as plt
import numpy as np
from skimage import io

from utils import face_utils

import face_recognition

def read_cv2_img(path):
    '''
    Read color images
    :param path: Path to image
    :return: Only returns color images
    '''
    img = cv2.imread(path, -1)

    if img is not None:
        if len(img.shape) != 3:
            img = np.stack((img,)*3, axis=-1)
            #return None

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img

def read_and_crop_cv2_img(path):
    '''
    Read color images
    :param path: Path to image
    :return: Only returns color images
    '''
    img = cv2.imread(path, -1)

    if img is not None:
        if len(img.shape) != 3:
            return None

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    '''bbs = cnn_face_detector(img, 1)
    if len(bbs) > 0:
        r = bbs[0].rect
        x = int(r.left())
        y = int(r.top())
        right = int(r.right())
        bottom = int(r.bottom())
        #y, right, bottom, x = bbs[0]
        bb = x, y, (right - x), (bottom - y)
        img = face_utils.crop_face_with_bb(img, bb)'''

    bbs = face_recognition.face_locations(img)
    if len(bbs) > 0:
        y, right, bottom, x = bbs[0]
        bb = x, y, (right - x), (bottom - y)
        img = face_utils.crop_face_with_bb(img, bb)
    return img

def show_cv2_img(img, title='img'):
    '''
    Display cv2 image
    :param img: cv::mat
    :param title: title
    :return: None
    '''
    plt.imshow(img)
    plt.title(title)
    plt.axis('off')
    plt.show()

def show_images_row(imgs, titles, rows=1):
    '''
       Display grid of cv2 images image
       :param img: list [cv::mat]
       :param title: titles
       :return: None
    '''
    assert ((titles is None) or (len(imgs) == len(titles)))
    num_images = len(imgs)

    if titles is None:
        titles = ['Image (%d)' % i for i in range(1, num_images + 1)]

    fig = plt.figure()
    for n, (image, title) in enumerate(zip(imgs, titles)):
        ax = fig.add_subplot(rows, np.ceil(num_images / float(rows)), n + 1)
        if image.ndim == 2:
            plt.gray()
        plt.imshow(image)
        ax.set_title(title)
        plt.axis('off')
    plt.show()
