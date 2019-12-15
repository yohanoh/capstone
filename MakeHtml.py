def write_html(cblock, title):
    start_text = '{% extends "main.html" %}'
    start_text = start_text + "{% block content%}"
    end_text = "{% endblock %}"

    ssrcdoc = '<!DOCTYPE html><html lnag="kr"><head><meta charset="UTF-8"><base href={{baseurl}}><style>body{text-align : center;}</style></head><body>'
    esrcdoc = "</body></html>"

    inter_text = "<h2>" + title + "</h2>"
    for block in cblock.getBlockList():
        inter_text += block.Pobj.prettify()

    srcdoc = ssrcdoc + inter_text + esrcdoc
    result = start_text + "<iframe id='iframe_content' srcdoc=" + "'" + srcdoc + "'>" + "</iframe>" + end_text
    file = open('./template/result.html', 'w', encoding="utf8")
    file.write(result)
    file.close()
