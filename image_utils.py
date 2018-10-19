from PIL import Image
import numpy as np
import os
from time import time
import pickle
import segmentation

def load_image(path):
    return Image.open(path)

def mean_rgb(rgb):
    return (sum(rgb)/len(rgb))

def image_binary(image):
    result = []
    (h, w) = image.size
    for x in range(w):
        row = []
        for y in range(h):
            value = mean_rgb(image.getpixel((y,x)))
            if value >= 125:
                res = 0
            else :
                res = 1 
            row.append(res)
        result.append(row)
    return result

def image_array(image):
    img = load_image(image)
    return np.array(img)

def template_maker(path, prepro = False, save_path = ''):
    fn = os.listdir(path)
    result = []
    for file in fn:
        path_file = os.path.join(path, file)
        img = load_image(path_file)
        if prepro :
            img_bin = image_binary(img)
            cropped = segmentation.xy_proj_crop(img, img_bin, pad = 5)
            size = (32, 32)
            sample = cropped.resize(size)
            img_bin = image_binary(sample)
        dats = {
            'id' : file,
            'pixel' : img_bin
        }
        result.append(dats)
    if save_path == '' :
        return result
    else :
        with open(save_path, 'wb') as f:
            pickle.dump(result, f)

def template_matching(mdl, trg):
    # W1 = 14
    # W2 = 10
    # W3 = 5
    # W4 = 0
    t = 0
    # dk1 equation :
    h = len(mdl)
    for y in range(h) :
        w = len(mdl[y])
        for x in range(w) :
           if mdl[x][y] == 1 :
                if trg[x][y] == 1 :
                    t += 14  # case of W1
                    pass
                neigh = neighbour(x, y, trg)
                if neigh == 'en' :
                    t += 10
                elif neigh == 'on' :
                    t += 5
    b = h*w*14 # as in paper -> accumulation of W1 by the number of pixel 
    return ((t+0.0)/b)

def recognition(mdls, trg):
    res_i = 0
    tmp_res = 0
    size = len(mdls)
    for i in range(size):
        score = template_matching(mdls[i]['pixel'], trg)
        if score > tmp_res :
            tmp_res = score
            res_i = i
    return mdls[res_i]['id']

def neighbour(x, y, trg):
    res_i = 8
    for i in range(8):
        (nx, ny) = translate(i, x, y)
        if trg[nx][ny] == 1 :
            res_i = i
            break
    if res_i == 8 :
        return 'nn'
    elif res_i % 2 == 0 :
        return 'en'
    return 'on'

def translate(pnt, x, y):
    if pnt == 0 :
        res = (x, y+1)
    elif pnt == 1 :
        res = (x+1, y+1)
    elif pnt == 2 :
        res = (x+1, y)
    elif pnt == 3 :
        res = (x+1, y-1)
    elif pnt == 4 :
        res = (x, y-1)
    elif pnt == 5 :
        res = (x-1, y-1)
    elif pnt == 6 :
        res = (x-1, y)
    elif pnt == 7 :
        res = (x-1, y+1)
    return res

def load_templates(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def print_img_bin(image):
    for i in image:
        print i

import thinning
if __name__ == '__main__':
    start = time()
    path_train = os.path.join(os.path.sep, "D:","\\proyek","s2","tugas","PatternRecognition","Data","arial", "train")
    path_test = os.path.join(os.path.sep, "D:","\\proyek","s2","tugas","PatternRecognition","Data","arial", "test")
    path_test2 = os.path.join(os.path.sep, "D:","\\proyek","s2","tugas","PatternRecognition","Data","arial", "test2")

    # # just making dataset~
    # list_dir = os.listdir(path_test)
    
    # for path in list_dir:
    #   img = load_image(os.path.join(path_test, path))
    #   (h, w) = img.size
    #   size = (24, 24)
    #   img = img.resize((32, 32))
    #   img.save(os.path.join(path_train, path), "PNG")

    # # making data train templates file
    # template_maker(path_test, True, os.path.join(path_train, 'train_pkl.pkl'))

    # load image templates
    templates = load_templates(os.path.join(path_train, 'train_pkl.pkl'))

    # # test algorithm - single char, single sample
    # # load test sample
    for i in range(10):
        sample = load_image(os.path.join(path_test, '%d.PNG') % i)
    # # resize image
    # size = (32, 32)
    # sample = sample.resize(size)
    # img_bin = image_binary(sample)
    # thinned = thinning.zhangSuen(img_bin)
    # # test matching
    # print recognition(templates, img_bin)
    # print recognition(templates, thinned)

    # # test algorithm - single char, multi sample
    # list_dir = os.listdir(path_test2)
    
    # for path in list_dir:
    #     img = load_image(os.path.join(path_test2, path))
    #     (h, w) = img.size
    #     size = (32, 32)
    #     img = img.resize(size)
    #     img_bin = image_binary(img)
    #     thinned = thinning.zhangSuen(img_bin)
    #     print recognition(templates, thinned)

    # preprocessing
        img_bin = image_binary(sample)
        cropped = segmentation.xy_proj_crop(sample, img_bin, pad = 10)
        size = (32, 32)
        sample = cropped.resize(size)
        img_bin = image_binary(sample)
        thinned = thinning.zhangSuen(img_bin)
        print recognition(templates, thinned)
    # print_img_bin(templates[16]['pixel'])
    # print templates[16]['id']
    # print_img_bin(thinned)

    print time() - start