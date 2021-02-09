import os
import qrcode


def main():
    # Link for website
    input_links = [
        {
            'file': 'qrcode_linkedin.png',
            'url': "https://www.linkedin.com/in/german-mesa-sap/"
        },
        {
            'file': 'qrcode_youtube.png',
            'url': "https://youtu.be/j3dNiMRtReY"
        }
    ]

    # Creating an instance of qrcode
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)

    for link in input_links:
        qr.add_data(link['url'])
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        img.save(os.path.join(os.getcwd(), 'images', 'outputs', 'qrcodes', link['file']))


if __name__ == '__main__':
    main()
