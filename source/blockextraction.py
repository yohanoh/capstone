from Block import Block
from Rule import Rule

# block 추출을 위한 객체
class extraction:
    def __init__(self, pbody, dbody):
        self.pbody = pbody
        self.dbody = dbody
        self.blockList = []

    # body 부분을 나타내는 block 객체를 생성
    # 생성된 block에 대해 어느 정도로 쪼갤지 결정하기 위해 divideblock 메소드를 호출
    def service(self):
        block = Block(self.pbody, self.dbody)
        self.divideblock(block)

        return self.blockList

    # 인자로 받은 block를 더 잘게 쪼갤지 여부를 rule에 기반하여 결정
    def divideblock(self, block):
        rule = Rule()

        if "script" in block.Pobj.name or block.Pobj.name == "iframe":
            return

        # 해당 block를 더 잘게 쪼갠다
        if rule.dividable(block):
            block.divided = True
            for childblock in block.getChildren():
                self.divideblock(childblock)

        # 해당 block를 쪼개지 않고 리스트에 저장한다.
        else:
            if not block.isCut():
                if block.getX() >= 0 and block.getY() >= 0 and block.getHeight() > 0 and block.getWidth() > 0:
                    self.fillList(block)

    def fillList(self, block):
        self.blockList.append(block)
