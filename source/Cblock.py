
# 군집화된 block들의 정보를 저장하는 객체
class Cblock:
    def __init__(self, width, height, x, y, blockList):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.blockList = blockList

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getBlockList(self):
        return self.blockList
