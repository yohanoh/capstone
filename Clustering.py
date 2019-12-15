from Cblock import Cblock
import bs4

"""
추출된 blockLIst를 받아서
1) 태그의 구조가 유사하고
2) 두 블럭이 인접할 경우
해당 블럭들을 같은 리스트에 넣어주는 작업을 수행한다.
"""
def start(blockList, similar_limit, neighbor_limit):
    bound = len(blockList)
    clusterList = []

    for i in range(0, bound-1):
        for j in range(i+1, bound):
            # 구조적 유사성 확인
            check1 = isSimilar(blockList[i], blockList[j], similar_limit)

            # 인접성 확인
            check2 = isNeighbor(blockList[i], blockList[j], neighbor_limit)

            iindex = isInList(clusterList, blockList[i])  # 블럭 i가 속한 군집단이 있는지 확인
            jindex = isInList(clusterList, blockList[j])  # 블럭 j가 속한 군집단이 있는지 확인

            if check1 and check2:
                # 두 block이 모두 속하는 block 리스트가 없는 경우
                if iindex == -1 and jindex == -1:
                    tempList = []
                    tempList.append(blockList[i])
                    tempList.append(blockList[j])
                    clusterList.append(tempList)

                # 두 block이 이미 같은 block 리스트에 포함된 경우
                elif iindex == jindex:
                    continue

                # 두 block이 서로 다른 block 리스트에 포함된 경우
                elif not (iindex == -1) and not (jindex == -1):
                    merge(clusterList, iindex, jindex)

                # block i가 속한 block리스트가 없는 경우, block j가 속한 block리스트에 포함시킨다.
                elif iindex == -1:
                    clusterList[jindex].append(blockList[i])

                # block j가 속한 block리스트가 없는 경우, block i가 속한 block리스트에 포함시킨다.
                elif jindex == -1:
                    clusterList[iindex].append(blockList[j])

            else:
                # 두 block이 속한 block 리스트가 없는 경우
                if iindex == -1 and jindex == -1:
                    tempList = []
                    tempList.append(blockList[i])
                    clusterList.append(tempList)

                    tempList = []
                    tempList.append(blockList[j])
                    clusterList.append(tempList)

                # block i가 속하는 block 리스트가 없는 경우, 새로 만들어준다.
                elif iindex == -1:
                    tempList = []
                    tempList.append(blockList[i])
                    clusterList.append(tempList)

                # block j가 속하는 block 리스트가 없는 경우, 새로 만들어준다.
                elif jindex == -1:
                    tempList = []
                    tempList.append(blockList[j])
                    clusterList.append(tempList)

    return clustering(clusterList)

# 블럭이 속한 군집단이 있는지 확인
# 있으면 해당 index를 리턴, 없으면 -1 리턴
def isInList(clusterList, block):
    bound = len(clusterList)
    if bound == 0:
        return -1

    for i in range(bound):
        for check_block in clusterList[i]:
            if block.id == check_block.id:
                return i
    return -1

# 구조적으로 유사하고 인접한 블럭들이 서로 다른 리스트에 포함되어있는 경우
# 해당 블럭들의 리스트를 갱신한다.(하나로 합쳐준다.)
def merge(clusterList, iindex, jindex):
    len1 = len(clusterList[iindex])
    len2 = len(clusterList[jindex])

    if len2 <= len1:
        for i in range(len2):
            temp = clusterList[jindex][i]
            clusterList[iindex].append(temp)
        del clusterList[jindex]
    else:
        for i in range(len1):
            temp = clusterList[iindex][i]
            clusterList[jindex].append(temp)
        del clusterList[iindex]

# 블럭에 해당하는 html 구조에서 속성 값 및 텍스트 제거
# 구조적 영향을 주지 않는 br 태그는 제거
def remove_attr(Pobj):
    tagList = []
    tag = Pobj.name

    if not(tag == "br") and not(tag == "script"):
        tagList.append(tag)

    #블락의 자식 태그를 확인 후 tagList에 저장한다.
    children = Pobj.children
    for child in children:
        if type(child) is not bs4.element.Tag:
            continue

        child_tag_list = remove_attr(child)
        for child_tag in child_tag_list:
            tagList.append(child_tag)

    if not(tag == "br") and not(tag == "script"):
        tag = "/" + tag
        tagList.append(tag)

    return tagList

#주어진 세 수 중 최소값 구하기
def cal_min(num1, num2, num3):
    if num1 < num2:
        min = num1
    else:
        min = num2

    if min < num3:
        return min
    else:
        return num3

""" 
String Edit Distance algorithm(문자열 편집 거리 알고리즘)을 이용해
두 블럭이 가지는 태그의 구조적 유사성 확인
문자열 편집 거리 알고리즘 : 두 문자열이 몇 번의 수정, 삭제를 통해 같아질 수 있는지를 구하는 알고리즘
 """
