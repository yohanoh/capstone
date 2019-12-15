import bs4

def check_bodyInFrame(parser):
    soup = parser.find("head")

    # head의 next_sibling 중 bs4.element.Tag 타입의 객체를 가져온다.
    while(True):
        soup = soup.next_sibling
        if type(soup) == bs4.element.Tag:
            break

    #head 의 next_sibling이 frameset인 경우
    if soup.name == "frameset":
        return True
    else:
        return False

#html 를 포함하고 있는 여러 frame 중 "main" 키워드를 name으로 가진 frame를 선택해서
#해당 html 문서로 driver를 switch해주는 작업
def rule_bodyInFrame(driver):
    frames = driver.find_elements_by_tag_name("frame")
    if len(frames) >= 1:
        for frame in frames:
            name = frame.get_attribute("name")
            if "main" in name.lower():
                driver.switch_to_frame(frame)
                break
    return driver