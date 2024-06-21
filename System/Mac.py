import uuid


def get_selected_address():
    default_mac = hex(uuid.getnode())
    return default_mac


