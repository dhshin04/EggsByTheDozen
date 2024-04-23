import cv2


class Parasite:

    def __init__(self, center, height, width, angle):
        self.center = center
        self.height = height
        self.width = width
        self.angle = angle

    def getDistance(self, other):
        return (self.center.x-other.center.x)^2 + (self.center.y-other.center.y)^2
    
    def getDistance(self, x,y):
        return (self.center.x-x)^2 + (self.center.y-y)^2
    
    def getCenter(self):
        return self.center