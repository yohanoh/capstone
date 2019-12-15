import cv2

def drawline(imgsrc, blockList, is_block, width, height):
    src = cv2.imread(imgsrc, cv2.IMREAD_COLOR)
    img = cv2.resize(src, dsize=(width, height), interpolation=cv2.INTER_LINEAR)

    for block in blockList:
        leftTopX = block.getX()
        leftTopY = block.getY()
        rightBottomX = leftTopX + block.getWidth()
        rightBottomY = leftTopY + block.getHeight()

        if is_block:
            img = cv2.rectangle(img, (leftTopX, leftTopY), (rightBottomX, rightBottomY), (0, 255, 0), 1)
        else:
            img = cv2.rectangle(img, (leftTopX, leftTopY), (rightBottomX, rightBottomY), (255, 0, 0), 1)

    return img
