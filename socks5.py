#plink.exe -ssh -P 10022 -l admin -pw ala1289 -D 127.0.0.1:8080 10.60.1.150

import sys, subprocess, winreg

#A value of 3 mean use manual settings. A value of 9 mean use automatic settings. A value of 1 means it is not enabled.
def proxy_on():
    key=winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections",0,winreg.KEY_ALL_ACCESS)
    (value, regtype) = winreg.QueryValueEx(key, "DefaultConnectionSettings")
    if regtype == winreg.REG_BINARY:
        #print("value: ", value, "\n\n")
        value = value[:8] + b'\x03' + value[9:]
        #print("value: ", value, "\n\n" )
    winreg.SetValueEx(key, "DefaultConnectionSettings", None, regtype, value)
    print('socks on')
#A value of 3 mean use manual settings. A value of 9 mean use automatic settings. A value of 1 means it is not enabled.
def proxy_off():
    key=winreg.OpenKey(winreg.HKEY_CURRENT_USER,"Software\Microsoft\Windows\CurrentVersion\Internet Settings\Connections",0,winreg.KEY_ALL_ACCESS)
    (value, regtype) = winreg.QueryValueEx(key, "DefaultConnectionSettings")
    if regtype == winreg.REG_BINARY:
        #print("value: ", value, "\n\n")
        value = value[:8] + b'\x01' + value[9:]
        #print("value: ", value, "\n\n" )
    winreg.SetValueEx(key, "DefaultConnectionSettings", None, regtype, value)
    print('socks off')

#check arguments
if len(sys.argv) < 5:
    print('''\nToo few arguments. Usage: socks5.py <ip> <port> <login> <password>''')
    exit()

ip = sys.argv[1]
port = sys.argv[2]
login = sys.argv[3]
password = sys.argv[4]

#print arguments
#for argument in  sys.argv:
    #print("arg: ", argument)

#run ssh dynamic portforwarding, run in thread
try:
    proxy_on()
    cmd = "C:\\tools\plink.exe -ssh -P " +port + " -l " + login + " -pw " + password + " -D 127.0.0.1:8080 " +ip
    rv = subprocess.call(cmd, shell=True)
    print("\nreturn value: ", rv)
except subprocess.SubprocessError as subProcErr:
    print(subProcErr)
    proxy_off()
except subprocess.TimeoutExpired as subProcTimeout:
    print(subProcTimeout)
    proxy_off()    
finally:
    proxy_off()
    print('done')

