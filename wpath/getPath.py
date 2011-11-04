import shelve
import simplejson

import urllib2
import fixurl

lPart = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22en.wikipedia.org%2Fwiki%2F'

rPart = "%22%20and%20xpath%3D'%2F%2Fa%5Bstarts-with(%40href%2C%20%22%2Fwiki%22)%20and%20not(contains(%40href%2C%20%22%3A%22))%20and%20not(contains(%40href%2C%20%22Main_Page%22))%20and%20not(contains(%40href%2C%20%22List_%22))%5D'&format=json&diagnostics=true&callback="

db = shelve.open('links.db')
print len(db)

class Node:
    content = ""
    href = ""
    parent = 0
    
def getNeighbor(name):
    print "getNeighbor invoked:" + name
    if db.has_key(name):
        print "hit"
        return db[name]
    src = lPart + name + rPart
    urlResult = ""
    try:
        urlResult = urllib2.urlopen(src).read()
    except Exception, inst:
        print "wrong src " + src
        print inst
        
    try:
        result = (simplejson.loads(urlResult))['query']['results']['a']
    except Exception, inst:
        db[name] = []
        return []
    db[name] = result
    return result

def getPath(start, end):
    queue = []
    startObj = {}
    startObj["content"] = start
    startObj["href"] = "/wiki/" + start
    startObj["parent"] = -1
    queue.append(startObj)
    h = {}
    i = 0
    # do bfs
    while True:
        try:
            obj = queue[i]
        except IndexError:
            return []
        print "iteration ------" + str(i)
        print "degree: " + str(obj['parent'])
        
        if obj["content"].lower() == unicode(end).lower():
            break
        queryList = getNeighbor(obj["content"])
        h[obj["content"]] = True
        for neighbor in queryList:
            try:
                neighbor["content"] = neighbor["content"].replace(" ", "_")
                neighbor["content"] = fixurl.url_fix(unicode(neighbor["content"]))
            except Exception, inst:
                continue
            if h.has_key(neighbor["content"]):
                continue
            neighbor["parent"] = i
            queue.append(neighbor)
        i = i + 1
    print "---------------------------------------finished "
    p = queue[i]
    while p["parent"] != -1:
        print p["content"]
        print p["href"]
        print p["parent"]
        p = queue[p["parent"]]
        
if __name__ == '__main__':
    print getPath("Icecream", "yahoo")

