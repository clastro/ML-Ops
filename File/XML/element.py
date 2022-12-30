# XML 파일을 elementTree로 Parsing

import xml.etree.ElementTree as ET

tree = ET.parse('file.xml')
root = tree.getroot() # 가장 상위 태그를 반환해 줌

root.tag #가장 상위 태그 이름
root.attrib #태그 내 속성 값이 있다면 호출
root.text #태그와 태그 사이 Text 값이 있다면 호출

#root는 iter함수를 사용할 수 있고 For loop를 사용하여 하위 태그로 접근이 가능함
[elem.tag for elem in root.iter()] #모든 태그를 불러오기

for movie in root.iter('movie'):
    print(movie.attrib)
    print(movie.tag)
    print(movie.text)
