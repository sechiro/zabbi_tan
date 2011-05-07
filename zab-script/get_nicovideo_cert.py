#! /usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2

# JSON
try:
    import simplejson as json
except ImportError:
    import json

def main():
    """ Get authenticate """
    params = {}
    params['user'] = 'Admin'
    params['password'] = 'zabbix'
    
    api_request = {}
    api_request['method'] = 'user.authenticate'
    api_request['params'] = params                                                
    
    data = get_zabbix_data(api_request=api_request)
    api_request['auth'] = data['result'] 

    params = {}     # params, filterは原則毎回初期化
    filter = {}
    api_request['method'] = 'host.get'
    filter['host'] = 'secure.nicovideo.jp'
    params['filter'] = filter
    api_request['params'] = params
    
    data = get_zabbix_data(api_request=api_request)
    hostid = data['result'][0]['hostid']
    
    params = {} 
    filter = {}
    api_request['method'] = 'item.get'
    filter['key_'] = 'ssl-check.sh[443]'
    params['hostids'] = hostid
    params['filter'] = filter
    api_request['params'] = params
    data = get_zabbix_data(api_request=api_request)
    #print data['result'][0]['lastvalue']
    nico_limit = str(data['result'][0]['lastvalue'])

    message = ur'secure.nicovideo.jpの証明書が失効するまで、\nあと' + str(nico_limit) + ur'日のようね。\n\e';
    send_sstp(message)

def get_zabbix_data(api_request, zabbix_host='http://192.168.11.201'):
    api_url = zabbix_host + '/zabbix/api_jsonrpc.php'
    headers = {'Content-Type': 'application/json-rpc'}  # このHeaderは必須
    if not ('id' in api_request):
        api_request['id'] = 0
    else:
        api_request['id'] += 1
        
    api_request['jsonrpc'] = '2.0'
    params = api_request['params']
    
    if not ('limit' in params):
        params['limit'] = 10
    if not ('output' in params):
        params['output'] = 'extend'

    api_request['params'] = params    
    json_request = json.dumps(api_request)

    request = urllib2.Request(api_url, json_request, headers)
    p = urllib2.urlopen(request)
    data = json.loads(p.read())
    return data


def send_sstp(message, ghost_name=u'ざびたん', host=u'localhost', port=9801):
    """send by socket"""
    import socket
    
    request = u'SEND SSTP/1.4\r\n'
    request += u'Sender: ' + ghost_name + u'\r\n'
    request += u'Script: ' + message + u'\r\n' 
    request += u'Charset: UTF8\r\n'    

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((host, port))
    s.send(request.encode('utf-8'))

    # For Debug
    #s.settimeout(180)
    #res = s.recv(2)
    #print repr(res)
    s.close()
                  

if __name__=="__main__":
    main()
