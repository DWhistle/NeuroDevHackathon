#!/usr/bin/env python
# coding: utf-8

# In[46]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import socket
import copy
import json
import scipy as sp
from scipy.signal import argrelextrema
# In[188]:





# In[2]:



import zerorpc


# In[1]:



def build_plot(json_t):


    raw_data = {}
    def data_former(json_d):
        json_cpy = copy.copy(json_d)
        count = 0
        stamps = {}
        for raw in json_cpy['DataPacketValue']:
            stamps['Value_' + str(count)] = raw
            count +=1
        del json_cpy['DataPacketValue']
        del json_cpy['Timestamp']
        json_cpy.update(stamps)
        return json_cpy

    counter = 0
    for i in json_t:
        raw_data[i['Timestamp']] = data_former(i)
        counter+=1
    df3 = pd.DataFrame(raw_data).transpose()

	df3 = df3.drop(df3.std()[df3.std() < 0.3].index.values, axis=1)
    df3['Value'] =  (df3['Value_0'] + df3['Value_1'] +df3['Value_2'] +df3['Value_3'] + df3['Value_5']) / 5
    df3.drop(columns=['Value_0', 'Value_1', 'Value_2', 'Value_3', 'Value_4', 'Value_5'], inplace=True)

    outliers = []
    ret_json = {}
    outliers_indexes = np.array(df3['Value']).argsort()[-10:][::-1]
    def sort_outliers(array):
        array.sort()
        array = array[::-1]
        to_ret = [array[val] for val in range(5,15)]
        return (to_ret)
    outliers = sort_outliers(list(df3['Value']))
    indexes  = df3.index
    outs = []
    df3 = df3.reset_index()
    to_ret = df3.to_dict('records')
    final_dict = {}
    co = 0
    for elem in to_ret:
        if elem['Value'] in outliers:
           final_dict[co] = elem
           co+=1
    #for s in range(10):
    #     outs.append(indexes.get_loc(outliers[s]))
    #print(outliers)
    print (final_dict)
    return (json.dumps(final_dict))
	# In[ ]:



class StreamingRPC(object):
    @zerorpc.stream
    def streaming_range(self, stage, json, arg):
        output = build_plot(json)
        return (output, arg)

s = zerorpc.Server(StreamingRPC())
s.bind("tcp://127.0.0.1:4242")
s.run()



"""
def device_data_processor(df):
    time_global = df['t']
    counter = []
    counter_local = []
    time_local = []
    value_local = []
    for c in df['c']:
        counter.append(c)
    for s in df['s']:
        value_local.append(s['v'])
        time_local.append(pd.to_datetime(time_global) + pd.to_timedelta(s['t']))
        counter_local.append(s['c'])
    return (time_local, counter_local, value_local)

print(df['t'])
date = pd.to_datetime(df['t'][0])
print(date)
#print(counter, counter_local, value_local, time_local)
"""

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjdjMmQzOWZlN2NlMWE2NTMwNWRlZjJiNjAzMTNhYjVhIiwidHlwIjoiSldUIn0.eyJuYmYiOjE1NjE4MTY2NDYsImV4cCI6MTU2MjE3NjY0NiwiaXNzIjoiaHR0cDovL2NkYi5uZXVyb3Aub3JnIiwiYXVkIjpbImh0dHA6Ly9jZGIubmV1cm9wLm9yZy9yZXNvdXJjZXMiLCJhcGkiXSwiY2xpZW50X2lkIjoiNjMiLCJzdWIiOiI0MTkiLCJhdXRoX3RpbWUiOjE1NjE4MTY2NDYsImlkcCI6IlZDQSIsIm5hbWUiOlsi0JTQvNC40YLRgNC40Lkg0KHRg9GH0LrQvtCyIiwi0JTQvNC40YLRgNC40Lkg0KHRg9GH0LrQvtCyIl0sInJvbGUiOiJVU0VSIiwic2NvcGUiOlsiYXBpIl0sImFtciI6WyJleHRlcm5hbCJdfQ.bY63zJERCvDLVDn_dDNC4a7rPVPI5wQHF5ry6BgTRq3fOUHrY1Z7s-oA1lD8zP5lxfJhb8SGg6WaFjV6FnWKI0fd7dqYmYxQTQi8fbuN9lM_anV_5GCIBqfSeB-Ry7E5Q5hMOZB7gqMwaELm0RwDZ97g4QHXes8D_WdwYnYK5XsTmpXlPJNuyc5QW9qiTIyG_BgkmzQrXjfjESE-iwx9YAwOyjOJ3KzkeXQuCGAtMlN6Y7z8-QbWkkok4ruEiPj0_HOepoqCJNHlmvK10Ewk72BN-CE34I0w5XAOQcISqvzQxNZKrnl2s4Yx1QPDi_pS2dbHk0VqM8z8mlZJ3R7qQA"
json_request ="""
{
  "Command": {
    "CommandType": "start",
    "CommandId": "{commandId}",
    "Args": {
      "AccessToken": +
      """ + token +  ',' + """
      "ModelId": "ostrov1022",
      "Model": "<modules/>",
      "RunModules": true
    }
"""

headers = """POST /npe/engine HTTP/1.1\r
Content-Type: {content_type}\r
Content-Length: {content_length}\r
Host: {host}\r
Connection: close\r
\r\n"""
"""
host_neu = "ws://cdb.neurop.org"
port_neu = 8080
json_bytes = json_request.encode("ascii")
header_bytes = headers.format(
        content_type=json_request,
        content_length=len(json_request),
        host=host_neu
        ).encode('iso-8859-1')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host_neu,port_neu))
s.sendall(header_bytes + json_bytes)
"""
# In[191]: