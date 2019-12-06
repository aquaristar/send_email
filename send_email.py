import base64
import sys, os
import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

if len(sys.argv) < 2:
	print "usage: python send_email.py <from> [file] [image] [debug]"
	exit()

debug = False
host = "email"
image_file = None
attach_file = None
s = None

from_address = sys.argv[1]
if len(sys.argv) == 3:
	attach_file = sys.argv[2]

if len(sys.argv) == 4:
	attach_file = sys.argv[2]
	image_file = sys.argv[3]

if len(sys.argv) == 5:
	attach_file = sys.argv[2]
	image_file = sys.argv[3]
	debug = sys.argv[4]

os.environ["mail.smtp.host"] = host

to_address = raw_input();
subject = raw_input();
inputHTML = raw_input();
inputHTML = inputHTML.replace("\\\\n", "<br>")
inputHTML = inputHTML.replace("\\n", "<br>")
inputHTML = inputHTML.replace("\n", "<br>")

msgRoot = MIMEMultipart('related')
msgRoot['From']=from_address
msgRoot['To']=to_address
msgRoot['Subject']=subject
msgRoot.preamble = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

imgText = '<img src="cid:image1">'
if('{{image}}' in inputHTML):
	inputHTML = inputHTML.replace('{{image}}', imgText)
else:
	if(image_file):
		inputHTML = '<pre>' + inputHTML + '</pre>' + imgText
	else:
		inputHTML = '<pre>' + inputHTML + '</pre>'

msgText = MIMEText(inputHTML, 'html')
msgAlternative.attach(msgText)

if(image_file):
	with open(image_file, 'rb') as fp:
		msgImage = MIMEImage(fp.read())
		fp.close()
		msgImage.add_header('Content-ID', '<image1>')
		msgRoot.attach(msgImage)

if(attach_file):
	# Open PDF file in binary mode
	with open(attach_file, "rb") as attachment:
	    # Add file as application/octet-stream
	    # Email client can usually download this automatically as attachment
	    part = MIMEBase("application", "octet-stream")
	    part.set_payload(attachment.read())

	# Encode file in ASCII characters to send by email    
	encoders.encode_base64(part)

	# Add header as key/value pair to attachment part
	path, attach_filename = os.path.split(attach_file)
	print attach_filename
	part.add_header(
	    "Content-Disposition",
	    "attachment; filename=%s" % attach_filename,
	)
	msgRoot.attach(part)

if(debug):
	print msgRoot.as_string()
	s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
	s.starttls()
	s.login(from_address, 'arirangA123')
else:
	s = smtplib.SMTP(host)

s.sendmail(from_address, to_address.split(','), msgRoot.as_string())

del msgRoot

s.quit()
