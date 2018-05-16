
#!/usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
import json

user = 'Jeff.Liu@riverbed.com'
password = 'password'
general_url = "https://riverbed-se03.riverbed.cc/api/scm.config/1.0/"
org_url = "https://riverbed-se03.riverbed.cc/api/scm.config/1.0/org/org-OrgJeffLiu-fd40ed90eac7fba6/"
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
		savedSites.append(each['id'])


# @returns dictionary of sites => attributes data
def getSites():
	nodes = getNodes()
	sitedict = {}
	for each in nodes.json()['items']:
		sitedict[each['site']] = each
	print (sitedict.keys())
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


''' @param port: use portlist or ports for more data
	@return list_of_stats: returns stats on ports for specific site'''
def getPortStats(port):
	if type(port)==list:
		list_of_stats = {}
		for each in port:
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

# @return type:dict json code on all networks associated with this org
def getNetworks():
	return requests.get(general_url + 'networks', auth= (user, password)).json()

# @return type:dict json code on all outbound rules associated with this org
def getOutboundRules():
	return requests.get(general_url + 'outbound_rules', auth= (user, password)).json()

# @return type:dict json code on all uplinks associated with this org
def getUplinks():
	return requests.get(general_url + 'uplinks', auth= (user, password)).json()

# @return type:dict json code on all wans associated with this org
def getWans():
	return requests.get(general_url + 'wans', auth= (user, password)).json()

# @return type:dict json code on all zones associated with this org
def getZones():
	return requests.get(general_url + 'zones', auth= (user, password)).json()


################################## POST/CREATE REST API PORTION ####################################


'''@param siteName: string to create site with
   @param longname: name identifier
   @paramcity location of site
   @return returns response code for creation status'''
def createSite(siteName, longname, city):
	if(siteName not in savedSites):
		payload = {'name': siteName, 'longname': longname, 'city': city}

		resps = requests.post(org_url + "sites", auth = (user, password), headers = headers, json = payload)

		return resps
	else:
		return "Site already exists. Please try again"

'''@param siteName: string to delete site with '''
def deleteSite(site):
	if(site not in savedSites):
		return "Site doesn't exist, please try again."

	return requests.delete(general_url + "site/" + site, auth = (user, password))
'''
	@param siteName: site to deploy a cloud site
'''
def cloud_deploy(siteName):
	payload = {
	  "siteid": siteName,
	  "type": "{'type' : 'Standard_DS2_v2'}",
	  #"wanopt": "{'wanopt' : 'm4.large'}",
	  "deployRedundant": "{'deployRedundant' : 0}",
	  #"awsrouting": "{'awsrouting' : 'manual'}",
	  #"uplinktype": "{'uplinktype' : 'transit_vpc'}",
	  "routing": "{'routing' : 'auto'}"
	}
	resps = requests.get(general_url + 'site/' + siteName + '/cloud-deploy', auth = (user, password))

	return resps.json()


###### This shows all the pieces running in the org ######
#print (json.dumps(getNodes().json(), indent=4))


###### This shows all the sites running in the org ######


currentSites()

#print (getSites().keys())

print (savedSites)

###### This shows all the cloud accounts running in the org ######
#print (json.dumps(getCloudAccounts(), indent = 4))
#print (json.dumps(cloud_deploy('site-AzureUSWestTestHomeOfficevnetTestHomeO-3659b5070d63a140'), indent = 4))
#print (getSiteMetrics('site-Home-d095dd2567721464'))


###### This shows all iterations to create different sites ######

'''

for i in range(0,7):
	print (createSite("test" + str(i), "testln" + str(i), "City" + str(i)))


'''

###### This runs to show all the ports in selected site ######
'''
site = input('Please choose a site from above: ')
print (json.dumps(getPortsBySites(getSites()),indent=4))
list_of_ports = getPortsBySites(getSites(), site)
print ("Site: %s \nList of ports:\n%s" %(site, '\n'.join(list_of_ports)))


###### This shows all the port stats for specific ports on sites ######

port = input("If you want all port stats, click Enter. Else, enter specific port from above:")

if (port == ''):
	print (json.dumps(getPortStats(list_of_ports), indent=4))
else:
	print (json.dumps(getPortStats(port), indent=4))
	'''

#print (json.dumps(getNetworks(), indent = 4))
#print (json.dumps(getOutboundRules(), indent = 4))



