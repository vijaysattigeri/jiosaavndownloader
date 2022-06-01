from encodings import utf_8
import re

my_pattern =re.compile(r'https://www.jiosaavn.com/song/[%a-zA-Z0-9,.+_-]*/[%a-zA-Z0-9,.+_-]*')

#read file

fh = open("a.html", encoding="utf_8")
cont = fh.read()
urls = my_pattern.findall(cont)


out_f = open("URLs.txt", 'w')
for u in urls:
    out_f.write(u + "\n")

out_f.close()
print(len(urls))
