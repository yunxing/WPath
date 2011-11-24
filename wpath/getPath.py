import shelve
import simplejson
import xml.dom.minidom  
import urllib2
import urllib
import fixurl

lPart = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22en.wikipedia.org%2Fwiki%2F'

rPart = "%22%20and%20xpath%3D'%2F%2Fa%5Bstarts-with(%40href%2C%20%22%2Fwiki%22)%20and%20not(contains(%40href%2C%20%22%3A%22))%20and%20not(contains(%40href%2C%20%22Main_Page%22))%20and%20not(contains(%40href%2C%20%22List_%22))%5D'&format=json&diagnostics=true&callback="

htmlURL = "http://en.wikipedia.org/w/index.php?action=render&title="

nameURL = "http://en.wikipedia.org/w/api.php?action=opensearch&limit=1&namespace=0&format=xml&search="

db = shelve.open('links.db')
print len(db)


class Node:
    content = ""
    href = ""
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
def getNeighbor(name):
    if db.has_key(name):
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
    start = getRealName(start)
    end = getRealName(end)
    print "invoked by " + start + " " + end    
    queue = []
    startObj = {}
    startObj["content"] = start
    startObj["href"] = "/wiki/" + start
    startObj["parent"] = -1
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
        queryList = getNeighbor(obj["content"])
        h[obj["content"]] = True
        for neighbor in queryList:
            try:
                neighbor["content"] = neighbor["content"].replace(" ", "_")
                neighbor["content"] = fixurl.url_fix(unicode(neighbor["content"]))
                if neighbor["content"].lower() == unicode(end).lower():
                    queue.append(neighbor)
                    queue[len(queue) - 1]['parent'] = i
                    find = True
                    break
            except Exception, inst:
                continue
            neighbor["parent"] = i
            if h.has_key(neighbor["content"]):
                continue
            queue.append(neighbor)
        if find:
            break            
        i = i + 1


    p = queue[-1]
    r = []
    while p["parent"] != -1:

        r.append(p)
        p = queue[p["parent"]]
    
    r.append(startObj)
    try:
        for sr in r:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]            
            sr["html"] = opener.open(htmlURL+sr["content"]).read().replace('\n','')
            sr["html"] = "<head><style type='text/css'>a {color:grey;}</style></head>"+sr["html"] 
            sr["html"] = urllib.quote(sr["html"])

            sr["content"] = urllib.unquote(sr["content"])

        r.reverse()
        for i in range(len(r) - 1):
            r[i]["next"] = r[i + 1]["content"]
        r[-1]["next"] = r[0]["content"]
        r.reverse()        
        print "--reversed"
    except Exception, inst:
        print inst
    print "---------------------------------------finished "
    return r
        
if __name__ == '__main__':
    print getRealName("umich")
    
