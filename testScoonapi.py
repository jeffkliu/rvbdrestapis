import requests
from requests.auth import HTTPBasicAuth
import json

user = 'Jeff.Liu@riverbed.com'
password = 'Natures546!@'
general_url = "https://riverbed-se03.riverbed.cc/api/scm.config/1.0/"
org_url = "https://riverbed-se03.riverbed.cc/api/scm.config/1.0/org/org-OrgJeffLiu-fd40ed90eac7fba6/"
#auth = requests.get(url, auth =(user, password))
#print (auth)
headers = {'Content-type':'application/json'}

# returns all the nodes that are associated with this particular org
def getNodes():
	return requests.get(org_url + "nodes", auth =(user, password))

# returns dictionary of sites => attributes data
def getSites():
	nodes = getNodes()
	sitedict = {}
	for each in nodes.json()['items']:
		sitedict[each['site']] = each
	return sitedict

	''' @param site: if dictionary, print site=>ports mapping.
		if single site, print respective site and ports '''
def getPortsBySites(site_dict, site=None):
	if (site == None) :
		new_dict = {}
		print ("Let's print out all of sites ports")
		for each in site_dict:
			new_dict[each] = site_dict[each]['ports']
		return new_dict
	else:
		return site_dict[site]['ports']


def getPortStats(port):
	if type(port)==list:
		list_of_stats = {}
		for each in port:
			print (each)
			resps = requests.get(general_url + "port/" + each, auth =(user, password))
			list_of_stats[each] = (resps.json())
		return list_of_stats
	elif type(port) == str:
		return requests.get(general_url + "port/" + port, auth =(user, password)).json()


print (json.dumps(getSites(), indent=4))
print (json.dumps(getPortsBySites(getSites()),indent=4))
list_of_ports = getPortsBySites(getSites(), "site-Boston-68e0791f7e0ac6cd")
print (list_of_ports)
print (json.dumps(getPortStats(list_of_ports), indent=4))


