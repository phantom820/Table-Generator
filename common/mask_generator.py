import numpy as np
import cv2 as cv

# Preprocessor
''' Operations to appl befor generating mask '''
class PreProcessor:
    ''' grayscale the image '''
    def grayscale(self,img):
        grayscaled = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        return grayscaled
    
    ''' thresholding the image to a binary image '''
    def threshold(self,img,mode='adaptive'):
        if mode == 'adaptive':
            thresh = cv.adaptiveThreshold(img, 255, 1, 1, 11, 2)
            return thresh
        elif mode=='otsu':
            _,thresh = cv.threshold(img,128,255,cv.THRESH_BINARY |cv.THRESH_OTSU)
            return thresh

    ''' apply preprocessing steps ''' 
    def preprocess(self,img):
        grayscaled = self.grayscale(img)
        thresholded = self.threshold(grayscaled)
        return thresholded

# Mask Generator
''' From the given pdf image generate table mask (label). This is done as follows.
- Compute absolute difference between raw pdf img and outlined img
- Apply adaptive thresholding to resulting image to obtain binary image
- Detect external contours in binary image and fill bounding box regions of contours '''

class MaskGenerator:
    def __init__(self):
        self.preprocessor = PreProcessor()
       
    ''' fill region with specified contours '''
    def fill(self,shape,contours):
        filled_binary_mask = np.zeros(shape,dtype=np.uint8)
        bounding_rectangles = []
        for contour in contours:
            rect = cv.boundingRect(contour)
            x,y,w,h = rect
            filled_binary_mask[y:y+h,x:x+w] = 255
        return filled_binary_mask
            
    ''' fill the mask '''
    def fill_mask(self,mask):
        binary_mask = self.preprocessor.preprocess(mask)
        contours, _ = cv.findContours(binary_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        binary_mask = self.fill(binary_mask.shape,contours)
        return binary_mask
    
    ''' generate table mask taking difference of 2 imgs '''
    def mask(self,raw_img,outlined_img):
        x = raw_img
        y = outlined_img
        mask = abs(x-y)
        filled_mask = self.fill_mask(mask)
        return filled_mask
    
    def masks(self,raw_imgs,outlined_imgs):
        masks = []
        for i in range(len(raw_imgs)):
            x = raw_imgs[i]
            y = outlined_imgs[i]
            mask = self.mask(x,y)
            masks.append(mask)
        return masks