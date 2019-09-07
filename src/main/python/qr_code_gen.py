import qrcode

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()
    img.save("./src/main/resources/qr.jpg")
    return img

import socket


IP_ADDR = "http://" + socket.gethostbyname(socket.gethostname()) + ":" + str(8000)
generate_qr_code(IP_ADDR)