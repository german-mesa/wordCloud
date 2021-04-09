import os
import qrcode


def main():
    # Link for website
    input_links = [
        {
            'file': 'qrcode_candidate.png',
            'url': "https://performancemanager5.successfactors.eu/sf/careers/mycandprofile?bplte_company=SAP&_s.crb=kpi%252bSwIbU5oV70VKPvQtpvhMnIx3Ig5mF%252fAuZeJzAuI%253d"
        },
        {
            'file': 'qrcode_linkedin.png',
            'url': "https://www.linkedin.com/in/german-mesa-sap/"
        },
        {
            'file': 'qrcode_youtube.png',
            'url': "https://youtu.be/j3dNiMRtReY/"
        },
        {
            'file': 'qrcode_int_advisory.png',
            'url': "https://open.sap.com/verify/xeneb-fofun-befes-bodog-vycuc"
        },
        {
            'file': 'qrcode_int_intelligent_suite.png',
            'url': "https://open.sap.com/verify/xubov-decon-decav-vamef-zapyp/"
        },
        {
            'file': 'qrcode_i4now.png',
            'url': "https://www.youracclaim.com/badges/d0032cde-1404-4525-b1b6-1a346577a064?source=linked_in_profile"
        },
        {
            'file': 'qrcode_ml_tf_gcp.png',
            'url': "https://www.coursera.org/account/accomplishments/specialization/QM2XU3B2WVBU"
        },
        {
            'file': 'qrcode_ml_deep_tf_developer.png',
            'url': "https://www.coursera.org/account/accomplishments/specialization/FBHF3W2AF9SR"
        },
        {
            'file': 'qrcode_innovation_man.png',
            'url': "https://www.youracclaim.com/badges/d4731efc-be7d-48be-95ab-453e749c383e"
        },
        {
            'file': 'qrcode_rpa.png',
            'url': "https://open.sap.com/verify/xegen-nosel-dunot-sefaf-mazaf"
        },
        {
            'file': 'qrcode_docker.png',
            'url': "http://ude.my/UC-0Z4GY5N3"
        },
        {
            'file': 'qrcode_kyma.png',
            'url': "https://open.sap.com/verify/xepoc-nogub-bigam-pytid-torit"
        },
        {
            'file': 'qrcode_graph.png',
            'url': "https://open.sap.com/verify/xutep-hisym-lanem-kofan-fasyt"
        },
        {
            'file': 'qrcode_deep_learning.png',
            'url': "https://www.coursera.org/account/accomplishments/specialization/7LUZDHBK5EDD"
        },
        {
            'file': 'qrcode_machine_learning.png',
            'url': "https://www.coursera.org/account/accomplishments/verify/4HUKCZHXTD4Q"
        },
        {
            'file': 'qrcode_tensorflow_certificate.png',
            'url': "https://www.credential.net/03832cfb-7af3-4d2b-8f72-b41e6e8771e8"
        }
    ]

    # Creating an instance of qrcode
    for link in input_links:
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)

        qr.add_data(link['url'])
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        img.save(os.path.join(os.getcwd(), 'images', 'outputs', 'qrcodes', link['file']))

        qr.clear()


if __name__ == '__main__':
    main()
