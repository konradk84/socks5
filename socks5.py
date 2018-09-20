import sys, subprocess, winreg, configparser

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
if len(sys.argv) < 3:
    print('''\nToo few arguments. Usage: socks5.py <config_section> <ip> ''')
    exit()

cfg = configparser.ConfigParser()
cfg.read('config.ini')

config = sys.argv[1]
ip = sys.argv[2]

login = cfg[config]['LOGIN']
password = cfg[config]['PASSWORD']
port = cfg[config]['PORT']

#print arguments
#for argument in  sys.argv:
    #print("arg: ", argument)

#run ssh dynamic port forwarding
try:
    proxy_on()
    #export plink path to config file
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

