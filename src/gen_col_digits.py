"""From: https://github.com/salesforce/corr_based_prediction/blob/master/gen_color_mnist.py"""
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from sklearn.datasets import load_digits
import torch


def get_color_codes(cpr):
    C = np.random.rand(len(cpr), NB_CLASSES, 3)
    C = C/np.max(C, axis=2)[:,:,None]
    return C


digits = load_digits()
imgs = digits.images
targets = digits.target
NB_CLASSES = len(set(targets))

cpr = [0.5, 0.5]
noise = 10.

cfg = get_color_codes(cpr)
cbg = get_color_codes(cpr)

# im = Image.fromarray(imgs[0]).convert("RGB")
im = imgs[0]
target = targets[0].reshape(-1, 1)
x = np.array(im).reshape(-1, 8, 8)
x = torch.FloatTensor(((x*255)>150)*255)
x_rgb = torch.ones(1, 3, x.size(1), x.size(2))
x_rgb = x_rgb* x
x_rgb_fg = 1.*x_rgb

color_choice = np.argmax(np.random.multinomial(1, cpr, target.shape[0]), axis=1) if cpr is not None else 0
c = cfg[color_choice, target] if cpr is not None else cfg[color_choice, np.random.randint(NB_CLASSES, size=target.shape[0])]
c = c.reshape(-1, 3, 1, 1)
c = torch.from_numpy(c)
x_rgb_fg[:, 0] = x_rgb_fg[:, 0] * c[:, 0]
x_rgb_fg[:, 1] = x_rgb_fg[:, 1] * c[:, 1]
x_rgb_fg[:, 2] = x_rgb_fg[:, 2] * c[:, 2]

bg = (255-x_rgb)
color_choice = np.argmax(np.random.multinomial(1, cpr, target.shape[0]), axis=1) if cpr is not None else 0
c = cbg[color_choice, target] if cpr is not None else cbg[color_choice, np.random.randint(NB_CLASSES, size=target.shape[0])]
c = c.reshape(-1, 3, 1, 1)
c= torch.from_numpy(c)
bg[:, 0] = bg[:, 0] * c[:, 0]
bg[:, 1] = bg[:, 1] * c[:, 1]
bg[:, 2] = bg[:, 2] * c[:, 2]
x_rgb = x_rgb_fg + bg
x_rgb = x_rgb + torch.tensor((noise)* np.random.randn(*x_rgb.size()))
x_rgb = torch.clamp(x_rgb, 0. ,255.)

color_x = x_rgb/255.

plt.imshow(color_x.reshape(8, 8, -1)); plt.show()