def SED(html1, html2):
    rows = len(html1)
    cols = len(html2)

    # rows+1, cols+1 만큼의 index를 갖는 2차원 행렬 초기화
    matrix = [[0 for j in range(cols+1)] for i in range(rows+1)]

    # col index가 0인 행렬 값은 row index에 맞게 초기화
    for row in range(1, rows+1):
        matrix[row][0] = row

    # row index가 0인 행렬 값은 col index에 맞게 초기화
    for col in range(1, cols+1):
        matrix[0][col] = col

    # 2차원 행렬 값을 SED 알고리즘을 통해 구한다.
    for row in range(1, rows+1):
        for col in range(1, cols+1):
            p_value = 1
            if html1[row-1] == html2[col-1]:
                p_value = 0

            case1 = matrix[row-1][col-1] + p_value
            case2 = matrix[row-1][col] + 1
            case3 = matrix[row][col-1] + 1

            matrix[row][col] = min(case1, case2, case3)

    return matrix[rows][cols]

def isSimilar(block1, block2, similar_limit):
    html1 = remove_attr(block1.Pobj)
    html2 = remove_attr(block2.Pobj)

    if SED(html1, html2) <= similar_limit:
        return True
    else:
        return False

def checkPos(b1_pos1, b1_pos2, b2_pos1, b2_pos2, limit):
    tmp1 = b1_pos2 - b2_pos1
    tmp2 = b1_pos1 - b2_pos2

    if abs(tmp1) < limit:
        return True

    elif abs(tmp2) < limit:
        return True

    #b2 안에 b1이 포함되는 경우
    elif b1_pos1 <= b2_pos1 and b1_pos2 >= b2_pos2:
        return True

    #b1 안에 b2가 포함되는 경우
    elif b2_pos1 <= b1_pos1 and b2_pos2 >= b1_pos2:
        return True

    # b1와 b2의 일부가 겹쳐지는 경우
    elif b1_pos1 < b2_pos1 and b1_pos1 > b2_pos2:
        return True

    # b1와 b2의 일부가 겹쳐지는 경우
    elif b2_pos1 < b1_pos1 and b2_pos1 > b1_pos2:
        return True

    #두 블럭이 이웃하지 않는다.
    else:
        return False

def isNeighbor(block1, block2, limit_distance) :
    # 두 블록의 수직적인 관계 확인하기
    block1_top = block1.getY()
    block1_bottom = block1_top + block1.getHeight()

    block2_top = block2.getY()
    block2_bottom = block2_top + block2.getHeight()

    vertical = checkPos(block1_top, block1_bottom, block2_top, block2_bottom, limit_distance)

    if not vertical:
        return False

    # 두 블록의 수평적인 관계 파악하기
    block1_left = block1.getX()
    block1_right = block1_left + block1.getWidth()

    block2_left = block2.getX()
    block2_right = block2_left + block2.getWidth()

    horizon = checkPos(block1_right, block1_left, block2_right, block2_left, limit_distance)

    if not horizon:
        return False
    else:
        return True

# 생성된 군집단 리스트 별로 cblock 객체를 생성해서
# 생성된 cblock를 리스트에 넣어 최종적으로 생성된 리스트를 반환하는 함수
def clustering (clusterList):
    cblockList = []

    """
     군집단에 속하는 모든 블럭의 x, y 값을 비교해서
     가장 왼쪽 상위에 위치한 값을 min_x, min_y로 지정한다.
     그리고 x+width, y+height 값을 비교해서
     가장 오른쪽 하위에 위치한 값을 max_x, max_y로 지정한다.
     cwidth = max_x - min_x cheight=max_y-min_y
     이와 같이 얻은 cwidth, cheight, min_x, min_y 그리고 해당 군집단에 속하는 리스트인 blockLIst를 
     cblock의 속성 값으로 지정한다.
    """
    for blocklist in clusterList:
        if len(blocklist) > 1:
            max_x = 0
            max_y = 0
            min_x = 10000
            min_y = 10000

            for block in blocklist:
                x = block.getX()
                y = block.getY()
                width = block.getWidth()
                height = block.getHeight()

                if min_x > x:
                    min_x = x

                if min_y > y:
                    min_y = y

                if max_x < x+width:
                    max_x = x+width

                if max_y < y+height:
                    max_y = y+height

            cwidth = max_x - min_x
            cheight = max_y - min_y

            cblock = Cblock(cwidth, cheight, min_x, min_y, blocklist)
            cblockList.append(cblock)

        else:
            width = blocklist[0].getWidth()
            height = blocklist[0].getHeight()
            x = blocklist[0].getX()
            y = blocklist[0].getY()

            cblock = Cblock(width, height, x, y, blocklist)
            cblockList.append(cblock)

    return cblockList
