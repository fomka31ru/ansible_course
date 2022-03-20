#!/usr/bin/python
import re

from ansible.errors import (
    AnsibleFilterTypeError
)

def mac_normalize(mac, mac_sep=':'):
    
    if not isinstance(mac, str):
        return "mac is NOT a String type"
        # raise AnsibleFilterTypeError("mac address is not a String type, \n"
        #                              "got type %s instead" % type(mac))
        
    is_mac_valid = (re.match('^([0-9A-Fa-f]{12})$', mac) != None)
    is_mac_valid = is_mac_valid or (re.match('^([0-9A-Fa-f]{1,2}[\.:-]){5}[0-9A-Fa-f]{1,2}$', mac) != None)
    is_mac_valid = is_mac_valid or (re.match('^([0-9A-Fa-f]{4}[\.]){2}[0-9A-Fa-f]{4}$', mac) != None)

    if not is_mac_valid:
        return "mac address is NOT valid"
        # raise AnsibleFilterTypeError("mac address is NOT valid")
    
    mac_list = []
    for ele in re.split('\.|-|:', mac):
        mac_list += re.findall('.{1,2}', ele)
    
    mac_result = mac_sep.join([f"{ele:0>2}" for ele in mac_list])
    
    return mac_result

class FilterModule(object):
    def filters(self):
        return {
            'mac_normalize': mac_normalize
        }
