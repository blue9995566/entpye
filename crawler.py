import requests
from bs4 import BeautifulSoup
import random
import time

words=[]
res=requests.get("http://dictionary.cambridge.org/dictionary/english/a")
soup=BeautifulSoup(res.text)
try:
	for x in range(3000):
		
		i=0
		for item in soup.select('.query'):
			i+=1
			#print item.text
			#print item['title']
			#print item['href']
			if item['title'] not in words:
				words.append(item['title'].lower().encode('utf8'))
		if x%100==0:
			print x
			time.sleep(1)
		#if len(words)>=7000:
			#break
		#print i
		if i==0:
			res=requests.get("http://dictionary.cambridge.org/dictionary/english/a")
		elif i==1:
			res=requests.get(soup.select('.query')[0]['href'])
		else:
			res=requests.get(soup.select('.query')[random.randint(0,i-1)]['href'])
		soup=BeautifulSoup(res.text)
except Exception:
	pass

#print soup.select('.query')
#print soup.select('.query')[10]['href']
#res=requests.get(soup.select('.query')[10]['href'])
#soup=BeautifulSoup(res.text)

#print words
print len(words)

write_file=open("save.txt",'w')
for word in words[:-1]:
	write_file.write(word+',')
write_file.write(words[-1])
write_file.close()
