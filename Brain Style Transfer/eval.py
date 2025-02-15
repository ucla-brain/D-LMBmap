import os
import numpy as np
import math
# import tifffile
import cv2

def psnr(img1, img2):
   mse = np.mean((img1/1.0 - img2/1.0) ** 2 )
   if mse < 1.0e-10:
      return 100
   return 10 * math.log10(255.0**2/mse)

import numpy
from numpy import cov
from numpy import trace
from numpy import iscomplexobj
from scipy.linalg import sqrtm

def fid(act1, act2):
    # calculate mean and covariance statistics
    mu1, sigma1 = act1.mean(axis=0), cov(act1, rowvar=False)
    mu2, sigma2 = act2.mean(axis=0), cov(act2, rowvar=False)
    # calculate sum squared difference between means
    ssdiff = numpy.sum((mu1 - mu2)**2.0)
    # calculate sqrt of product between cov
    covmean = sqrtm(sigma1.dot(sigma2))
    # check and correct imaginary numbers from sqrt
    if iscomplexobj(covmean):
        covmean = covmean.real
    # calculate score
    fid = ssdiff + trace(sigma1 + sigma2 - 2.0 * covmean)
    return fid

root = 'results/model1/test_latest/images'
dirs = filter(lambda x: os.path.isdir(os.path.join(root, x)), os.listdir(root))
dirs = sorted(list(dirs))

if __name__ == '__main__':
    for d in dirs:
        tiff = sorted(os.listdir(os.path.join(root, d)))
        print(tiff)

        s = 0
        l = len(tiff) // 6
        for i in range(l):
            img1 = cv2.imread(os.path.join(root, d, tiff[(6*(i-1))+2]), 0)
            print(os.path.join(root, d, tiff[(6*(i-1))+2]))
            img2 = cv2.imread(os.path.join(root, d, tiff[(6*(i-1))+1]), 0)
            print(os.path.join(root, d, tiff[(6*(i-1))+1]))
            # print(d, dirs2[k])


            dmin1 = img1.min()
            dmax1 = img1.max()
            data_img1 = (img1 - dmin1) / (dmax1 - dmin1 + 1)
            dmin2 = img2.min()
            dmax2 = img2.max()
            data_img2 = (img2 - dmin2) / (dmax2 - dmin2 + 1)

            # tmp = psnr(data_img1, data_img2)
            # tmp = ssim(data_img1, data_img2)
            tmp = fid(data_img1, data_img2)

            print(tmp)
            s += tmp
        print(d, '%.5f' % (s / l))