#!/usr/bin/python
import urllib2
import re

use_cache = 0

if use_cache == 0:
	content = urllib2.urlopen('http://www.cryptome.org').read()
	f = open ("cryptome.txt", "w")
	f.write(content)
	f.close()
else:
	f = open("cryptome.txt", "r")
	content = f.read()
	f.close()

content = content.split("<PRE>")
content = content[1]

href = re.finditer(r'<B><A HREF="http:\/\/(.*)">(.*)<\/A>[^\)](.*)<\/B>', str(content))
count = 0
rss = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<rss version=\"2.0\">\n<channel>\n<title>RSS Feed Cryptome Latest</title><link>http://www.cryptome.org</link><description>Latest top 10 news items on Cryptome</description>"

for i in href:
	count +=1 
	if count <= 10:
		url = i.group(1)
		doc = i.group(1)
		doc = doc.split('/')
		doc = doc[-1]
		texts = i.group(3)
		text = re.sub(r' ( +)', " ", texts) 
		text = re.sub(r'\(<A(.*)>(.*)<\/A>\)', "", text, re.I) 
		date = re.search(r'([a-zA-Z]+) [0-9]{1,2}\, [0-9]{4}', texts, re.I)
		text = text.replace(" "+date.group(), "")		
		
		#text = text.replace("</A>", "")
		#print "#"+str(count)+"\n"
		#print "Description : "+text+"\n"
		#print "Date : "+date.group()+"\n"
		#print "URL : "+url+"\n"
		#print "Doc : "+doc+"\n"
		#	
		rss += "\n<item>\n<title># : "+str(count)+"</title>\n<pubDate>"+date.group().replace(',','')+"</pubDate>\n<description>"+text+"\nDoc : "+doc+"</description>\n<link>http://"+url+"</link>\n</item>\n"
		 
	else:
		break
rssnews = rss + "\n</channel>\n</rss>\n"
f = open("cryptnews.xml", "w")
f.write(rssnews)
f.close()
