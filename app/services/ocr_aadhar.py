import pytesseract, re
from flask import jsonify
from PIL import Image

def aadhar_read_data(image):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"    

    # validity of input image
    try:
        img = Image.open(image)
    
    # test for image readability
        try:
            text = pytesseract.image_to_string(img, lang ="eng")

            # classification of uniqueness of the addhar card
            if "male" in text.lower():
                res = text.split()
                name, dob, adh, sex = None, None, None, None
                text0, text1 = [], []
                lines = text.split('\n')
                for lin in lines: s = lin. strip(); s = lin.replace('\n',''); s = s.rstrip(); s = s.lstrip(); text1.append(s)
                
                if 'female' in text.lower(): sex='FEMALE'
                else: sex='MALE'

                text1 = list(filter(None, text1))
                text0 = text1[:]

                try:
                    # Cleaning first names
                    name = text0[0]
                    name = name.rstrip()
                    name = name.lstrip()
                    name = name.replace("8", "B")
                    name = name.replace("0", "D")
                    name = name.replace("6", "G")
                    name = name.replace("1", "I")
                    name = re.sub('[^a-zA-Z] +', ' ', name)

                    # Cleaning DOB
                    dob = text0[1][-10:]
                    dob = dob.rstrip()
                    dob = dob.lstrip()
                    dob = dob.replace('l', '/')
                    dob = dob.replace('L', '/')
                    dob = dob.replace('I', '/')
                    dob = dob.replace('i', '/')
                    dob = dob.replace('|', '/')
                    dob = dob.replace('\"', '/1')
                    dob = dob.replace(":","")
                    dob = dob.replace(" ", "")
                
                    # Cleaning Aadhaar number details
                    aadhar_number=''
                    for word in res:
                        if len(word) == 4 and word.isdigit():
                            aadhar_number=aadhar_number  + word + ' '
                    if len(aadhar_number)>=12:
                        adh = aadhar_number

                except:
                    pass
                
                data = {
                    'ad_data' : lines,
                    'ad_number': adh,
                    'ad_name': name,
                    'ad_dob': dob,
                    'ad_sex': sex
                }

                return data
            
            else:
                resp = jsonify({'status':'failed',' message':'Please provide an aadhar card image'})
                resp.status_code = 400
                return resp

        except:
            resp = jsonify({'status':'failed',' message':'Image is not readable'})
            resp.status_code = 400
            return resp

    except:
        resp = jsonify({'status':'failed',' message':'Invalid image'})
        resp.status_code = 400
        return resp