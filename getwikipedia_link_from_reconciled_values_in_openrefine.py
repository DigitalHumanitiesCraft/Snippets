import json
import urllib2

site = "dewiki"
url = "https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=sitelinks/urls&ids=" + \
    cell.recon.match.id + "&sitefilter=%s" % site
response = urllib2.urlopen(url)
json = json.loads(response.read())
for i in json['entities'].values():
    return i['sitelinks'][site]['url']
