import numpy as np
import cv2
import math 
import random

class ellipseDetector:
    
    def __init__(self, ):
        pass
    
    def assessEllipse(self, ellipse):
        OT = 0.4 #OUTER THRESHOLD
        IT = 0.8 #INNER THRESHOLD
        
        (center_x, center_y), (major_axis, minor_axis), angle = ellipse

        # Calculate the area of the ellipse
        area = np.pi * (major_axis/2) * (minor_axis/2)

        # Calculate the aspect ratio of the ellipse
        ar = major_axis / minor_axis
        
        good_ratio = (ar > OT and ar < IT) or (ar > 1/IT and ar <1/OT)
        
        return (area > 700 and area < 2000 and good_ratio)
    

    def distPoint_Ellipse(self, BoundingRectangle, Point):
        (cxE, cyE), (WidthE, HeightE), rotE = BoundingRectangle
        ptX, ptY = Point[0], Point[1] * -1
        radX, radY = WidthE / 2, HeightE / 2
        angleToCenterE = math.atan2(ptY - cyE * -1, ptX - cxE)
        nearestEX, nearestEY = cxE + radX * math.cos(angleToCenterE), cyE * -1 + radY * math.sin(angleToCenterE)
        return (ptX - nearestEX) ** 2 + (ptY * -1 - nearestEY * -1) ** 2, (nearestEX, -1 * nearestEY)
    
    def fitEllipse_RANSAC(self, Contour):
        if len(Contour) < 5:
            print("Contour Too Small")
            
        
        maxInliers, bestFit = 0, ((0,0),(0,0),0)
        
        MaxIterations = int(len(Contour)/3)
        for i in range(MaxIterations):
            sample = np.array([Contour[i][0] for i in random.sample(range(len(Contour)),5)])
            potentFit = cv2.fitEllipseDirect(sample)
            
            if self.assessEllipse(potentFit):
                numInliers = 0
                for pt in Contour:
                    pt = tuple(pt[0])
                    d = self.distPoint_Ellipse(potentFit, pt)[0]
                    if d < 10:
                        numInliers += 1
                if numInliers > maxInliers:
                    maxInliers = numInliers
                    bestFit = potentFit
        
        return bestFit
    
    def fitEllipse_Polygon(self, Contour):
        area = int(cv2.contourArea(Contour))  # Cast area to int (though not necessary in Python)
        bounding_box = cv2.boundingRect(Contour)
        aspect_ratio = bounding_box[2] / bounding_box[3]  # Width divided by Height

        # Filter based on aspect ratio and minimum size
        elongation_factor = abs(1 - aspect_ratio)
        
        if 0.1 < elongation_factor and elongation_factor < 1 and 1000 < area < 4000:
            # Approximate contour to smooth shape
            epsilon = 0.01 * cv2.arcLength(Contour, True)
            approx = cv2.approxPolyDP(Contour, epsilon, True)

            if len(approx) > 4:  # Need at least 5 points to fit ellipse
                fitted_ellipse = cv2.fitEllipse(approx)
                # You can draw the ellipse on the image to visualize
                return fitted_ellipse
        return None
    
    