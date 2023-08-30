import urllib
import urllib.request as req
import re
import os
import csv

url1 = 'https://sdmda.bupt.edu.cn/szdw/js.htm'
url2 = 'https://sdmda.bupt.edu.cn/szdw/fjs.htm'
url3 = 'https://sdmda.bupt.edu.cn/szdw/js1.htm'

response1 = req.urlopen(url1)
url1_content = response1.read().decode('utf-8')
url2_content = response1.read().decode('utf-8')
url3_content = response1.read().decode('utf-8')
chinese_characters = re.findall(r'[\u4e00-\u9fff]', url1_content)
num_chinese_characters = len(chinese_characters)

text_data1 = re.sub('<[^<]+?>', '', url1_content)
text_data2 = re.sub('<[^<]+?>', '', url2_content)
text_data3 = re.sub('<[^<]+?>', '', url3_content)

pattern = r'[^\u4e00-\u9fff]*([\u4e00-\u9fff]+)[^\u4e00-\u9fff]·*'
pattern2 = r'.*?<div class="name-group">.*?<span class="name">(?P<name> .*?)</span>'
matched_groups = re.findall(pattern, url1_content)
matched_groups2 = re.findall(pattern2, url1_content)
# print(url1_content)
# print(matched_groups)
#
# for group in matched_groups2:
#     print()


# 先写一个带表头的csv
teacherHeader = ["Department", "Name", "Title", "Photo"]
with open("teacher.csv", "a") as file:
    writer = csv.DictWriter(file, fieldnames=teacherHeader)
    writer.writeheader()
    file.close()

professionUrlObj = re.compile(r'<a class="people.*?href="(?P<professionUrl>.*?)">(?P<profession>.*?)</a>', re.S)
professionUrlResult = professionUrlObj.finditer(url1_content)

# 老师职业列表
professionUrl = []
for i in professionUrlResult:
    url = "https://sdmda.bupt.edu.cn/szdw/" + i.group("professionUrl")
    professionUrl.append([url, i.group("profession")])

for i in range(3):
    response = req.urlopen(professionUrl[i][0])
    url_content = response.read().decode('utf-8')

    obj = re.compile(
        r'<div class="name-group">.*?<span class="name">(?P<name>.*?)</span>.*?<span class="iden">(?P<xi>.*?)</span>',
        re.S)
    result = obj.finditer(url_content)

    # 姓名列表
    name = []
    # 专业列表
    major = []
    for it in result:
        name.append(it.group("name"))

        major.append(it.group("xi"))

    # 提取图片链接
    objImage = re.compile(r'<div class="col-md-1-5 col-sm-1-5  col-xs-6">.*?<img src="(?P<img>.*?)" alt="">', re.S)
    image_urls = objImage.finditer(url_content)

    # 创建一个目录来保存图片
    if not os.path.exists('images'):
        os.mkdir('images')
    if not os.path.exists(professionUrl[i][1]):
        os.mkdir('images/' + professionUrl[i][1])

    # 下载并保存图片
    n = 0
    for img_url in image_urls:
        img = "https://sdmda.bupt.edu.cn/" + img_url.group("img")

        img_name = name[n] + ".jpg"  # 提取图片名
        n += 1

        img_path = os.path.join('images/' + professionUrl[i][1], img_name)

        #
        # # 发起图片请求并保存
        img_response = urllib.request.urlopen(img)
        with open(img_path, 'wb') as img_file:
            img_file.write(img_response.read())
            img_file.close()

    csvList = []

    for j in range(len(name)):
        Dir = {"Department": major[j], "Name": name[j], "Title": professionUrl[i][1],
               "Photo": "images/" + professionUrl[i][1] + "/" + name[j] + ".jpg"}
        csvList.append(Dir)

    with open("teacher.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=teacherHeader)
        writer.writerows(csvList)
        file.close()
