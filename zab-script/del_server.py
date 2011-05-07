#!/usr/bin/env python
# -*- coding: utf-8 -*-

def main():
    import sys
    import re
    import os

    message = ''
    argvs = []
    params = []    
    homedir = os.path.dirname(os.path.abspath(__file__))
    
    datafile = open(homedir + "\zabbitan.dat")
    argv_data = datafile.readline()
    while argv_data:
        if re.match("#", argv_data):
            argv_data = datafile.readline()            
            continue
            
        argvs.append(argv_data.rstrip())
        print argvs
        targethost = argvs[0]
        argv_data = datafile.readline()    
            
    f = open(homedir + "\hostsetting.dat" , "r")
    line = f.readline()
    
    while line: 
        line = line.rstrip()
        params.append(line.split(","))
        line = f.readline()

    print params
    f.close

    f = open(homedir + "\hostsetting.dat" , "w")
    g = open(homedir + "\hosts.dat" , "w")
    message = ""
    hostsettings = []
       
    for hostsettings in params:
        if targethost == hostsettings[0]:
            continue
        else:
            medium = ','
            setting = medium.join(hostsettings)
            setting += "\n"
            hostname = hostsettings[0] + "\n"
            f.write(setting)
            g.write(hostsettings[0])
   
    f.close
    g.close
    
   

if __name__ == '__main__':
    main()
