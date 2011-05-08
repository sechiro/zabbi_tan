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
    cmd = "uptime"  # 対象コマンドが見つからなかったら、とりあえずuptime
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
            
    f = open(homedir + "\conf\hostsetting.dat")
    line = f.readline()
    while line:
        if re.match("#", line ):
            line = f.readline()            
            continue
            
        line = line.rstrip()
        params.append(line.split(","))
        line = f.readline()

    #print params
    message = log = ''
    log_file = '\log\ssh4sstp.log'
    try:
        log_f = open(homedir + log_file, 'ab')
    except:
        message += ur'ログファイルが開けないわ。\e'
        ghost_name = u'ざびたん'
        request = sstp_send_request(message, ghost_name)
        send_sstp(request)
        exit()

    print 'Now Executing...'
    log += '========================================\n' + \
            'Executed Command: ' + cmd + \
            '\n========================================\n'

     
    for hostname,ip,port,username,password,key_filename in params:
        port = int(port)
        conn = None
        try:
            conn = p.SSHClient()
            conn.set_missing_host_key_policy(p.AutoAddPolicy())
            try:
                conn.connect(hostname=ip,port=port,username=username,key_filename=key_filename)
                login = 'Login with keyfile'
            except:
                conn.connect(hostname=ip,port=port,username=username,password=password)
                login = 'Login with password'

            i,o,e = conn.exec_command(cmd)

            if re.match('sudo ', cmd) and ( password != '' ):
                i.write( (password + '\n') )
                i.flush()
                print 'sudo with password'
                data = e.read()#.splitlines()
                print data
            
            data = o.read()#.splitlines
            message += hostname + ':\\n'
            log += hostname + '(' + login + ')\n'
            message += ( re.sub(r'\n', r'\\n', data ) ).decode('utf-8')
            log += data.decode('utf-8')
            message += r'\n'
            log += '\n'
            #print message
            
        finally:
            if conn: conn.close()
            
    log_f.write(log.encode('utf-8'))
    message += ur'実行ログは \f[underline,true]\q[ログファイル,ViewSSHLog]\f[underline,false]を見てね♪\n(' + re.sub(r'\\', r'\\\\', (homedir + log_file) ) + ')'

    #print message
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
