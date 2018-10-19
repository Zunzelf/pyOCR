"""
===========================
@Author  : zunzelf
@Version: 0.1    19/10/2018
These are the implementations of segmentation algorithms
===========================
"""

# x-y-projection segmentation

def y_proj(image):
	res = []
	for j in range(len(image)):
		temp = 0
		for i in range(len(image[j])):
			if image[j][i] == 1 :

				temp += 1
		res.append(temp)
	return res


def x_proj(image):
	res = []
	for i in range(len(image[0])):
		temp = 0
		for j in range(len(image)):
			if image[j][i] == 1 :
				temp += 1
		res.append(temp)
	return res

def single_crop_point(image, pad = 0):
	xs = x_proj(image)
	ys = y_proj(image)
	s_x, s_y = (0, 0)
	e_x, e_y = (0, 0)
	# x points
	for idx, i in enumerate(xs):
		if i > 0 :
			if s_x == 0 :
				s_x = idx
			else :
				e_x = idx
	# y points
	for idx, i in enumerate(ys):
		if i > 0 :
			if s_y == 0 :
				s_y = idx
			else :
				e_y = idx
	return s_x-pad, s_y-pad, e_x+pad, e_y+pad

def xy_proj_crop(image, img_bin, pad = 0):
    crop_point = single_crop_point(img_bin, pad = pad)
    return image.crop(crop_point)

