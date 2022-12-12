import pytesseract, ftfy, re
from flask import jsonify
from PIL import Image

def vehicleRC_read_data(image):
    
    # Defining path to tesseract.exe and the image
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    try:
        img = Image.open(image)

        try:
            DL = []

            # Extract text from image
            text = pytesseract.image_to_string(img, lang ="eng")
            if "dl" in text.lower() or "valid till" in text.lower() or "authorisation" in text.lower() or "authorization" in text.lower():
                text = ftfy.fix_text(text)
                text = ftfy.fix_encoding(text)
        
                # Splitting the lines to sort the text paragraph wise
                lines = text.split('\n')
                for lin in lines:
                    s = lin.strip()
                    s = s.rstrip()
                    s = s.lstrip()
                    DL.append(s)
                
                for x in lines:
                    _ = x.split()
                    if ([w for w in _ if re.search("(Driving Licence|DL No|DL|Licence No|REGN)$", w)]):    
                        dl_number = x
                        #print(dl_number)
                        
                    if ([w for w in _ if re.search("(Date of Birth|DOB|D.O.B.)$", w)]):    
                        dl_dob = x.split(':')[1].strip()
                        dl_dob = dl_dob.rstrip()
                        dl_dob = dl_dob.lstrip()
                        dl_dob = dl_dob.replace('l', '/')
                        dl_dob = dl_dob.replace('L', '/')
                        dl_dob = dl_dob.replace('I', '/')
                        dl_dob = dl_dob.replace('i', '/')
                        dl_dob = dl_dob.replace('|', '/')
                        dl_dob = dl_dob.replace('\"', '/1')
                        # dl_dob = dl_dob.replace(" ", "")
                    
                dl_data = {
                'dl_data' : lines,
                'dl_number' : dl_number,
                'dl_dob' : dl_dob
                }
                
                return dl_data
            
            else:
                resp = jsonify({'status':'failed',' message':'Please provide a driving license image'})
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

