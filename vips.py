from bs4 import BeautifulSoup
from blockextraction import extraction

# vips 알고리즘을 이용해 웹 페이지를 여러 block 단위로 나눠서 리턴
def service(driver, url):

    # body에 대한 webelement 객체 생성
    dbody = driver.find_element_by_tag_name("body")

    # body에 대한 parser 객체 생성
    html = dbody.get_attribute("outerHTML")
    soup = BeautifulSoup(html, "html.parser")
    pbody = soup.find('body')

    # block 추출 과정을 위한 extraction객체 생성 후 service 메소드 호출
    new_extraction = extraction(pbody, dbody)
    blockList = new_extraction.service()

    return blockList
