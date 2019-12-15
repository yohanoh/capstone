from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from vips import service
from Ranking import importance
from bs4 import BeautifulSoup
from bodyinframe import check_bodyInFrame, rule_bodyInFrame
from iframe import check_iframe, rule_iframe
from AHclustering import AHclustering
from MakeHtml import write_html

def start(url, limit):
    try:
        print("===========================================================================")
        print("url : ", url)
        options = Options()
        options.add_argument('headless')
        driver = webdriver.Chrome('./chromedriver.exe', options=options)
        driver.implicitly_wait(3)
        driver.get(url)

        """
        1) body 태그의 자식 태그 중 iframe이 있는 경우
        -> rule_iframe를 통해 새로운 driver 객체를 생성한다.
        2) frame set 안에 있는 frame 안에 body가 있는 경우
        -> rule_bodyInFrame를 통해 새로운 driver 객체를 생성한다.
        3) 그 외 경우
        -> 기존에 driver 객체를 그대로 사용한다.
        """
        # body_in_frame 과 iframe 을 체크하기 위한 parser 객체 생성
        html = driver.page_source
        parser = BeautifulSoup(html, "html.parser")

        if check_iframe(parser):  # iframe in body 인지를 체크
            driver = rule_iframe(driver)
        else:
            # body in frame 인지를 확인
            if check_bodyInFrame(parser):
                driver = rule_bodyInFrame(driver)

        # title 추출
        title = parser.title.string

        # vips 알고리즘을 통해 block 추출 과정 수행
        print("block 추출 중......")
        blockList = service(driver, url)
        print("block 추출 완료!!")

        # 군집화 과정 수행
        print("군집화 진행 중 .....")
        cblockList = AHclustering(blockList, limit)


        print("군집화 완료!!")
        print("중요도 판별 중!!!")
        big_cblock = importance(cblockList)
        list = []
        list.append(big_cblock)
        write_html(big_cblock, title)
        print("중요도 판별 완료!!")
        print("===========================================================================")

    finally:
        driver.quit()
