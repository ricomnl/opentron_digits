import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from sklearn.datasets import load_digits

lena = Image.open("resources/lena.png")

digits = load_digits()
imgs = digits.images
IMG_SIZE = imgs.shape[-1]
x_train = imgs.reshape(-1, IMG_SIZE, IMG_SIZE, 1).astype(np.float32)

def color_digits_batch(x, batch_size=256, change_colors=True):
    # Select random batch (WxHxC)
    idx = np.random.choice(x.shape[0], batch_size)
    batch_raw = x_train[idx, :, :, 0].reshape((batch_size, IMG_SIZE, IMG_SIZE, 1))

    # Extend to RGB
    batch_rgb = np.concatenate([batch_raw, batch_raw, batch_raw], axis=3)

    # Convert the MNIST images to binary
    batch_binary = (batch_rgb > 0.5)

    # Create a new placeholder variable for our batch
    batch = np.zeros((batch_size, IMG_SIZE, IMG_SIZE, 3))

    for i in range(batch_size):
        # Take a random crop of the Lena image (background)
        x_c = np.random.randint(0, lena.size[0] - IMG_SIZE)
        y_c = np.random.randint(0, lena.size[1] - IMG_SIZE)
        image = lena.crop((x_c, y_c, x_c + IMG_SIZE, y_c + IMG_SIZE))
        # Conver the image to float between 0 and 1
        image = np.asarray(image) / 255.0

        if change_colors:
            # Change color distribution
            for j in range(3):
                image[:, :, j] = (image[:, :, j] + np.random.uniform(0, 1)) / 2.0

        # Invert the colors at the location of the number
        image[batch_binary[i]] = 1 - image[batch_binary[i]]
        batch[i] = image
    return batch, batch_raw

batch_size = 4
batch, batch_raw = color_digits_batch(x_train, batch_size=batch_size, change_colors=False)

fig, axs = plt.subplots(2, batch_size, figsize=(15,3))
for i in range(batch_size):
    axs[0, i].imshow(batch[i])
    axs[1, i].imshow(batch_raw[i])
    axs[0, i].axis("off")
    axs[1, i].axis("off")
plt.tight_layout()
plt.show()