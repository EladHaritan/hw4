#!/usr/bin/env python
# coding: utf-8

# In[107]:


import requests
import urllib
key = # Enter API #
source_city = 'Tel Aviv'


# In[108]:


dests = open('dests.txt','r',encoding = 'utf8')
destlist=list()
for line in dests:
    destlist.append(line.rstrip('\n'))

print (destlist)


# In[109]:


gotoAPI = input("Do you want to go to API? Enter 'Y' to proceed: ").lower()=='y'
if gotoAPI:
    distancematrix_url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    distancematrix_parms={'origins': source_city,'key': key}
    destdata = dict()
    for des in destlist:
        destdata[des]=dict()
        distancematrix_parms['destinations'] = des
        url = distancematrix_url+urllib.parse.urlencode(distancematrix_parms)
        try:
            response = requests.get(url)
            if not response.status_code == 200:
                print('distancematrix HTTP Error:',response.status_code)
            else:
                try:
                    response_data = response.json()
                except:
                    print('Response distancematrix Not Valid In JSON Format')
        except:
            print('Somthing went wrong with distancematrix response.get')
        destdata[des]['destination_data']=response_data

        url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (des,key)
        try:
            response = requests.get(url)
            if not response.status_code == 200:
                print('geocode HTTP Error:',response.status_code)
            else:
                try:
                    response_data = response.json()
                except:
                    print('Response geocode Not Valid In JSON Format')
        except:
            print('Somthing went wrong with geocode response.get')
        destdata[des]['geocode_data']=response_data
    print("Done")
else:
    print("Exit")


# In[110]:


final_data = dict()
for city,data in destdata.items():
    dist = data['destination_data']['rows'][0]['elements'][0]['distance']['text']
    dur = data['destination_data']['rows'][0]['elements'][0]['duration']['text']
    lng = data['geocode_data']['results'][0]['geometry']['location']['lng']
    lat = data['geocode_data']['results'][0]['geometry']['location']['lat']
    final_data[city]=(dist,dur,lng,lat)


# In[111]:


for city,data in final_data.items():
    print("City: "+city+'\n'+
          '\t'+'Distance from '+source_city+': '+data[0]+'\n'+
          '\t'+'Duration: '+data[1]+'\n'+
          '\t'+'Longitude: '+str(data[2])+'\n'+
          '\t'+'Latitude: '+str(data[3]))


# In[121]:


sorted_cities = sorted(final_data.items(), key=lambda x: x[1][0], reverse=True)
for i in sorted_cities[:3]:
    print(i[0], i[1][0])


# In[ ]:




