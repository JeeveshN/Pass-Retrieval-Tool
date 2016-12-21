import subprocess
import re
import os
import sys

COMMAND_LINUX = "sudo grep -r '^psk=' /etc/NetworkManager/system-connections/"
COMMAND_WINDOWS_GENERIC = "netsh wlan show profile"
RE_LINUX = '/etc/NetworkManager/system-connections/(.*)'
SAVED_PASSWORDS = dict()

def get_pass_wind_indivisual(Name):
    output = subprocess.check_output(COMMAND_WINDOWS_GENERIC+" name="+Name+" key=clear",shell=True)
    output = re.findall('Key Content(.*)\n',output)[0].strip().split(':')[1].strip()
    return output

def make_pass_dict():
    if os.name=='posix':
        output = subprocess.check_output(COMMAND_LINUX,shell=True).split('\n')
        for pair in output:
            try:
                pair = re.findall(RE_LINUX,pair)[0].split(':')
                Name = pair[0]
                Pass = pair[1].split('=')[1]
                SAVED_PASSWORDS[Name]=Pass
            except:
                pass
    elif os.name =='nt':
        output = subprocess.check_output(COMMAND_WINDOWS_GENERIC,shell=True).split('\n')
        Names = list()
        for name in output:
            name = name.split(':')
            try:
                Names.append(name[1].strip())
            except:
                pass
        for names in Names:
            try:
                Password = get_pass_wind_indivisual(names)
                SAVED_PASSWORDS[names]=Password
            except:
                pass

def get_passwords(**kwargs):
    if 'ssid' in kwargs:
        if os.name=='nt':
            try:
                Password = get_pass_wind_indivisual(kwargs['ssid'])
                print 'Network:',kwargs['ssid'],'|''Password:',Password
            except:
                print "Wrong Network Name"
        else:
            print 'Network:',kwargs['ssid'],'|''Password:',SAVED_PASSWORDS[kwargs['ssid']]
    else:
        for name in SAVED_PASSWORDS.keys():
            print 'Network:',name,'|''Password:',SAVED_PASSWORDS[name]

def main():
    if len(sys.argv) < 2:
        make_pass_dict()
        get_passwords()
    else:
        if os.name=='posix':
            make_pass_dict()
        get_passwords(ssid=sys.argv[1])

if __name__ == "__main__":
    main()
