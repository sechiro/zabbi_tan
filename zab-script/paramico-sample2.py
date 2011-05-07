#!/usr/bin/env python
#coding:shift-jis
def main():
    import sys
    import re
    host = 'localhost'
    port = 9801
    message = ''
    from subprocess import list2cmdline

    import paramiko as p
    cmd = "/sbin/service httpd restart"
    #cmd = "uptime"
    servers =[
        ( "192.168.11.201" ,"root" ,"hogehoge" ),  # server, user, pwd
        ( "192.168.11.202" ,"root" ,"hogehoge" ),  # server, user, pwd
        ( "192.168.11.203" ,"root" ,"hogehoge" ),  # server, user, pwd
    ]

    message = ""

    for hostname,username,password in servers:
        conn = None
        try:
            conn = p.SSHClient()
            conn.set_missing_host_key_policy(p.AutoAddPolicy())
            conn.connect(hostname,username=username,password=password)
            i,o,e = conn.exec_command(cmd)
            i.write("hogehoge\n")
            i.flush()
            data = o.read()#.splitlines()
            data2 = data.decode("utf8")
            data3 = data2.splitlines()
            #print "%s   %s" % ( hostname, o.read().strip() )
            print data3
            message += hostname + ":" +ur'\n'
            
            for line in data3:
                message += "  " + line
                message += ur'\n'

        finally:
            if conn: conn.close()

    message += ur'\e'
    ghost_name = u'ざびたん'
    request = sstp_send_request(message, ghost_name)
    send_sstp(host, port, request)


def sstp_send_request(message, ghost_name=u'test-agent'):
    request = u'SEND SSTP/1.4\r\n'
    request += u'Sender: ' + ghost_name + u'\r\n'
    request += u'Script: ' + message + u'\r\n' 
    request += u'Charset: UTF8\r\n'
    return request


def send_sstp(host, port, request):
    """send socket"""
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(request.encode('utf-8'))
    s.close()
    

if __name__ == '__main__':
    main()
