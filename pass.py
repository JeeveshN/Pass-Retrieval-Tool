import subprocess
import re
import os
import sys

COMMAND_LINUX = "sudo grep -r '^psk=' /etc/NetworkManager/system-connections/"
COMMAND_OSX = "defaults read /Library/Preferences/SystemConfiguration/com.apple.airport.preferences |grep SSIDString"
COMMAND_WINDOWS_GENERIC = "netsh wlan show profile"
RE_LINUX = '/etc/NetworkManager/system-connections/(.*)'
RE_OSX = 'SSIDString = (.*);'
PASS_OSX = 'security find-generic-password -wa '
SAVED_PASSWORDS = dict()

def get_pass_wind_individual(Name):
    output = subprocess.check_output(COMMAND_WINDOWS_GENERIC+" name="+Name+" key=clear",shell=True)
    output = re.findall('Key Content(.*)\n',output)[0].strip().split(':')[1].strip()
    return output

def make_pass_dict():
    if os.name=='posix':
        try:
            output = subprocess.check_output(COMMAND_LINUX,shell=True).split('\n')
            for pair in output:
                try:
                    pair = re.findall(RE_LINUX,pair)[0].split(':')
                    Name = pair[0]
                    Pass = pair[1].split('=')[1]
                    SAVED_PASSWORDS[Name]=Pass
                except:
                    pass
        except:
            output = subprocess.check_output(COMMAND_OSX,shell=True).split('\n')
            for pair in output:
                try:
                    Name = re.findall(RE_OSX,pair)[0]
                    Pass = subprocess.check_output(PASS_OSX + Name,shell=True)
                    print "Getting password for " + Name
                    SAVED_PASSWORDS[Name] = Pass
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
                Password = get_pass_wind_individual(names)
                SAVED_PASSWORDS[names]=Password
            except:
                pass

def get_passwords(**kwargs):
    if 'ssid' in kwargs:
        if os.name=='nt':
            try:
                Password = get_pass_wind_individual(kwargs['ssid'])
                print 'Network:',kwargs['ssid'],'|''Password:',Password
            except:
                print "No Such SSID exists"
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
