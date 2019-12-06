import base64
import sys

input_file = 'image.png'
target_file = 'image.b64'

if len(sys.argv) > 2:
	input_file = sys.argv[1]
	target_file = sys.argv[2]

encoded_string=None
with open(input_file, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())    
with open(target_file, 'w') as fout:
    fout.write(encoded_string)