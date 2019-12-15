import uuid

"""
Pobj -> Beautifulsoup 객체
Dobj -> webelement 객체
size -> 해당 block이 웹 페이지 상 차지하는 width와 height
location -> 해당 block의 왼쪽 상위 좌표 값(x, y)
id -> block들을 구분하기 위한 식별자
parent -> dom tree 상에서 해당 block의 부모 block
children -> dom tree 상에서 해당 block의 자식 block
"""
class Block:
    def __init__(self, Pobj, Dobj):
        self.Pobj = Pobj  # parser 객체
        self.Dobj = Dobj  # driver 객체
        self.size = {}  # web element의 width와 height
        self.location = {}  # web element의 left top의 좌표값
        self.id = str(uuid.uuid4())  # 블락들을 구분하기 위한 id
        self.parent = []  # 해당 블락의 부모 블락
        self.children = []  # 해당 블락의 자식 블락들
        self.cuttable = False  # 의미 있는 블락인지 확인하기 위한 변수(True로 설정되면 의미없는 블락)
        self.divided = False  # 차후 해당 블락이 나누어졌는지를 확인하기 위한 변수
        self.center = []

        self.setBGcolor(Dobj.value_of_css_property("background-color"))  # block의 배경색 속성 초기화
        self.setSize(Dobj.size['height'], Dobj.size['width'])  # block의 size 속성 초기화
        self.setLocation(Dobj.location['x'], Dobj.location['y'])  # block의 location 속성 초기화
        self.setVisibility(Dobj.value_of_css_property("visibility"))  # block의 visibility 속성 초기화
        self.setCenter()

    def setCenter(self):
        x = self.getX()
        y = self.getY()
        width = self.getWidth()
        height = self.getHeight()
        centerx = (x+width)/2
        centery = (y+height)/2
        self.center = [centerx, centery]

    def getCenter(self):
        return self.center

    def setCut(self):
        self.cuttable = True

    def isCut(self):
        return self.cuttable

    def getID(self):
        return self.id

    def setBGcolor(self, BGcolor):
        self.BGcolor = BGcolor

    def getBGcolor(self):
        return self.BGcolor

    def setSize(self, height, width):
        self.size['height'] = height
        self.size['width'] = width

    def getHeight(self):
        return self.size['height']

    def getWidth(self):
        return self.size['width']

    def setLocation(self, x, y):
        self.location['x'] = x
        self.location['y'] = y

    def getX(self):
        return self.location['x']

    def getY(self):
        return self.location['y']

    def setVisibility(self, visible):
        self.visible=visible

    def getVisibility(self):
        if self.visible == "hidden":
            return False
        else:
            return True

    def setParent(self, parent):
        self.parent.append(parent)

    def getParent(self):
        return self.parent[0]

    def setChild(self, child):
        self.children.append(child)

    def getChildren(self):
        return self.children

    def getId(self):
        return self.id

    def isNone(self):
        display = self.Dobj.value_of_css_property("display")
        if display == "none":
            return True
        else:
            return False

    def isblock(self):
        display = self.Dobj.value_of_css_property("display")
        if display == "block":
            return True
        else:
            return False

    def isinline(self):
        display = self.Dobj.value_of_css_property("display")
        if "inline" in display:
            return True
        else:
            return False

    # parent블락의 자식들 중 해당 블락이 몇 번째 자식인지 index로 알려주는 메소드
    def findBlockIndex(self):
        children = self.getParent().getChildren()

        for index in range(len(children)):
            if children[index].getId() == self.getId():
                return index

    """
    BeautifulSoup 객체를 통해 parser 객체에 해당하는 webelement 객체를 구하는 메소드
    pchild -> bs4.element.Tag 객체
    dchild -> webelement 객체
    
    1. 먼저 pboj를 통해 찾고자 하는 webelement의 태그이름을 얻어낸다.(pobj.name)
    2. 찾고자 하는 webelement가 부모의 첫번쨰 자식인지 아닌지에 따라 서로 다른 driver 메소드를 적용한다.
     2-1. 첫번째 자식
        부모 weblemnt(self.Dobj)에 find_element_by_tag_name 메소드를 적용해서 첫번째 자식 webelement를 구한다.
     2-2. 그 외 자식
        이전 형제 weblement(pre_dobj)에 find_element_by_xpath 메소드를 적용해서 해당 weblement를 구한다.
    """
    def get_Dobj(self, pre_dobj, pobj, is_first_child):
        tag = pobj.name
        if is_first_child: # 첫번째 자식
            dobj = self.Dobj.find_element_by_tag_name(tag)

        else: # 그외 자식
            expression = "following-sibling::%s[1]" %(tag)
            dobj = pre_dobj.find_element_by_xpath(expression)
        return dobj
