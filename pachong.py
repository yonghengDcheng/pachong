import urllib.request as req

url1 = 'https://sdmda.bupt.edu.cn/szdw/js.htm'
url2 = 'https://sdmda.bupt.edu.cn/szdw/fjs.htm'
url3 = 'https://sdmda.bupt.edu.cn/szdw/js1.htm'


response1 = req.urlopen(url1)
url1_content = response1.read().decode('utf-8')

print(url1_content)

