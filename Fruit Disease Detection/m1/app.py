import os
import json
from flask import (
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    session
)
from werkzeug.utils import secure_filename

# NOTE: The 'detect' function is a placeholder. You need to implement or import 
# your actual machine learning model detection logic here.
def detect(image_path):
    """
    Placeholder for the AI model detection function.
    Returns a sample fruit disease string.
    """
    # This is a mock function. Replace with your actual model's prediction.
    return "APPLE_scab"

UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "uploads")

app = Flask(__name__)
app.secret_key = "secretkeysomething"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Check if the upload folder exists, create it if not
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ---------- File Upload & Detection ----------
def save_file(file):
    """Saves an uploaded file and returns its sanitized filename."""
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)
    return filename

@app.route("/index", methods=["GET", "POST"])
def index():
    """Handles the main application page and image upload."""
    # Check if the user is logged in
    if 'email' not in session:
        return redirect(url_for('login'))
    
    if request.method == "GET":
        return render_template("index.html")
    
    elif request.method == "POST":
        if 'file' not in request.files or request.files['file'].filename == '':
            # Handle case where no file is selected
            # You might want to display an error on the index.html page
            return redirect(url_for('index'))
            
        uploaded_file = request.files["file"]
        # Save the file and get the clean filename
        filename = save_file(uploaded_file)
        
        # Call the placeholder detection function
        detection_result = detect(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        
        # Redirect to the information page with the results
        return redirect(f"/information/{detection_result}/{filename}")

# ---------- Disease Information ----------
@app.route("/information/<string:fruit>/<string:image>")
def information(fruit, image):
    """Displays information and solutions for a detected disease."""
    fruit_disease_descriptions = {
        "APPLE_blotch": {"disease information": "A disease affecting apple trees characterized by dark, irregular blotches on the fruit's surface.", "solution": ["Apply fungicide spray according to manufacturer's instructions.", "Prune affected branches and remove infected fruit."]},
        "APPLE_normal": {"disease information": "Healthy state of apple trees without any significant diseases or abnormalities.", "solution": ["Maintain proper watering and fertilization schedule.", "Monitor for pests and diseases regularly."]},
        "APPLE_rot": {"disease information": "A condition in apple fruits where decay or decomposition sets in, often caused by fungal or bacterial infection.", "solution": ["Harvest fruits promptly to avoid overripening.", "Store apples in a cool, dry place with good air circulation."]},
        "APPLE_scab": {"disease information": "A common apple tree disease caused by a fungus, resulting in scaly or scabby lesions on leaves and fruit.", "solution": ["Apply fungicides labeled for apple scab control.", "Prune infected branches and improve air circulation."]},
        "GUAVA_pytopthora": {"disease information": "A disease affecting guava plants caused by the Pytophthora pathogen, leading to wilting and root rot.", "solution": ["Improve soil drainage to prevent waterlogging.", "Use fungicides to manage Pytophthora infections."]},
        "GUAVA_root": {"disease information": "A condition in guava plants characterized by issues in the root system, potentially leading to stunted growth or other symptoms.", "solution": ["Ensure proper planting depth and soil pH for guava trees.", "Avoid overwatering to prevent root diseases."]},
        "GUAVA_scab": {"disease information": "A fungal disease affecting guava trees, causing scaly or scabby lesions on leaves and fruit similar to apple scab.", "solution": ["Prune infected branches to improve air circulation.", "Apply fungicides during the growing season."]},
        "LEMON_canker": {"disease information": "A bacterial infection affecting lemon trees, resulting in raised lesions on leaves, fruit, and stems.", "solution": ["Prune affected branches and remove infected plant material.", "Apply copper-based fungicides to manage canker."]},
        "LEMON_healthy": {"disease information": "Healthy state of lemon trees without any significant diseases or abnormalities.", "solution": ["Provide proper nutrients and water to maintain tree health.", "Monitor for pests and diseases regularly."]},
        "LEMON_mold": {"disease information": "A condition in lemon fruits where mold growth occurs, often due to environmental factors or improper storage.", "solution": ["Harvest fruits before they become overripe.", "Store lemons in a cool, dry place with good ventilation."]},
        "LEMON_scab": {"disease information": "A fungal disease affecting lemon trees, causing scaly or scabby lesions on leaves and fruit similar to apple and guava scab.", "solution": ["Apply fungicides labeled for lemon scab control.", "Prune infected branches and improve air circulation."]}
    }
    
    # Get the disease and description, defaulting to an empty dict if not found
    description = fruit_disease_descriptions.get(fruit, {})
    fruit_name = fruit.split('_')[0]
    
    return render_template("information.html", 
                           fruit_name=fruit_name, 
                           fruit_disease=fruit, 
                           disease_description=description, 
                           fruit_image=image)

# ---------- Signup ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handles user registration."""
    if request.method == "GET":
        return render_template("signup.html", error_message=None)
    elif request.method == "POST":
        full_name = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        data = {"full name": full_name, "email": email, "password": password}

        # Reading the json file
        try:
            with open("userCredentials.json", "r") as file:
                jsonFile = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            jsonFile = {}

        if email not in jsonFile:
            # Adding data to the json file
            jsonFile[email] = data
            with open("userCredentials.json", "w") as file:
                json.dump(jsonFile, file, indent=4)
            session['email'] = email
            return redirect(url_for("index"))
        else:
            return render_template("signup.html", error_message="Email already present")

# ---------- Login ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles user login."""
    if request.method == "GET":
        return render_template("login.html", error_message=None)
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Reading the json file
        try:
            with open("userCredentials.json", "r") as file:
                jsonFile = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            jsonFile = {}

        if email in jsonFile:
            if password == jsonFile[email]["password"]:
                session['email'] = email
                return redirect(url_for('index'))
            else:
                return render_template("login.html", error_message="Password does not match")
        else:
            return render_template("login.html", error_message="Email not registered")

# ---------- Logout ----------
@app.route("/logout")
def logout():
    """Logs the user out and redirects to the login page."""
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('home.html')

# ---------- General Pages ----------
@app.route('/')
def home():
    """Redirects to the index page if a user is logged in, otherwise to login."""
    if 'email' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Here you can add email sending functionality
        # For now, we'll just print the message
        print(f"Contact form submission from {name} ({email}): {message}")

        # You can add email sending logic here
        # Example: send_email(name, email, message)

        return render_template('contact.html', success=True)

    return render_template('contact.html')


@app.route('/enroll')
def enroll():
    course_name = request.args.get('course', 'Unknown Course')
    return render_template('enroll.html', course_name=course_name)

@app.route('/submit_enrollment', methods=['POST'])
def submit_enrollment():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    phone = request.form.get('phone')
    education = request.form.get('education')
    message = request.form.get('message')
    course = request.form.get('course')
    
    print(f"Enrollment received for {course} from {fullname} ({email}, {phone})")
    
    return render_template('thank_you.html', name=fullname, course=course)

# ---------- Run App ----------
if __name__ == "__main__":
    app.run(debug=True, port=5001)
