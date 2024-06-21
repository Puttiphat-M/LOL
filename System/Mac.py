import psutil

def get_mac_address():
    interfaces = psutil.net_if_addrs()
    for interface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:
                mac_address = addr.address
                if mac_address != '00:00:00:00:00:00':
                    mac_address = mac_address.replace(':', '')
                    return mac_address
    return None
