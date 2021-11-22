import cv2 as cv

# Transformer
''' Transform a given image , to try and mimic real world data of scanned images. The following transforms applicable
- Gaussian Blur $k$ (kernel size), $(k,k)$ 
- Scale $(sx,sy)$ 
- Rotate $\theta$ '''

class Transformer:
    ''' blur (! later must investigate scan effect)'''
    def blur(self,img,kernel):
        sigma_x,sigma_y = 2,2
        blurred_img = cv.GaussianBlur(img,kernel,sigma_x,sigma_y)
        return blurred_img
    
    ''' rotate '''
    def rotate(self,img,theta:float,border=(255,255,255)):
        height, width = img.shape[:2]
        center = (width/2, height/2)
        rotate_matrix = cv.getRotationMatrix2D(center=center, angle=theta, scale=1)
        rotated_img = cv.warpAffine(src=img, M=rotate_matrix, dsize=(width, height),borderValue=border)
        return rotated_img
    
    ''' dirtify data by applying sequence of transformations'''
    def dirtify(self,img,k:int,s_x:int,s_y:int,theta:float,mask:bool):
        m,n = img.shape[:2]
        m,n = int(s_y*m),int(s_x*n)
        dim = (n,m)
        if not mask:
            x = self.blur(img,kernel=(k,k))
            y = cv.resize(x, dim, interpolation = cv.INTER_AREA)
            z = self.rotate(y,theta=theta)
        else:
            x = img
            y = cv.resize(x, dim, interpolation = cv.INTER_AREA)
            z = self.rotate(y,theta=theta,border=(0,0,0))
        return z
