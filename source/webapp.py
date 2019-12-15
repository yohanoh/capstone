from main import start
from flask import Flask, render_template, redirect, request, url_for
import re

"""
* 여기가 메인입니다. 여기서 돌려주세요.*

* 동작 설명 *
webapp.py를 실행하면 command 창에 http://127.0.0.1:5000/ url을 통해 web이 동작하게 됨
해당 url을 들어가면 웹 데이터 수집기 창이 뜬다.
수집하고자 하는 url, 임계값 을 넣어준 후, 입력을 클릭하면 수집 과정을 수행한다.
만약 이 과정에서 driver 에러가 발생하면 크롬 드라이버 버전에 문제가 있는 것이므로 적절한 driver를 다운 받아 재실행한다.
수집이 완료되면 동일한 웹 페이지에서 결과를 확인 가능하다.

* TO-DO *
 1. 콘텐츠를 군집화하는 과정에서 오직 거리 지표를 통해 수행하기 때문에 모든 페이지가 잘 수집되는 것은 아니다.(난잡한
 웹 페이지의 경우, 잘 수집되지 않을 수 있다.)
 
 2. 거리 지표는 콘텐츠 간의 중심 거리 vs 콘텐츠 간 이웃 거리 둘 가지 옵션 중 중심 거리를 선정했는데 이미지 같이 중심거리
 가 크게 벌어질 경우 후자에 경우가 나을 수 있다. 해당 팀에서는 비지도 학습의 일부인 AHClustering을 통한 빠르고 직관적인
 장점 때문에 중심 거리를 선택했다.  

"""
app = Flask(__name__, template_folder='./template/')


@app.route('/')


def inputTest():
    return render_template('main.html')


@app.route('/result')
@app.route('/result/<path:baseurl>')
def result(baseurl=None):
    return render_template('result.html', baseurl=baseurl)


@app.route('/calculate', methods=['POST'])
def calculate():
    if request.method == 'POST':
        url = request.form['url']
        limit = request.form['limit']
        limit = int(limit)
        start(url, limit)
        base = baseurlfind(url)
    else:
        url = None
        base = None

    return redirect(url_for('result', baseurl=base))


def baseurlfind(url):
    reg_baseParse_patter = re.compile("^https?:\/\/[^\/]+")
    baseurl = reg_baseParse_patter.search(url)
    if baseurl:
        return baseurl.group(0)
    else:
        return False


if __name__ == "__main__":
    app.run(debug=True)

