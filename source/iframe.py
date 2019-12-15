import bs4

def check_iframe(parser):
    soup = parser.find("head")

    # head의 next_sibling 중 bs4.element.Tag 타입의 객체를 가져온다.
    while True:
        soup = soup.next_sibling
        if type(soup) == bs4.element.Tag:
            break

    if soup.name == "body":
        children = soup.children

        for child in children:
            if type(child) == bs4.element.Tag:
                if child.name == "iframe":
                    return True
                else:
                    return False

#iframe이 하나만 있는 경우는?? bodyinframe도 동일
def rule_iframe(driver):
    iframes = driver.find_elements_by_tag_name("iframe")
    if len(iframes) >= 1:
        for iframe in iframes:
            name = iframe.get_attribute("name").lower()
            if 'main' in name:
                driver.switch_to_frame(iframe)
                break

    return driver
