import requests

from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import Qgis

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def validate_key(apikey='') -> bool:
    testurl = 'https://api.maptiler.com/maps/basic/style.json?key='
    response = requests.get(testurl + apikey)
    
    if response.status_code == 200:
        return True
    
    print(f"key validation error code:{response.status_code}")
    return False


def is_qgs_vectortile_api_enable():
    # judge vtile is available or not
    # e.g. QGIS3.10.4 -> 31004
    qgis_version_str = str(Qgis.QGIS_VERSION_INT)
    minor_ver = int(qgis_version_str[1:3])
    return minor_ver >= 13


def is_in_darkmode(threshold=383):
    """detect the Qt in Darkmode or not 

    This function has a dependancy on PyQt, QMessageBox.
    Although Qt has no API to detect running in Darkmode or not,
    it is able to get RGB value of widgets, including UI parts of them.
    This function detect Darkmode by evaluating a sum of RGB value of the widget with threshold.

    Args:
        threshold (int, optional): a sum of RGB value (each 0-255, sum 0-765). Default to 383, is just median.
    Returns:
        bool: True means in Darkmode, False in not.
    """
    # generate empty QMessageBox to detect
    # generated widgets has default color palette in the OS
    empty_mbox = QMessageBox()

    # get a background color of the widget
    red = empty_mbox.palette().window().color().red()
    green = empty_mbox.palette().window().color().green()
    blue = empty_mbox.palette().window().color().blue()

    sum_rgb_value = red + green + blue
    return sum_rgb_value < threshold


if __name__ == "__main__":
    validate_key('')
