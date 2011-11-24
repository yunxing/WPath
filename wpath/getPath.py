import shelve
import simplejson
import xml.dom.minidom  
import urllib2
import urllib
import fixurl
import HTMLParser
import re

lPart = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22en.wikipedia.org%2Fwiki%2F'

rPart = "%22%20and%20xpath%3D'%2F%2Fa%5Bstarts-with(%40href%2C%20%22%2Fwiki%22)%20and%20not(contains(%40href%2C%20%22%3A%22))%20and%20not(contains(%40href%2C%20%22Main_Page%22))%20and%20not(contains(%40href%2C%20%22List_%22))%5D'&format=json&diagnostics=true&callback="

queryAPIURL = u"http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles="

htmlURL = "http://en.wikipedia.org/w/index.php?action=render&title="

nameURL = "http://en.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=xml&search="


class Node:
    content = ""
    parent = 0

    
    
def getRealName(name):
    name = name.replace(" ", "%20")
    result = ""
    print nameURL + name
    doc = xml.dom.minidom.parseString(urllib2.urlopen(nameURL + name).read())
    l = doc.getElementsByTagName("Url")
    
    if len(l) == 0:
        raise Exception("name no found")
    result = l[0].toxml()
    result = result.split(r"</")[0:-1][0]
    result = result.split(r"/")[-1]    
    return str(result)

def getLinks(name):
    print "searching for : " + name
    doc = xml.dom.minidom.parseString(urllib2.urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles=" + name).read())
    xmlRow= doc.getElementsByTagName("rev")
    result = xmlRow[0].toxml()

    result = result.split(r">")[1]
    result = result.split(r"<")[0]
    result = HTMLParser.HTMLParser().unescape(result)
    result = re.compile("\<\!\-\-.*?\-\-\>", re.M|re.S).sub(r"", result)
    result = re.compile(r"^\{\{Infobox.*?^\}\}\s*$", re.M|re.S).sub(r"", result)
    result = re.compile(r"^\s*\|.*?\[\[.*\]\].*$", re.M).sub("", result)
    result = result.split(r"==")[0]
    
    # result = result.split(r"}}")[-1]
    links  = re.compile(r"\[\[.*?\]\]", re.U).findall(result)
    links=filter(lambda x: x.find(r":") == -1, links)
    links=filter(lambda x: x.find(r"#") == -1, links)    
    links=map(lambda x: x[2:-2], links)
    links=map(lambda x: x.split(r"|")[0], links)
    links=map(lambda x: x.replace(r" ", r"_"), links)
    links=map(lambda x: x.replace(u"\u2013", r"-"), links)
    links=map(lambda x: x.replace(u"\u2014", r"'"), links)
    links=map(lambda x: x.replace(u"\u2019", r"'"), links)    
    links=map(lambda x: x.replace(u"\u200e", r""), links)
    links=map(lambda x: x.replace(u"\u0101", r""), links)    
#     links=map(lambda x: x.replace(u"\xe1", r"a"), links)
#     links=map(lambda x: x.replace(u"\xe4", r"a"), links)
#     links=map(lambda x: x.replace(u"\xe6", r"a"), links)
#     links=map(lambda x: x.replace(u"\xe7", r"c"), links)
#     links=map(lambda x: x.replace(u"\xe8", r"e"), links)    
#     links=map(lambda x: x.replace(u"\xe9", r"e"), links)
#     links=map(lambda x: x.replace(u"\xed", r"i"), links)
#     links=map(lambda x: x.replace(u"\xd8", r"o"), links)    
#     links=map(lambda x: x.replace(u"\xfc", r"u"), links)    

    print links
    return links
    
def getPath(start, end):
    start = getRealName(start)
    end = getRealName(end)
    print "invoked by " + start + " " + end    
    queue = []
    startObj = Node()
    startObj.content = start
    startObj.parent = -1
    queue.append(startObj)
    h = {}
    i = 0
    find = False
    # do bfs
    while True:
        try:
            obj = queue[i]
        except IndexError:
            return []
        print "====iteration====" + str(i)
        links = getLinks(obj.content)
        h[obj.content] = True
        for link in links:
            try:
                neighbor = Node()
                neighbor.content = link
                neighbor.content = fixurl.url_fix(unicode(neighbor.content))
                if neighbor.content.lower() == unicode(end).lower():
                    queue.append(neighbor)
                    queue[len(queue) - 1].parent = i
                    find = True
                    break
            except Exception, inst:
                continue
            neighbor.parent = i
            if h.has_key(neighbor.content):
                continue
            queue.append(neighbor)
        if find:
            break            
        i = i + 1

    p = queue[-1]
    r = []
    while p.parent != -1:
        r.append(p)
        p = queue[p.parent]

    r.append(startObj)
    for node in r:
        print node.content
        
if __name__ == '__main__':
    print getPath(getRealName("Baltic_Sea"), getRealName("ice cream"))
    #getLinks(getRealName("South_pole"))
