#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():
    import sys
    import re
    import os
    import paramiko as p

    message = ''
    argvs = []
    params = []    
    cmd = "uptime"
    homedir = os.path.dirname(os.path.abspath(__file__))
    
    # Ensure variable is defined
    try:
        cmd = sys.argv[1]
    except:
        cmd = "uptime"

    datafile = open(homedir + "\conf\zabbitan.dat")
    argv_data = datafile.readline()
    while argv_data:
        if re.match("#", argv_data ):
            argv_data = datafile.readline()            
            continue
            
        argvs.append(argv_data.rstrip())
        print argvs
        cmd = argvs[0]
        argv_data = datafile.readline()    
            
    f = open(homedir + "\conf\servers")
    line = f.readline()
    while line:
        if re.match("#", line ):
            line = f.readline()            
            continue
            
        line = line.rstrip()
        params.append(line.split(","))
        line = f.readline()

    print params
    message = ""
    
    for hostname,port,username,key_filename in params:
        port = int(port)
        conn = None
        try:
            conn = p.SSHClient()
            conn.set_missing_host_key_policy(p.AutoAddPolicy())
            conn.connect(hostname,port=port,username=username,key_filename=key_filename)
            i,o,e = conn.exec_command(cmd)
            i.flush()
            data = o.read()#.splitlines()
            #print "%s   %s" % ( hostname, o.read().strip() )
            message += hostname + ": "
            message += data.decode("utf-8")
            message += ur'\n'

        finally:
            if conn: conn.close()

    message += ur'\e'
    ghost_name = u'ざびたん'
    request = sstp_send_request(message, ghost_name)
    send_sstp(request)


def sstp_send_request(message, ghost_name=u'test-agent'):
    request = u'SEND SSTP/1.4\r\n'
    request += u'Sender: ' + ghost_name + u'\r\n'
    request += u'Script: ' + message + u'\r\n' 
    request += u'Charset: UTF8\r\n'
    return request


def send_sstp(request, host=u'localhost', port=9801):
    """send socket"""
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(request.encode('utf-8'))
    s.close()
    

if __name__ == '__main__':
    main()
