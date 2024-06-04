from getmac import get_mac_address


def get_selected_address():
    default_mac = get_mac_address()
    default_mac = default_mac.replace(':', '')
    return default_mac

