import os, time
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from ocr_aadhar import aadhar_read_data
from ocr_dl import vehicleRC_read_data
from ocr_pan import pan_read_data

ALLOWED_EXTENSIONS = set(['pdf','png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def help():
    return {"data":95, "val":25}

def aadhar():
    if 'file' not in request.files:
        resp = jsonify({'status':'failed',' message':'No file part in the request'})
        resp.status_code = 400
        return resp
    
    file = request.files['file']
    
    if file.filename == '':
        resp = jsonify({'status':'failed', 'message':'No file selected for uploading'})
        resp.status_code = 400
        return resp
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        
        file.save(os.path.join('/tmp/', filename))
        os.rename('/tmp/'+filename, '/tmp/'+timestr+".png")
        resp = jsonify({'status':'success', 'message' : 'File successfully uploaded'})
        resp.status_code = 201
        aadhar_data = aadhar_read_data(file)
        return aadhar_data
    
    else:
        resp = jsonify({'status':'failed', 'message' : 'Allowed file types are png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

def pan():
    
    if 'file' not in request.files:
        resp = jsonify({'status':'failed', 'status':'failed', 'message':'No file part in the request'})
        resp.status_code = 400
        return resp
    
    file = request.files['file']
    
    if file.filename == '':
        resp = jsonify({'status':'failed', 'message':'No file selected for uploading'})
        resp.status_code = 400
        return resp
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        
        file.save(os.path.join('/tmp/', filename))
        os.rename('/tmp/'+filename, '/tmp/'+timestr+".png")
        resp = jsonify({'status':'success', 'message' : 'File successfully uploaded'})
        resp.status_code = 201
        aadhar_data = pan_read_data(file)
        return aadhar_data
    
    else:
        resp = jsonify({'status':'failed', 'message' : 'Allowed file types are png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

def dlic():
    
    if 'file' not in request.files:
        resp = jsonify({'message':'No file part in the request'})
        resp.status_code = 400
        return resp
    
    file = request.files['file']
    
    if file.filename == '':
        resp = jsonify({'status':'failed', 'message':'No file selected for uploading'})
        resp.status_code = 400
        return resp
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        
        file.save(os.path.join('/tmp/', filename))
        os.rename('/tmp/'+filename, '/tmp/'+timestr+".png")
        resp = jsonify({'status':'success', 'message' : 'File successfully uploaded'})
        resp.status_code = 201
        aadhar_data = vehicleRC_read_data(file)
        return aadhar_data
    
    else:
        resp = jsonify({'status':'failed', 'message' : 'Allowed file types are png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp
