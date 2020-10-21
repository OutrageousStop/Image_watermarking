from PIL import Image
import pywt 
import os
import numpy as np
from scipy.fftpack import dct
from scipy.fftpack import idct

component_map = {'r': 0, 'g': 1, 'b': 2}
x_axis = 5
y_axis = 5

def apply_dct(image_array):
    size = image_array[0].__len__()
    all_subdct = np.empty((size, size))
    for i in range (0, size, 8):
        for j in range (0, size, 8):
            subpixels = image_array[i:i+8, j:j+8]
            subdct = dct(dct(subpixels.T, norm="ortho").T, norm="ortho")
            all_subdct[i:i+8, j:j+8] = subdct

    return all_subdct

def inverse_dct(all_subdct):
    size = all_subdct[0].__len__()
    all_subidct = np.empty((size, size))
    for i in range (0, size, 8):
        for j in range (0, size, 8):
            subidct = idct(idct(all_subdct[i:i+8, j:j+8].T, norm="ortho").T, norm="ortho")
            all_subidct[i:i+8, j:j+8] = subidct

    return all_subidct

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

def get_watermark(dct_watermarked_coeff, watermark_size):
    
    subwatermarks = []

    for x in range (0, dct_watermarked_coeff.__len__(), 8):
        for y in range (0, dct_watermarked_coeff.__len__(), 8):
            coeff_slice = dct_watermarked_coeff[x:x+8, y:y+8]
            subwatermarks.append(coeff_slice[y_axis][x_axis])

    watermark = np.array(subwatermarks).reshape(watermark_size, watermark_size)

    return watermark

def recover_watermark(image_array, model='haar', level = 1):


    coeffs_watermarked_image = process_coefficients(image_array, model, level=level)
    dct_watermarked_coeff = apply_dct(coeffs_watermarked_image[0])
    
    watermark_array = get_watermark(dct_watermarked_coeff, 128)

    watermark_array =  np.uint8(watermark_array)

    img = Image.fromarray(watermark_array)
    img.save('./result/recovered_watermark.jpeg')

def process_coefficients(imArray, model, level):
    coeffs=pywt.wavedec2(data = imArray, wavelet = model, level=level)
    coeffs_H=list(coeffs) 
   
    return coeffs_H

def getColorImage(name, size):
    image = Image.open(name).resize((size, size))
    image = image.convert("RGB")
    img = np.array(image)
    return img

def getImage(name, size):
    image = Image.open(name).resize((size, size))
    image = image.convert('L')
    img = np.array(image)
    return img

def singleComponentwatermark(img_name, watermark_name, component):
    model = 'haar'
    level = 1
    idx = component_map[component]
    
    img = getColorImage(img_name, 2048)
    watermark = getImage(watermark_name, 128)
    img_working = img[..., idx]
    
    coeffs_img_working = process_coefficients(img_working, model, level)
    dct_working = apply_dct(coeffs_img_working[0])
    dct_working = embed_watermark(watermark, dct_working)
    coeffs_img_working[0] = inverse_dct(dct_working)
    img_working = pywt.waverec2(coeffs_img_working, model)
    img[..., idx] = img_working
    img = Image.fromarray(np.uint8(img)).convert("RGB")
    img.save('./result/image_with_watermark.jpeg')

def extractFromSingleComponent(img_name, component):
    model = 'haar'
    level = 1
    idx = component_map[component]
    img = getColorImage(img_name, 2048)
    
    img_working = img[..., idx]
    watermark = process_coefficients(img_working, model, level)
    dct_watermark = apply_dct(watermark[0])
    watermark = get_watermark(dct_watermark, 128)
    rec_watermark = Image.fromarray(np.uint8(watermark))
    rec_watermark.save('./result/recovered_watermark.jpeg')

def greywatermark(img_name, watermark_name):
    model = 'haar'
    level = 1
    img = getImage(img_name, 2048)
    watermark = getImage(watermark_name, 128)
    coeffs_img = process_coefficients(img, model, level)
    dct_img = apply_dct(coeffs_img[0])
    dct_img = embed_watermark(watermark, dct_img)
    coeffs_img[0] = inverse_dct(dct_img)
    img = pywt.waverec2(coeffs_img, model)
    img = Image.fromarray(np.uint8(img)).convert("RGB")
    img.save('./result/image_with_watermark.jpeg')

def extractFromgrey(img_name):
    model = 'haar'
    level = 1
    img = getImage(img_name, 2048)
    watermark = process_coefficients(img, model, level)
    dct_watermark = apply_dct(watermark[0])
    watermark = get_watermark(dct_watermark, 128)
    rec_watermark = Image.fromarray(np.uint8(watermark))
    rec_watermark.save('./result/recovered_watermark.jpeg')

def allComponentwatermark(img_name, watermark_name):
    model = 'haar'
    level = 1
    img_array = getColorImage(img_name, 2048)
    watermark_array = getColorImage(watermark_name, 128)
    
    img_array_r, img_array_g, img_array_b = img_array[..., 0], img_array[..., 1], img_array[..., 2]
    watermark_array_r, watermark_array_g, watermark_array_b = watermark_array[..., 0], watermark_array[..., 1], watermark_array[..., 2]
    
    coeffs_img_r = process_coefficients(img_array_r, model, level)
    coeffs_img_g = process_coefficients(img_array_g, model, level)
    coeffs_img_b = process_coefficients(img_array_b, model, level)
    
    dct_array_r = apply_dct(coeffs_img_r[0])
    dct_array_g = apply_dct(coeffs_img_g[0])
    dct_array_b = apply_dct(coeffs_img_b[0])
    
    dct_array_r = embed_watermark(watermark_array_r, dct_array_r)
    dct_array_g = embed_watermark(watermark_array_g, dct_array_g)
    dct_array_b = embed_watermark(watermark_array_b, dct_array_b)
    
    coeffs_img_r[0] = inverse_dct(dct_array_r)
    coeffs_img_g[0] = inverse_dct(dct_array_g)
    coeffs_img_b[0] = inverse_dct(dct_array_b)
    
    img_array[..., 0] = pywt.waverec2(coeffs_img_r, model)
    img_array[..., 1] = pywt.waverec2(coeffs_img_g, model)
    img_array[..., 2] = pywt.waverec2(coeffs_img_b, model)
    
    rec_img = Image.fromarray(np.uint8(img_array)).convert("RGB")
    rec_img.save('./result/image_with_watermark.jpeg')

def extractFromColorImage(img_name):
    model = 'haar'
    level = 1
    rec_img = getColorImage(img_name, 2048)
    
    rec_img_r, rec_img_g, rec_img_b = rec_img[..., 0], rec_img[..., 1], rec_img[..., 2]
    
    watermark_r = process_coefficients(rec_img_r, model, level)
    watermark_g = process_coefficients(rec_img_g, model, level)
    watermark_b = process_coefficients(rec_img_b, model, level)
    
    dct_watermark_r = apply_dct(watermark_r[0])
    dct_watermark_g = apply_dct(watermark_g[0])
    dct_watermark_b = apply_dct(watermark_b[0])
    
    watermark_r = get_watermark(dct_watermark_r, 128)
    watermark_g = get_watermark(dct_watermark_g, 128)
    watermark_b = get_watermark(dct_watermark_b, 128)
    
    base = np.ones((128, 128, 3))
    base[..., 0], base[..., 1], base[..., 2] = watermark_r, watermark_g, watermark_b
    
    rec_watermark = Image.fromarray(np.uint8(base))
    rec_watermark.save('./result/recovered_watermark.jpeg')

