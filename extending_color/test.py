from PIL import Image
import pywt 
import os
import numpy as np
from scipy.fftpack import dct
from scipy.fftpack import idct

img = Image.open('./temp/original_image')
watermark = Image.open('./temp/watermark_image')
watermark = watermark.convert('L')

#img_array = np.array(img.getdata(), dtype=np.float).reshape((2048, 2048))
watermark_array = np.array(watermark.getdata(), dtype=np.float).reshape((128, 128))


grey = img.convert('L')
print(img.getpixel((1, 1)))
print(grey.getpixel((1, 1)))
print('-------------------')
a = np.array(img.getdata(), dtype=np.float)
b = np.array(grey.getdata(), dtype=np.float)

print(len(a))
print(len(b))
print(a[0])
print(b[0])
c = Image.open('./temp/original_image').resize((2048, 2048))
red = []
green = []
blue = []
for i in range(2048):
    for j in range(2048):
        r, g, b = c.getpixel((j, i))
        red.append(r)
        green.append(g)
        blue.append(b)
print(red[:5])
print(len(red))
print(green[:5])
print(blue[:5])

red, green, blue = np.array(red, dtype=np.float), np.array(green, dtype=np.float), np.array(blue, dtype=np.float)
print(red, green, blue)
print(len(red), len(green), len(blue))

img_array = (red, green, blue)
def apply_dct(image_array):
    size = image_array[0].__len__()
    all_subdct = np.empty((size, size))
    for i in range (0, size, 8):
        for j in range (0, size, 8):
            subpixels = image_array[i:i+8, j:j+8]
            subdct = dct(dct(subpixels.T, norm="ortho").T, norm="ortho")
            all_subdct[i:i+8, j:j+8] = subdct

    return all_subdct

def process_coefficients(imArray, model, level):
    coeffs=pywt.wavedec2(data = imArray, wavelet = model, level = level)
    coeffs_H=list(coeffs) 
   
    return coeffs_H

def embed_watermark(watermark_array, orig_image):
    watermark_array_size = watermark_array[0].__len__()
    watermark_flat = watermark_array.ravel()
    ind = 0
    for x in range (0, orig_image.__len__(), 8):
        for y in range (0, orig_image.__len__(), 8):
            if ind < watermark_flat.__len__():
                subdct = orig_image[x:x+8, y:y+8]
                subdct[y_axis][x_axis] = watermark_flat[ind]
                orig_image[x:x+8, y:y+8] = subdct
                ind += 1 


    return orig_image

def inverse_dct(all_subdct):
    size = all_subdct[0].__len__()
    all_subidct = np.empty((size, size))
    for i in range (0, size, 8):
        for j in range (0, size, 8):
            subidct = idct(idct(all_subdct[i:i+8, j:j+8].T, norm="ortho").T, norm="ortho")
            all_subidct[i:i+8, j:j+8] = subidct

    return all_subidct

def w2d():
    model = "haar"
    level = 1
    coeffs_img_red = process_coefficients(img_array[0], model, level=level)
    coeffs_img_green = process_coefficients(img_array[1], model, level=level)
    coeffs_img_blue = process_coefficients(img_array[2], model, level=level)
    dct_red_array = apply_dct(coeffs_img_red[0])
    dct_green_array = apply_dct(coeffs_img_green[0])
    dct_blue_array = apply_dct(coeffs_img_blue[0])
    dct_red_array = embed_watermark(watermark_array, dct_red_array)
    dct_green_array = embed_watermark(watermark_array, dct_green_array)
    dct_blue_array = embed_watermark(watermark_array, dct_blue_array)
    coeffs_img_red[0] = inverse_dct(dct_red_array)
    coeffs_img_green[0] = inverse_dct(dct_green_array)
    coeffs_img_blue[0] = inverse_dct(dct_blue_array)
    recons_red = pywt.waverec2(coeffs_img_red, model)
    recons_green = pywt.waverec2(coeffs_img_green, model)
    recons_blue = pywt.waverec2(coeffs_img_blue, model)

    final_img = 

w2d()
