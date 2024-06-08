import os
import sys


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    resource_path = os.path.join(base_path, relative_path)
    return resource_path