"""

"""

import cv2
from tqdm import tqdm
import os


def add_logo_to_image(logo: cv2,
                      image: cv2,
                      margin: float = 0.02,
                      logo_size_w: float = 0.2,
                      logo_size_h: float = 0.35) -> cv2:
    """
    Add the logo image in the image. The position of the image is going to be
    in the lower center of the image. A lower margin exists, and it's going to
    be margin times the height of the image.
    Also, the logo is resized logo_size times the height of the images.

    :param logo:
    :param image:
    :param margin:
    :param logo_size_w:
    :param logo_size_h:

    :return:
    """
    logo_h, logo_w, logo_c = logo.shape
    im_h, im_w, im_c = image.shape

    if im_w > im_h:
        # logo is going to be logo_size times the height of the image
        new_logo_h = int(logo_size_h * im_h)
        resize_factor = new_logo_h / logo_h
        new_logo_w = int(logo_w * resize_factor)

        resized_logo = cv2.resize(logo, (new_logo_w, new_logo_h))
    else:
        # logo is going to be logo_size times the height of the image
        new_logo_w = int(logo_size_w * im_w)
        resize_factor = new_logo_w / logo_w
        new_logo_h = int(logo_h * resize_factor)

        resized_logo = cv2.resize(logo, (new_logo_w, new_logo_h))

    # add the logo to the image
    # calculate the position of the logo in the image
    w_start_pixel = int(im_w/2) - int(new_logo_w/2)
    w_finish_pixel = w_start_pixel + new_logo_w

    n_pixels_margin = int(im_h * margin)
    h_start_pixel = im_h - n_pixels_margin - new_logo_h
    h_finish_pixel = h_start_pixel + new_logo_h

    image_with_logo = image.copy()

    if logo_c > 3:
        # image is png with transparent background
        for i, row in enumerate(resized_logo):
            for j, pixels in enumerate(row):
                if pixels[-1] != 0:
                    image_with_logo[h_start_pixel+i, w_start_pixel+j, :] = pixels[:3]

    else:
        # is a normal image
        image_with_logo[h_start_pixel:h_finish_pixel,
                        w_start_pixel:w_finish_pixel, :] = resized_logo

    return image_with_logo


if __name__ == '__main__':

    logo_path = '/home/bea/Downloads/Sello_blanco.png'
    folder_images_path = '/home/bea/Downloads/Hola/'

    if not os.path.isfile(logo_path):
        print(f'El fichero del logo "{logo_path}" no existe')

    elif not os.path.exists(folder_images_path):
        print(f'La carpeta  "{folder_images_path}" no existe')

    else:
        images_logo_path = os.path.join(folder_images_path, 'logo_images')

        for image_name in tqdm(os.listdir(folder_images_path)):
            image_path = os.path.join(folder_images_path, image_name)
            image_with_logo_path = os.path.join(images_logo_path, image_name)

            if not os.path.exists(images_logo_path):
                os.makedirs(images_logo_path)

            if not os.path.isfile(image_path):
                continue

            # load images
            image_logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
            image = cv2.imread(image_path)

            image_with_logo = add_logo_to_image(image_logo, image)

            cv2.imwrite(image_with_logo_path, image_with_logo)
