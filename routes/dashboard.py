from flask import Blueprint, render_template, session, redirect, url_for, request, flash, send_from_directory
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from models import db, File
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

dashboard_bp = Blueprint("dashboard_bp", __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif","docx"}
SECRET_KEY = b'ThisIsA32ByteSecretKeyForAES!!12'  # ✅ 32 bytes


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def encrypt_file(data):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC)
    padded_data = pad(data, AES.block_size)  # ✅ Ensure data is padded to 16-byte boundary
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(cipher.iv + encrypted_data)



def decrypt_file(encrypted_data):
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data[AES.block_size:])
    return unpad(decrypted_data, AES.block_size)  # ✅ Remove padding after decryption


# @dashboard_bp.route("/admin")
# def admin_dashboard():
#     user = session.get("user")
#     if not user or user["role"] != "admin":  
#         return redirect(url_for("auth_bp.login"))
#     return render_template("admin_dashboard.html")

@dashboard_bp.route("/admin")
def admin_dashboard():
    user = session.get("user")
    
    if not user or user["role"] != "admin":
        return redirect(url_for("auth_bp.login"))

    users = user.query.all()  # Fetch all users
    files = File.query.all()  # Fetch all files

    print("Users:", users)  # Debugging: Check if users exist
    print("Files:", files)  # Debugging: Check if files exist

    return render_template("admin_dashboard.html", users=users, files=files)


# @dashboard_bp.route("/user", methods=["GET", "POST"])
# def user_dashboard():
#     user = session.get("user")
    
#     if not user or 'id' not in user:  
#         return redirect(url_for('auth_bp.login'))  

#     if request.method == "POST":
#         if "file" not in request.files:
#             flash("No file part", "error")
#             return redirect(request.url)

#         file = request.files["file"]
        
#         if file.filename == "":
#             flash("No selected file", "error")
#             return redirect(request.url)

#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(UPLOAD_FOLDER, filename)
#             encrypted_data = encrypt_file(file.read())
#             with open(file_path, "wb") as f:
#                 f.write(encrypted_data)

#             # ✅ Store file details in the database
#             new_file = File(filename=filename, filepath=file_path, user_id=user['id'])
#             db.session.add(new_file)
#             db.session.commit()

#             flash("File uploaded and encrypted successfully!", "success")

#     # ✅ Fetch files uploaded by the user
#     user_files = File.query.filter_by(user_id=user['id']).all()
    
#     return render_template("user_dashboard.html", files=user_files)

@dashboard_bp.route("/guest")
def guest_dashboard():
    user = session.get("user")
    if not user or user["role"] != "guest":  
        return redirect(url_for("auth_bp.login"))
    return render_template("guest_dashboard.html")

@dashboard_bp.route("/download/<filename>")
def download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        flash("File not found!", "error")
        return redirect(url_for("dashboard_bp.user_dashboard"))
    
    with open(file_path, "rb") as f:
        decrypted_data = decrypt_file(f.read())
    
    temp_path = os.path.join(UPLOAD_FOLDER, "decrypted_" + filename)
    with open(temp_path, "wb") as f:
        f.write(decrypted_data)
    
    return send_from_directory(UPLOAD_FOLDER, "decrypted_" + filename, as_attachment=True)

@dashboard_bp.route("/delete/<int:file_id>", methods=["POST"])
def delete_file(file_id):
    user = session.get("user")
    if not user or 'id' not in user:
        return redirect(url_for("auth_bp.login"))

    file = File.query.filter_by(id=file_id, user_id=user['id']).first()
    if file:
        file_path = file.filepath  
        if os.path.exists(file_path):
            os.remove(file_path)  # Delete from uploads folder
        db.session.delete(file)  # Delete from database
        db.session.commit()
        flash("File deleted successfully!", "success")
    else:
        flash("File not found or you don't have permission!", "error")

    return redirect(url_for("dashboard_bp.user_dashboard"))


@dashboard_bp.route("/user", methods=["GET", "POST"])
def user_dashboard():
    user = session.get("user")

    if not user or 'id' not in user:  
        return redirect(url_for('auth_bp.login'))  

    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part", "error")
            return redirect(request.url)

        file = request.files["file"]
        
        if file.filename == "":
            flash("No selected file", "error")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            encrypted_data = encrypt_file(file.read())
            with open(file_path, "wb") as f:
                f.write(encrypted_data)

            #access_type = request.form.get("access_type", "private")  # ✅ Get access type

            new_file = File(filename=filename, filepath=file_path, user_id=user['id'])
            db.session.add(new_file)
            db.session.commit()

            flash("File uploaded and encrypted successfully!", "success")

    user_files = File.query.filter_by(user_id=user['id']).all()
    
    return render_template("user_dashboard.html", user=user, files=user_files)  # ✅ Pass user to template
