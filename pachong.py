import urllib
import urllib.request as req
import re
import os
import csv

url = 'https://sdmda.bupt.edu.cn/szdw/js.htm'
response = req.urlopen(url)
url_content = response.read().decode('utf-8')

professionUrlObj = re.compile(r'<a class="people.*?href="(?P<professionUrl>.*?)">(?P<profession>.*?)</a>', re.S)
professionUrlResult = professionUrlObj.finditer(url_content)

professionUrl = []
for i in professionUrlResult:
    url = "https://sdmda.bupt.edu.cn/szdw/" + i.group("professionUrl")
    professionUrl.append([url, i.group("profession")])

teacherHeader = ["Department", "Name", "Title", "Photo"]
with open("teacher.csv", "a") as file:
    writer = csv.DictWriter(file, fieldnames=teacherHeader)
    writer.writeheader()
    file.close()

for i in range(3):
    response = req.urlopen(professionUrl[i][0])
    url_content = response.read().decode('utf-8')

    obj = re.compile(
        r'<div class="name-group">.*?<span class="name">(?P<name>.*?)</span>.*?<span class="iden">(?P<xi>.*?)</span>',
        re.S)
    result = obj.finditer(url_content)

    name = []
    major = []

    for it in result:
        name.append(it.group("name"))

        major.append(it.group("xi"))

    objImage = re.compile(r'<div class="col-md-1-5 col-sm-1-5  col-xs-6">.*?<img src="(?P<img>.*?)" alt="">', re.S)
    image_urls = objImage.finditer(url_content)

    if not os.path.exists('images'):
        os.mkdir('images')
    if not os.path.exists(professionUrl[i][1]):
        os.mkdir('images/' + professionUrl[i][1])

    n = 0
    for img_url in image_urls:
        img = "https://sdmda.bupt.edu.cn/" + img_url.group("img")

        img_name = name[n] + ".jpg"
        n += 1

        img_path = os.path.join('images/' + professionUrl[i][1], img_name)

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
