import numpy as np
from torch.utils.data import Dataset, DataLoader
import torchvision
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os
import random
import natsort
import cv2 
from PIL import Image
import pandas
import matplotlib.pyplot as plt

class FaceLandMark_Loader(Dataset):
    def __init__(self, root, IsAug = True):
        super(FaceLandMark_Loader, self).__init__()
        print("#### MotionLoader ####")
        print("####### load data from {} ######".format(root))

        # read list of images
        # read list of landmarks
        # read list of bbox
        self.img_path = os.path.join(root, "img")
        self.ldmks_path = os.path.join(root, "ldmks")
        self.bbox_leftcorner_coord_path = os.path.join(root, "bbox_leftcorner_coord")

        self.img_list = natsort.natsorted(os.listdir(self.img_path))
        self.ldmks_list = natsort.natsorted(os.listdir(self.ldmks_path))
        self.bbox_list = natsort.natsorted(os.listdir(self.bbox_leftcorner_coord_path))

        assert len(self.img_list) == len(self.ldmks_list)

        print(img_list[:10])
        print(ldmks_list[:10])
        
        self.std = 0.2
        self.mean = 0

        

        #using augmentation functions which do not effect on landmarks position 
    def __getitem__(self, idx):
        
        # get an image
        # get a landmark info
        # get a bbox info
        img = Image.open(self.img_path + '/' + self.img_list[idx])
        
        ldmks = pandas.read_csv(self.ldmks_path +'/'+self.ldmks_list[idx],  header=None, sep=' ')
        ldmks = np.asarray(ldmks) # shape : (70, 2), last two row for centers of eyes

        bbox_leftcorner = pandas.read_csv(self.bbox_leftcorner_coord_path +'/'+self.bbox_list[idx],  header=None, sep=' ')
        bbox_leftcorner = np.asarray(bbox_leftcorner) # shape : (2, 1) # x, y
        
        '''
        Paper:
        During training, we perform data augmentation including
        rotations, perspective warps, < -- landmark also should be changed 
        blurs, modulations to brightness and contrast, addition of noise, and conversion to grayscale. < -- does not be related with landmark
        '''

        #blurs, modulations to brightness and contrast, addition of noise, and conversion to grayscale. < -- does not be related with landmark
        img = F.adjust_brightness(img, brightness_factor = random.uniform(0.5,1.5)) # brightness_factor 0(black) ~ 2(white)
        img = F.adjust_contrast(img, contrast_factor = random.uniform(0.5,1.5)) # contrast_factor 0(solid gray) ~ 2
        img = F.gaussian_blur(img, kernel_size = random.randint(3, 7))
        img = F.rgb_to_grayscale(img, num_output_channels =3)
        img = img + torch.randn(img.size()) * self.std + self.mean 
        
        #crop image 256x256 including face info --> how? # crop이 가장 위에 가야지 계산 효율성이 좋을 듯!
    
        #conduct augmentation --> how handle the annotation simultaneously??

        return landmark_GT, input_Image, crop_info

    def __len__(self):
        return len(self.img_list)

def get_dataloader(dataroot, batch_size, IsSuffle = True):
    dataset = MotionLoader(dataroot)
    print("# of dataset:", len(dataset))

    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=IsSuffle, drop_last=True)
   
    return dataloader, dataset


if __name__ == '__main__':
    idx = 0
    root = "/data2/MS-FaceSynthetic"
    temp = FaceLandMark_Loader(root = "/data2/MS-FaceSynthetic")
    
