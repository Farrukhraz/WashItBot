# This util is used to read QR code from the image

import requests
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from pyzbar.pyzbar import decode


def get_qr_code_content(image: JpegImageFile) -> str:
    try:
        decoded_barcode = decode(image)
    except Exception:
        decoded_barcode = []
    decoded_barcode_data = ""
    if decoded_barcode:
        try:
            if len(decoded_barcode) > 1:
                decoded_barcode = __sort_barcodes_by_coordinates(decoded_barcode)
            decoded_barcode_data = decoded_barcode[0].data
        except Exception as exc:
            raise KeyError(f"Unsupported barcode format. Couldn't read data from barcode. Error: {exc}")
        try:
            decoded_barcode_data = decoded_barcode_data.decode('utf-8')
        except UnicodeDecodeError as exc:
            decoded_barcode_data = ""
    return decoded_barcode_data


def get_machine_number(image_url: str) -> (str, int):
    """ Returns name of the machine and its number
    Example:
        Стиральная машина, 3
        Сушилка, 1
    """
    result = None, None
    img = Image.open(requests.get(image_url, stream=True).raw)
    image_content = get_qr_code_content(img)
    splitted_image_content = image_content.strip().split(r'#')
    if len(splitted_image_content) != 2:
        return result
    machine = splitted_image_content[1]
    if "stiralka" not in machine and "sushilka" not in machine:
        return result
    name, number = splitted_image_content[1].split('_')
    if name == "stiralka":
        name = "Стиральная машина"
    else:
        name = "Сушилка"
    return name, number


def __sort_barcodes_by_coordinates(decoded_barcodes: list) -> list:
    """ Sorts by top left corner """
    decoded_barcodes_sorted_by_x = sorted(decoded_barcodes, key=lambda x: x.rect.left)
    decoded_barcodes_sorted_by_y = sorted(decoded_barcodes_sorted_by_x, key=lambda y: y.rect.top)
    return decoded_barcodes_sorted_by_y



