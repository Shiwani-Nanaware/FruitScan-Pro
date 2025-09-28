from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from detection import detect
import requests
import os
import json

# changes needed here
UPLOAD_FOLDER = "C:\\Users\\mohit\\OneDrive\\Desktop\\Fruit Disease Detection\\Fruit Disease Detection\\m1\\static\\uploads"

app = Flask(__name__)
app.secret_key = "secretkeysomething"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def save_file(file):
    # file = request.files["file"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    return True

@app.route("/index", methods=["GET", "POST"])
def index():
    # if "user" in session:
    if request.method == "GET":
        # return render_template("index.html", fruit_name="", fruit_disease="", disease_description="", fruit_image="")
        return render_template("index.html")
    elif request.method == "POST":
        fileUpload = save_file(request.files["file"])
        # posting the picture and getting the fruit_disease and detection
        # response = requests.post("http://127.0.0.1:5000/model", files={"file": open(UPLOAD_FOLDER+request.files["file"].filename, "rb")})
        # response = response.json()
        detection = detect("static/uploads/"+(request.files['file'].filename).lower().replace(" ", "_"))
        # response = {"disease": detection, "description":fruit_disease_descriptions[detection]}
        # fruit_name = response["disease"].split('_')[0]
        # fruit_disease = response["disease"]
        # disease_description = response["description"]
        return redirect(f"/information/{detection}/{(request.files['file'].filename).lower().replace(' ', '_')}")
        # return render_template("index.html", fruit_name=fruit_name, fruit_disease=fruit_disease, disease_description=disease_description, fruit_image=request.files["file"].filename)
    # else:
    #     return redirect(url_for("signup"))

@app.route("/information/<string:fruit>/<string:image>")
def information(fruit, image):
    fruit_disease_descriptions = {
        "APPLE_blotch": {"disease information": "A disease affecting apple trees characterized by dark, irregular blotches on the fruit's surface.",
                        "solution": ["Apply fungicide spray according to manufacturer's instructions.", "Prune affected branches and remove infected fruit."]},
        "APPLE_normal": {"disease information": "Healthy state of apple trees without any significant diseases or abnormalities.",
                        "solution": ["Maintain proper watering and fertilization schedule.", "Monitor for pests and diseases regularly."]},
        "APPLE_rot": {"disease information": "A condition in apple fruits where decay or decomposition sets in, often caused by fungal or bacterial infection.",
                    "solution": ["Harvest fruits promptly to avoid overripening.", "Store apples in a cool, dry place with good air circulation."]},
        "APPLE_scab": {"disease information": "A common apple tree disease caused by a fungus, resulting in scaly or scabby lesions on leaves and fruit.",
                    "solution": ["Apply fungicides labeled for apple scab control.", "Prune infected branches and improve air circulation."]},
        "GUAVA_pytopthora": {"disease information": "A disease affecting guava plants caused by the Pytophthora pathogen, leading to wilting and root rot.",
                            "solution": ["Improve soil drainage to prevent waterlogging.", "Use fungicides to manage Pytophthora infections."]},
        "GUAVA_root": {"disease information": "A condition in guava plants characterized by issues in the root system, potentially leading to stunted growth or other symptoms.",
                    "solution": ["Ensure proper planting depth and soil pH for guava trees.", "Avoid overwatering to prevent root diseases."]},
        "GUAVA_scab": {"disease information": "A fungal disease affecting guava trees, causing scaly or scabby lesions on leaves and fruit similar to apple scab.",
                    "solution": ["Prune infected branches to improve air circulation.", "Apply fungicides during the growing season."]},
        "LEMON_canker": {"disease information": "A bacterial infection affecting lemon trees, resulting in raised lesions on leaves, fruit, and stems.",
                        "solution": ["Prune affected branches and remove infected plant material.", "Apply copper-based fungicides to manage canker."]},
        "LEMON_healthy": {"disease information": "Healthy state of lemon trees without any significant diseases or abnormalities.",
                        "solution": ["Provide proper nutrients and water to maintain tree health.", "Monitor for pests and diseases regularly."]},
        "LEMON_mold": {"disease information": "A condition in lemon fruits where mold growth occurs, often due to environmental factors or improper storage.",
                    "solution": ["Harvest fruits before they become overripe.", "Store lemons in a cool, dry place with good ventilation."]},
        "LEMON_scab": {"disease information": "A fungal disease affecting lemon trees, causing scaly or scabby lesions on leaves and fruit similar to apple and guava scab.",
                    "solution": ["Apply fungicides labeled for lemon scab control.", "Prune infected branches and improve air circulation."]}
    }
    response = {"disease": fruit, "description":fruit_disease_descriptions[fruit]}
    fruit_name = response["disease"].split('_')[0]
    fruit_disease = response["disease"]
    disease_description = response["description"]
    return render_template("information.html", fruit_name=fruit_name, fruit_disease=fruit_disease, disease_description=disease_description, fruit_image=image)

@app.route("/", methods=["GET", "POST"])
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        print("hahahaha")
        return render_template("signup.html", error_message=None)
    elif request.method == "POST":
        full_name = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        data = {"full name": full_name, "email": email, "password": password}
        # reading the json file
        with open("userCredentials.json", "r") as file:
            jsonFile = json.load(file)
        if email not in jsonFile:
            # adding data to the json file
            jsonFile[email] = data
            with open("userCredentials.json", "w") as file:
                json.dump(jsonFile, file, indent=4)
            # session["user"] = True
            return redirect(url_for("index"))
        else:
            return render_template("signup.html", error_message="Email already present")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", error_message=None)
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # reading the json file
        with open("userCredentials.json", "r") as file:
            jsonFile = json.load(file)
        if email in jsonFile:
            if password == jsonFile[email]["password"]:
                # session["user"] = True
                return redirect(url_for("index"))
            else:
                return render_template("login.html", error_message="Password does not match")
        else:
            return render_template("login.html", error_message="Email not registered")

if __name__ == "__main__":
    app.run(debug=True, port=5001)