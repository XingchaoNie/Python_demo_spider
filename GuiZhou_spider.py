import requests
from bs4 import BeautifulSoup
import re
import json


def get_html(url):
    try:
        header_reset = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout=30, headers=header_reset)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        source = r.text
    except:
        source = "访问失败"
    return source


def set_new_json(file_name, source, url):
    dict_json = dict()
    # 存入URL
    dict_json["URL"] = url
    soup_source = BeautifulSoup(source, "html.parser")
    data_1_point = soup_source.body.find_all("table")[0].find_all("tr")
    # 存入index
    try:
        dict_json["index"] = data_1_point[0].find_all("span")[0].string
    except:
        dict_json["index"] = "未查询到"
    # 存入infotype
    try:
        pro = data_1_point[0].find_all("span")[1].string
        dict_json["infotype"] = re.findall(r"xxfl='.+'", pro)[0][6:-1]
    except:
        dict_json["infotype"] = "未查询到"
    # 存入dept
    try:
        pro = data_1_point[1].find_all("span")[0].string
        if len(re.findall(r'''var str.+"''', pro)[0][11:-1]) != 0:
            dict_json["dept"] = re.findall(r'''var str.+"''', pro)[0][11:-1]
        else:
            dict_json["dept"] = re.findall(r'''var str_1.+"''', pro)[0][13:-1]
    except:
        dict_json["dept"] = "未查询到"
    # 存入makedate
    try:
        dict_json["makedate"] = data_1_point[1].find_all("span")[1].string
    except:
        dict_json["makedate"] = "未查询到"
    # 存入document_num
    try:
        dict_json["document_num"] = data_1_point[2].find_all("span")[0].string
    except :
        dict_json["document_num"] = "未查询到"
    # 存入valid_flag
    try:
        pro = data_1_point[2].find_all("span")[1].string
        sig = re.findall(r"var isok.*'", pro)[10:-1]
        if not len(sig):
            dict_json["valid_flag"] = "是"
        else:
            if sig[0] != "否":
                dict_json["valid_flag"] = "是"
            else:
                dict_json["valid_flag"] = "否"
    except:
        dict_json["valid_flag"] = "未查询到"
    # 存入title
    try:
        dict_json["title"] = data_1_point[3].find_all("span")[0].string
    except:
        dict_json["title"] = "未查询到"
    # 存入sorce
    try:
        data_1_point = soup_source.body.find_all("div", attrs={"class": "article Box MT15"})
        pro = data_1_point[0].find_all("span")[1].string
        dict_json["source"] = re.findall(r"wzly='.+'", pro)[0][6:-1]
    except:
        dict_json["source"] = "未查询到"
    # 存入policy_content
    try:
        data_1_point = soup_source.body.find_all("font", attrs={"id": "Zoom"})[0]
        data_1_point = data_1_point.find_all(["p", "span"])
        dict_json["policy_content"] = ""
        for point in data_1_point:
            if point.string:
                dict_json["policy_content"] = dict_json["policy_content"] + str(point.string)
    except:
        dict_json["policy_content"] = "网页无正文"
    # 存入attachname与attachur1
    try:
        data_1_point = soup_source.body.find_all("font", attrs={"id": "Zoom"})[0]
        data_1_point = data_1_point.find_all("a")
        dict_json["attachname"] = list()
        dict_json["attachur"] = list()
        for point in data_1_point:
            dict_json["attachname"].append(point.attrs["title"])
            dict_json["attachur"].append(re.findall(".+zc.+wj", url)[0] + point.attrs["href"][1:])
    except:
        dict_json["attachname"] = "无"
        dict_json["attachur"] = "无"
    with open(file_name, 'w+') as fp_json:
        json.dump(dict_json, fp_json)
    fp_json.close()


def main():
    root_url = r"http://gxt.guizhou.gov.cn/zwgk/xxgkml/zcwj/qtwj/"
    son_url = "index"
    grandson_url = ".html"
    json_root = r"E:/IRdata/"
    num_url = list([""])
    for i in range(8):
        num_url.append("_"+str(i + 1))
    for i in range(9):
        page_source = get_html(root_url+son_url+num_url[i]+grandson_url)
        if page_source != "访问失败":
            print("第{:d}个目录页面获取成功".format(i+1))
            page_source_soup = BeautifulSoup(page_source, "html.parser")
            page_point_soup = page_source_soup.find("div", attrs={"class": "rightCon aBox f_r"})
            j = 0
            for url_soup in page_point_soup.find_all("a"):
                url = url_soup.attrs["href"]
                try:
                    source = get_html(str(url))
                    set_new_json(json_root+str(i+1)+"_"+str(j+1)+".json", source, str(url))
                except:
                    with open(json_root+str(i+1)+"_"+str(j+1)+"错误文件.json", 'w+') as fp_json:
                        json.dump({"错误链接": "http://gxt.guizhou.gov.cn"+str(url)}, fp_json)
                    fp_json.close()
                j = j+1
        else:
            print("第{:d}个目录页面获取失败".format(i+1))


if __name__ == "__main__":
    main()
