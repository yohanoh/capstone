from Block import Block
import bs4
from bs4 import BeautifulSoup

# 블럭에 해당하는 html 구조에서 속성 값 및 텍스트 제거
# 구조적 영향을 주지 않는 br 태그는 제거
def remove_attr(Pobj):
    tagList = []
    tag = Pobj.name

    if not (tag == "br") and not (tag == "script"):
        tagList.append(tag)

    # 블락의 자식 태그를 확인 후 tagList에 저장한다.
    children = Pobj.children
    for child in children:
        if type(child) is not bs4.element.Tag:
            continue

        child_tag_list = remove_attr(child)
        for child_tag in child_tag_list:
            tagList.append(child_tag)

    if not (tag == "br") and not (tag == "script"):
        tag = "/" + tag
        tagList.append(tag)

    return tagList

class Rule:
    def __init__(self, threshhold=70000):
        self.threshhold = threshhold

    # 블럭의 자식 블럭들을 만들고 자식과 부모 관계를 설정한다.
    def makeChildBlock(self, block):
        is_first_child = True

        # Pobj와 Dobj 간에 태그 구조를 동일하게 처리하기 위한 갱신 작업
        html = block.Dobj.get_attribute("outerHTML")
        soup = BeautifulSoup(html, "html.parser")
        tag = block.Dobj.tag_name
        block.Pobj = soup.find(tag)

        children = block.Pobj.children
        for pchild in children:
            # Pboj.children를 통해 얻는 자식들중 string 자식도 포함되어있기 때문에
            # tag 자식만 블럭 객체로 생성해준다.
            if type(pchild) is not bs4.element.Tag:
                continue

            # style 속성이 visibility:hidden으로 설정되어 있는 경우 selenium이 탐색할 수 없으므로
            # 이는 수집하지 않는다.
            if pchild.has_attr('style'):
                style = pchild['style'].replace(" ", "")
                if "visibility:hidden" in style:
                    continue

            if is_first_child:
                dchild = None
                dchild = block.get_Dobj(dchild, pchild, is_first_child)
                is_first_child = False
            else:
                dchild = block.get_Dobj(dchild, pchild, is_first_child)

            childblock = Block(pchild, dchild) #자식에 해당하는 블럭 객체 생성
            childblock.setParent(block) #자식의 부모 블럭 설정
            block.setChild(childblock) #부모의 자식 블럭 설정

    """웹 페이지에서 불필요하다고 생각되는 데이터는 수집하지 않는다."""
    def garbage_cutter(self, block):

        """태그 이름을 통한 제거"""
        tag_name = block.Pobj.name
        if tag_name.lower() == 'header':
            return True

        if tag_name.lower() == "footer":
            return True

        """class 속성 값을 통한 제거"""
        if block.Pobj.has_attr('class'):
            class_names = block.Pobj.get('class')

            for class_name in class_names:
                class_name = class_name.lower()

                # 상단 헤더 영역 제거
                if "head" in class_name:
                    return True

                if "top" in class_name:
                    return True

                # 하단 푸터 영역 제거
                if "foot" in class_name:
                    return True

                if "copyright" in class_name:
                    return True

                if "bottom" in class_name:
                    return True

                # 광고 영역 제거
                if "promotion" in class_name:
                    return True

                # 네비게이션바 제거
                if "nav" in class_name:
                    return True

                if "sitemap" in class_name:
                    return True

                # 배너 제거
                if "banner" in class_name:
                    return True

                # 사이드바 제거
                if "sidebar" in class_name:
                    return True

                # sns 공유 제거
                if "share" in class_name or 'sns' in class_name:
                    return True

        """id 속성값을 통한 제거"""
        if block.Pobj.has_attr('id'):
            id_name = block.Pobj.get('id')
            id_name = id_name.lower()

            # 상단 헤더 영역 제거
            if "head" in id_name:
                return True

            if "top" in id_name:
                return True

            # 하단 푸터 영역 제거
            if "foot" in id_name:
                return True

            if "copyright" in id_name:
                return True

            if "bottom" in id_name:
                return True

            # 광고 부분 제거
            if "promotion" in id_name:
                return True

            # 네비게이션바 제거
            if "nav" in id_name:
                return True

            if "sitemap" in id_name:
                return True

            # 배너 제거
            if "banner" in id_name:
                return True

            # 사이드바 제거
            if "sidebar" in id_name:
                return True

            # sns 공유하기 제거
            if "share" in id_name or "sns" in id_name:
                return True

        return False

    """
    Rule 클래스의 메인 메소드
    나눈다. -> True 리턴, 나누지 않는다. -> False 리턴
    1. 사전 조건을 통해 불필요한 블럭들을 우선적으로 cut한다.(header, footer, sidebar 등)
    2. img 태그와 같이 나누면 의미단위가 파괴되는 블락은 더 이상 나누지 않는다.
    3. 나머지 블럭들은 자식 블럭들을 구한다. (차후 rule를 적용하기 위해)
    4. 그 후 태그 정보에 따라 적용되는 rule를 지정한다.    
    """
    def dividable(self, block):
        name = block.Pobj.name

        # 1. 사전 조건을 통해 불필요한 블럭들을 우선적으로 cut한다. (header, footer, sidebar 등)
        if block.isNone():
            block.setCut()
            return False

        if self.garbage_cutter(block):
            block.setCut()
            return False

        # 2. img 태그와 같이 나누면 의미단위가 파괴되는 블락은 더 이상 나누지 않는다.
        if name == "img":
            return False

        if self.istextNode(block):
            return False

        # 3. 나머지 블럭들은 자식 블럭들을 구한다. (차후 rule를 적용하기 위해)
        self.makeChildBlock(block)

        # 4. 그 후 태그 정보에 따라 적용되는 rule를 지정한다.
        if block.isinline():
            return self.inlineRules(block)

        elif name == "table":
            return self.tableRules(block)

        elif name == "ol" or name == "ul":
            return self.tableRules(block)

        elif name == "tr":
            return self.trRules(block)

        elif name == "td":
            return self.tdRules(block)

        elif name == "p":
            return self.pRules(block)

        else:
            return self.otherRules(block)

    # inline block에 적용되는 rule
    def inlineRules(self, block):
        # r1, r2, r3, r4, r5, r6, r8, r9, r11
        self.rule1(block)

        if block.isCut():
            return False

        elif self.rule2(block):
            return True

        elif self.rule3(block):
            return True

        elif self.rule4(block):
            return True

        elif self.rule5(block):
            return True

        elif self.rule6(block):
            return True

        elif self.rule8(block):
            return True

        elif self.rule9(block):
            return True

        elif self.rule11(block):
            return True

        return False

    # table 태그에 적용되는 rule
    def tableRules(self, block):
        # r1, r2, r3, r7, r9, r12
        self.rule1(block)

        if block.isCut():
            return False

        elif self.rule2(block):
            return True

        elif self.rule3(block):
            return True

        elif self.rule7(block):
            return True

        elif self.rule9(block):
            return True

        elif self.rule12(block):
            return True

        return False

    # tr 태그에 적용되는 rule
    def trRules(self, block):
        # r1, r2, r3, r7, r9, r12
        self.rule1(block)

        if block.isCut():
            return False

        elif self.rule2(block):
            return True

        elif self.rule3(block):
            return True

        elif self.rule7(block):
            return True

        elif self.rule9(block):
            return True

        elif self.rule12(block):
            return True
        return False

    # td 태그에 적용되는 rule
    def tdRules(self, block):
        # r1, r2, r3, r4, r8, r9, r10, r12
        self.rule1(block)

        if block.isCut():
            return False

        elif self.rule2(block):
            return True

        elif self.rule3(block):
            return True

        elif self.rule4(block):
            return True

        elif self.rule8(block):
            return True

        elif self.rule9(block):
            return True

        elif self.rule10(block):
            return True

        elif self.rule12(block):
            return True

        return False

    # p 태그가 적용되는 rule
    def pRules(self, block):
        # r1, r2, r3, r4, r5, r6, r8, r9, r11
        self.rule1(block)

        if block.isCut():
            return False

        elif self.rule2(block):
            return True

        elif self.rule3(block):
            return True

        elif self.rule4(block):
            return True

        elif self.rule5(block):
            return True

        elif self.rule6(block):
            return True

        elif self.rule8(block):
            return True

        elif self.rule9(block):
            return True

        elif self.rule11(block):
            return True

        return False

    # 지정된 태그가 아닌 나머지 태그가 적용되는 rule
    def otherRules(self, block):
        # r1, r2, r3, r4, r6, r8, r9, r11
        self.rule1(block)

        if block.isCut():
            return False

        elif self.rule2(block):
            return True

        elif self.rule3(block):
            return True

        elif self.rule4(block):
            return True

        elif self.rule6(block):
            return True

        elif self.rule8(block):
            return True

        elif self.rule9(block):
            return True

        elif self.rule11(block):
            return True

        return False

    # 해당 노드가 text node가 아니고, vaild한 children이 없을 경우 해당 블럭은 추출하지 않는다.
    def rule1(self, block):
        if not self.istextNode(block) and not self.hasValidChildNode(block):
            block.setCut()

    # 해당 노드가 자식 노드를 한 가지만 가지고 있고, 그 자식 노드가 vaild한 노드이면서 text node가 아닌 경우 나눈다.
    def rule2(self, block):
        if len(block.getChildren()) == 1:
            childblock = block.getChildren()[0]
            if self.isValidNode(childblock) and not self.istextNode(childblock):
                return True

        return False

    # 해당 블럭의 자식들 중 동일한 구조를 가진 자식들이 존재하는지 확인
    # 존재하지 않으면, divide
    # 존재하면 나누지 않는다.
    def rule3(self, block):
        children = block.getChildren()
        num_children = len(children)

        if num_children == 1:
            return True

        # script 자식에 대해서는 비교를 하지 않는다.
        for i in range(0, num_children-1):
            if children[i].Pobj.name == "script":
                continue
            for j in range(i, num_children):
                if children[j].Pobj.name == "script":
                    continue

                # 속성 값과 내부 텍스트를 제거하고 순수한 태그만 리스트 형태로 가져온다.
                html1 = remove_attr(children[i].Pobj)
                html2 = remove_attr(children[j].Pobj)

                tag_num1 = len(html1)
                tag_num2 = len(html2)

                # 두 태그 리스트의 개수가 다르면 서로 다른 구조
                if not (tag_num1 == tag_num2):
                    continue

                # 두 태그 리스트를 하나씩 비교해서 다르면 issame = False로 설정하고 break
                issame = True
                for k in range(tag_num1):
                    if not (html1[k] == html2[k]):
                        issame = False
                        break

                if issame:  # 같은 구조를 가진 자식이 둘 이상
                    return False
                elif not issame:  # 같은 구조를 가진 자식이 없다.
                    continue

        return True

    # 블럭의 모든 자식이 textnode 이거나 virtual text node이면 나누지 않는다.
    def rule4(self, block):
        children = block.getChildren()
        count = 0

        # 블락의 자식들이 textnode 이거나 virtual text node인지 확인
        for childblock in children:
            if self.istextNode(childblock) or self.isVirtualTextNode(childblock):
                count = count + 1
            else:
                break

        if count == len(children):
            return False
        else:
            return True

    # 자식 노드 중 block 노드가 존재하면 나눈다.
    def rule5(self, block):
        for childblock in block.getChildren():
            if childblock.isblock():
                return True

        return False

    # 자식 노드 중 hr 태그를 자신 자식이 존재하면 나눈다.
    def rule6(self, block):
        children = block.getChildren()

        for child in children:
            if child.Pobj.name == "hr":
                return True

        return False

    # 해당 블럭의 배경색이 자식의 배경색과 다르면 나눈다.
    def rule7(self, block):
        check_differ = False

        for childblock in block.getChildren():
            if not (block.getBGcolor() == childblock.getBGcolor()):
                check_differ = True
                break

        if check_differ:
            return True
        else:
            return False


    # 자식들 중 하나라도 textnode 이거나 virtual node 이면서
    # 해당 블럭의 size가 threshhold 값보다 작으면 더 이상 나누지 않는다.
    def rule8(self, block):
        children = block.getChildren()
        check = False

        for childblock in children:
            if self.istextNode(childblock) or self.isVirtualTextNode(childblock):
                check = True
                break

        if check:
            width = block.getWidth()
            height = block.getHeight()
            size = width * height

            if size < self.threshhold:
                return False

        return True

    # 자식 노드들 중 크기가 가장 큰 노드의 값이 threshhold 값보다 작으면 더 이상 나누지 않는다.
    def rule9(self, block):
        max_size = 0

        for childblock in block.getChildren():
            width = childblock.getWidth()
            height = childblock.getHeight()

            child_size = width * height
            if max_size < child_size:
                max_size = child_size

        if max_size < self.threshhold:
            return False

        return True

    # 해당 블럭의 이전 블럭이 나뉘지 않았으면 해당 블럭은 나누지 않는다.
    def rule10(self, block):
        children = block.parent.getChildren()
        index = block.findBlockIndex()

        # 이전 형제 중 나누어진 블락이 있는지 확인
        for i in range(index):
            if children[i].divided:
                return True

        return False

    def rule11(self, block):
        return True

    def rule12(self, block):
        return False

    # 해당 블럭이 웹 페이지 상 시각적으로 보여지는 블럭이면 vaidnode이다.
    def isValidNode(self, block):
        width = block.getWidth()
        height = block.getHeight()

        if block.getVisibility():
            # width와 height가 0보다 크면 시각적으로 보여지기 때문에
            if width > 0 and height > 0:
                return True

            # 부모 블락이 보이지 않아도 자식이 보일 경우가 있어서
            for child in block.Pobj.children:
                if type(child) == bs4.NavigableString:
                    continue
                return True

        return False

    # 해당 블럭의 자식 블럭 중 vailnode가 존재하는지 확인
    def hasValidChildNode(self, block):
        for childblock in block.getChildren():
            if self.isValidNode(childblock):
                return True

        return False

    # 해당 블럭의 상위 태그 바로 아래 text가 포함되어있는 경우 textnode이다.
    def istextNode(self, block):
        for child in block.Pobj.children:
            if type(child) is not bs4.element.NavigableString:
                continue

            new = child.strip()
            if len(new) > 0 and not new.startswith("<!--"):
                return True

        return False

    # textnode는 virtualtextnode 이다.
    # 모든 자식이 virtualtextnode 이거나 textnode 이면 해당 block은 virtualtextnode이다.
    def isVirtualTextNode(self, block):
        children = block.getChildren()
        children_size = len(children)
        count = 0

        # textnode는 virtual text node 이다.
        if children_size == 0:
            return self.istextNode(block)

        # 모든 자식이 textnode 이거나 virtual text node이면
        # 해당 block은 virtual text node이다.
        for childblock in children:
            if self.istextNode(childblock) or self.isVirtualTextNode(childblock):
                count = count + 1
            else:
                break

        if count == children_size:
            return True

        return False
