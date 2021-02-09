import os
from segno import helpers

# Contact details
input_data = {
    'user_name': 'Mesa, German',
    'display_name': 'German Mesa',
    'email': [
        'german.mesa@sap.com'
    ],
    'phone': [
        '+34 619 75 9543'
    ],
    'url': [
        "https://www.linkedin.com/in/german-mesa-sap/"
    ]
}


# Creating a QR Code encoding contact information - meCard
def create_meCard():
    # Some params accept multiple values, like email, phone, url
    qr = helpers.make_mecard(
        name=input_data['user_name'],
        email=input_data['email'],
        phone=input_data['phone'],
        url=input_data['url']
    )

    qr.save(os.path.join(os.getcwd(), 'images', 'outputs', 'qrcodes', 'qrcode_mcard.png'), scale=4)


# Creating a QR Code encoding contact information - vCard
def create_vCard():
    # Some params accept multiple values, like email, phone, url
    qr = helpers.make_vcard(
        name=input_data['user_name'],
        displayname=input_data['display_name'],
        email=input_data['email'],
        phone=input_data['phone'],
        url=input_data['url']
    )

    qr.save(os.path.join(os.getcwd(), 'images', 'outputs', 'qrcodes', 'qrcode_vcard.png'), scale=4)


def main():
    # Creating a QR Code encoding contact information - meCard
    create_meCard()

    # Creating a QR Code encoding contact information - vCard
    create_vCard()


if __name__ == '__main__':
    main()
