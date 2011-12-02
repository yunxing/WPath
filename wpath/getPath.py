import shelve
import simplejson
import xml.dom.minidom  
import urllib2
import urllib
import fixurl
import HTMLParser
import re
import threading
import time
import socket

queryAPIURL = u"http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles="

htmlURL = "http://en.wikipedia.org/w/index.php?action=render&title="

nameURL = "http://en.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=xml&search="

port = 10241

class Node:
    content = ""
    parent = 0

queueLock = threading.Lock()
hashLock = threading.Lock()
i = 0
finishFlag = False
iLock = threading.Lock()
lastElement = Node()

class NameFinder(threading.Thread):
    def __init__(self, name):
        self.name = name
        threading.Thread.__init__(self)
        
    def run(self):
        name = self.name
        name = name.replace(" ", "%20")
        result = ""
        print nameURL + name
        doc = xml.dom.minidom.parseString(urllib2.urlopen(nameURL + name).read())
        l = doc.getElementsByTagName("Url")
        if len(l) == 0:
            raise Exception("name no found")
        result = l[0].toxml()
        Result = result.split(r"</")[0:-1][0]
        result = result.split(r"/")[-1]    
        name = result        

class worker(threading.Thread):
    def __init__(self, queue, h, end):
        self.queue = queue
        self.h = h
        self.end = end
        self.port = 10241
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        threading.Thread.__init__(self)
        
    def run(self):
        global finishFlag
        global i
        global queueLock
        global hashLock

        queue = self.queue
        h = self.h
        end = self.end
        while(not finishFlag):
            iLock.acquire()
            parent = i
            i += 1
            iLock.release()
            while(parent >= len(queue)):
                if finishFlag:
                    return
                time.sleep(0.1)
            if finishFlag:
                return
            
            print "====iter====" + str(parent)
            obj = queue[parent]
            startTime = time.time()*1000000
            links = getLinks(obj.content, self.s)
            print "time used for " + obj.content + ":" + str(time.time()*1000000 - startTime)
            
            if finishFlag:
                return
            
            for link in links:
                if finishFlag:
                    return
                neighbor = Node()
                neighbor.content = link
                neighbor.content = fixurl.url_fix(unicode(neighbor.content))
                if neighbor.content.lower() == unicode(end).lower():
                    queueLock.acquire()
                    queue.append(neighbor)
                    queue[len(queue) - 1].parent = parent
                    queueLock.release()
                    finishFlag = True
                    print "found!!!"
                    global lastElement
                    lastElement = neighbor
                    return
                neighbor.parent = parent
                hashLock.acquire()

                travelled = h.has_key(neighbor.content.lower())
                hashLock.release()
                if not travelled:
                    h[neighbor.content.lower()] = True

                    queueLock.acquire()
                    queue.append(neighbor)

                    
                    queueLock.release()
                    
                
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
    name = result

    
def getLinks(name, s):
    s.sendto("F"+name, ('localhost', port))
    if s.recvfrom(2048)[0] == 'Y':
        print name
        s.sendto("G"+name, ('localhost', port))
        result = unicode(urllib.unquote(s.recvfrom(2048)[0]).decode("utf-8")).rstrip().split(' ')
        if result == ['']:
            print "no result!"
            return []
        return result
    print "no hits!"
    
    try:
        doc = xml.dom.minidom.parseString(urllib2.urlopen("http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles=" + name).read())
        xmlRow= doc.getElementsByTagName("rev")
        result = xmlRow[0].toxml()
    except Exception,e:
        print e
        newEntry = "A" + name
        s.sendto((newEntry), ('localhost', 10241))
        s.recvfrom(2048)[0]        
        return []
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
    links=filter(lambda x: x.lower().find(r"list_of") == -1, links)
    links=map(lambda x: x.encode("utf-8"), links)
    links=map(lambda x: urllib.quote(x), links)    
    print "searching for : " + name
    newEntry = "A" + name
    for l in links:
        newEntry += " "+l
    s.sendto((newEntry), ('localhost', 10241))
    s.recvfrom(2048)[0]
    return links
    
def getPath(start, end):
    t1 = NameFinder(start)
    t2 = NameFinder(end)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    start = start.replace(r" ", r"_")
    end = end.replace(r" ", r"_")    
    
    print "invoked by " + start + " " + end    
    queue = []
    startObj = Node()
    startObj.content = start
    startObj.parent = -1
    queue.append(startObj)
    h = {}
    find = False

    threads = []
    for t in range(0,100):
        thread = worker(queue, h, end)
        thread.start()
        threads.append(thread)

    global finishFlag
    while not finishFlag:
        time.sleep(1)
    for t in threads:
        t.join()
    
    #finished
    p = lastElement
    r = []
    while p.parent != -1:
        r.append(p)
        p = queue[p.parent]
    print "\n\n***PATH***"
    r.append(startObj)
    for node in r:
        print node.content
    
    return r
        
if __name__ == '__main__':
    getPath("google", "polar_bear")
