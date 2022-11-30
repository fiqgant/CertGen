from PIL import Image, ImageDraw, ImageFont

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formataddr
from email import encoders

import pandas as pd
import smtplib
import ssl

# Import the excel file
data = pd.read_excel("List.xlsx")

# Import 'Name' List from list.xlsx
name_list = data['Name'].to_list()

# Determining the length of the list
max_no = len(name_list)

# The Loops for creating certificates in bulk
# for i in name_list:
for idx, i in enumerate(name_list):

    im = Image.open("Template/Certificate.jpg")
    d = ImageDraw.Draw(im)
    text_color = "#ffffff"
    bounding_box = [1462, 2450, 8021, 2450]
    x1, y1, x2, y2 = bounding_box  # For easy reading
    font = ImageFont.truetype("Fonts/Bajigoor.ttf", 450, encoding="unic")
    w, h = d.textsize(i.title(), font=font)
    x = (x2 - x1 - w) / 2 + x1
    y = (y2 - y1 - h) / 2 + y1

    # Write the text to the image, where (x,y) is the top left corner of the text
    d.text((x, y), i.title(), align='center', font=font, fill=text_color)
    im.save("Output/Certificate_TRPLWBI2022_"+i+".pdf")
    print("(%d/%d) Certificate Created for:  %s" % (idx+1, max_no, i.title()))

print("Done - Created by fiq")

sender_email = "EMAIL"
sender_name = "NAME"
password = "APP_PASSWORD"

receiver_emails = data['Email'].to_list()
receiver_names = data['Name'].to_list()

for receiver_email, receiver_name in zip(receiver_emails, receiver_names):

    print("Sending to " + receiver_name)
    msg = MIMEMultipart()
    msg['Subject'] = 'TEST-Certificate of Participation | ' + receiver_name + ' | TRPL PWBI'
    msg['From'] = formataddr((sender_name, sender_email))
    msg['To'] = formataddr((receiver_name, receiver_email))

    msg.attach(MIMEText("""Hello """ + receiver_name +""",
                            <p>Thank you for Participation. We have attached the Certificate of 
                            Participation below in the email. We look forward to seeing you for next program.
                            </p>
                            Regards,
                            <br>
                            Team TRPL
                            <br>
                            <br>
                            <i> NOTE: G-Mail renders a low resolution in the preview, Download Certificate for higher resolution.
                            """, 'html'))
    filename = "Output/Certificate_TRPLWBI2022_" + receiver_name + ".pdf"

    try:
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        msg.attach(part)
    except Exception as e:
        print(f'Attachment not found.!n{e}')
        break

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        context = ssl.create_default_context()
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent to " + receiver_email)
    except Exception as e:
        print(f'Error!n{e}')
        break
    finally:
        print('Closing Server.')
        server.quit()
