
import simplejson

import urllib2

lPart = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20html%20where%20url%3D%22en.wikipedia.org%2Fwiki%2F'
rPart="%22%20and%20xpath%3D'%2F%2Fa%5Bstarts-with(%40href%2C%20%22%2Fwiki%22)%20and%20not(contains(%40href%2C%20%22%3A%22))%5D'&format=json&diagnostics=true&callback="

def getNeighbor(name):
    src = lPart + name + rPart
    urlResult = ""
    try:
        urlResult = urllib2.urlopen(src).read()
    except Exception, inst:
        print inst
    return (simplejson.loads(urlResult))['query']['results']['a']

if __name__ == '__main__':
    print getNeighbor("yahoo")

