# import os
# from flask import Blueprint, request, redirect, url_for, flash
# from werkzeug.utils import secure_filename
# from models import db, File
# from flask import send_from_directory,session

# file_bp = Blueprint('file_bp', __name__)

# UPLOAD_FOLDER = 'uploads/'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt'}  # You can adjust the allowed extensions

# file_bp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @file_bp.route("/upload", methods=["POST"])
# def upload_file():
#     if 'file' not in request.files:
#         flash('No file part', 'error')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No selected file', 'error')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(file_bp.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)

#         # Save file information in the database
#         new_file = File(filename=filename, filepath=filepath, user_id=session.get('user')['id'])
#         db.session.add(new_file)
#         db.session.commit()

#         flash('File successfully uploaded', 'success')
#         return redirect(url_for('dashboard_bp.user_dashboard'))
#     else:
#         flash('Invalid file type', 'error')
#         return redirect(request.url)
    

# @file_bp.route("/download/<int:file_id>")
# def download_file(file_id):
#     file = File.query.get(file_id)
#     if file:
#         return send_from_directory(directory=os.path.dirname(file.filepath), filename=file.filename)
#     flash("File not found", "error")
#     return redirect(url_for("dashboard_bp.user_dashboard"))
