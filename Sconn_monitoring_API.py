
#!/usr/bin/env python

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
savedSites = []

# @returns all the nodes that are associated with this particular org
def getNodes():
	return requests.get(org_url + "nodes", auth =(user, password))

#@returns all sites without the key
def currentSites():
	arr = []
	resps = requests.get(general_url + "sites" ,auth = (user, password))
	saveddict = resps.json()
	for each in saveddict['items']:
		savedSites.append(each['name'])


# @returns dictionary of sites => attributes data
def getSites():
	nodes = getNodes()
	sitedict = {}
	for each in nodes.json()['items']:
		sitedict[each['site']] = each
	return sitedict

''' @param site: if dictionary, print site=>ports mapping.
	if single site, print respective site and ports 
	@param site_dict: dictionary of all the sites
	@return returns all ports associated with site in list format'''
def getPortsBySites(site_dict, site=None):
	if (site == None) :
		new_dict = {}
		print ("Let's print out all of sites ports")
		for each in site_dict:
			new_dict[each] = site_dict[each]['ports']
		return new_dict
	else:
		return site_dict[site]['ports']


''' @param port: use portlist or ports for more data'''
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


'''@param site: specific site to grab metrics for
   @return resps metric info in rest format'''
def getSiteMetrics(site):
	if type(site) != str:
		return "Invalid Site. Please try again"
	print (site)

	resps = requests.get(general_url + "site/" + site + "/sitelinks", auth = (user, password))

	return resps

# @return type:dict json code on all cloud accounts associated with this org
def getCloudAccounts():
	return requests.get(org_url + 'cloud-accounts', auth= (user, password)).json()


################################## POST/CREATE REST API PORTION ####################################


'''@param siteName: string to create site with
   @param longname: name identifier
   @paramcity location of site
   @return returns response code for creation status'''
def createSite(siteName, longname, city):
	if(siteName not in savedSites):
		payload = {'name': siteName, 'longname': longname, 'city': city}
		header = {'content-type' : 'application/json'}

		resps = requests.post(org_url + "sites", auth = (user, password), headers = header, json = payload)

		return resps
	else:
		return "Site already exists. Please try again"



#print (json.dumps(getSites(), indent=4))
#print (getSites().keys())
currentSites()
print (savedSites)
print (createSite('TX', 'Long Horn', 'Houston'))
print (json.dumps(getCloudAccounts(), indent = 4))
#print (getSiteMetrics('site-Home-d095dd2567721464'))
#print (json.dumps(createSite('testsite123').json(), indent = 4))
'''
print (json.dumps(getPortsBySites(getSites()),indent=4))
list_of_ports = getPortsBySites(getSites(), "site-Boston-68e0791f7e0ac6cd")
print (list_of_ports)
print (json.dumps(getPortStats(list_of_ports), indent=4))
'''


