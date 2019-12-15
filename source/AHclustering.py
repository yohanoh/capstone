import numpy as np
from sklearn.cluster import AgglomerativeClustering

from Cblock import Cblock

# AH(Agglomerative Hierarchical)clustering를 정의하는 함수
def AHclustering(blocklist, limit):
    block_loc_list = []

    # 각 블락의 중심 좌표 값을 리스트에 저장한다.
    for block in blocklist:
        block_loc_list.append(block.getCenter())

    # 클러스터링을 위한 사전 데이터셋을 만든다.
    locations = np.array(block_loc_list)

    # AH clustering 를 적용하기 위한 cluster 객체를 생성해준다.
    # 거리 측정은 eucildean 방식을, 클러스터 간 거리측정은 single 방식을, 마지막으로 거리의 임계값을 사용자 input으로 설정
    cluster = AgglomerativeClustering(n_clusters=None, affinity='euclidean', linkage='single', distance_threshold=limit)

    # 생성한 cluster 객체와 위에서 생성한 데이터셋을 결합하여 clustering을 진행한다.
    cluster.fit_predict(locations)

    # 클러스터링이 완료되면 각 블락은 해당하는 집단을 나타내는 label이 할당된다.
    # block_labels은 블락들의 label을 저장하고 있는 리스트이다.
    block_labels = cluster.labels_

    # cluster_list는 같은 집단에 속하는 블락들을 묶어주는 위한 이중 리스트이다.
    cluster_list = [[] for i in range(cluster.n_clusters_)]

    # 모든 블락에 대해 label 값을 확인해서 같은 label을 갖는 블락끼리 같은 리스트에 넣어준다.
    for block_index in range(len(blocklist)):
        label = block_labels[block_index]
        cluster_list[label].append(blocklist[block_index])

    return make_cblock(cluster_list)

# 각 군집단의 속성을 나타내는 cblock객체를 생성하고 이렇나 cblock 리스트를 리턴해준다.
def make_cblock(clusterList):
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

                if max_x < x + width:
                    max_x = x + width

                if max_y < y + height:
                    max_y = y + height

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
