import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from werkzeug.utils import secure_filename

# Assume 'detect' function is defined elsewhere, but for this code to run, it's commented out.
# from your_detection_module import detect

UPLOAD_FOLDER = os.path.join(os.getcwd(), "static", "uploads")
ALLOWED_EXTENSION = set(["jpg", "png", "jpeg"])

app = Flask(__name__)
api = Api(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Check if the upload folder exists, create it if not
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """
    Checks if the uploaded file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@app.route("/upload", methods=["POST"])
def upload():
    """
    Handles file upload to the server.
    """
    if 'file' not in request.files:
        return jsonify({"error": "media not provided"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "no file selected"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return jsonify({"msg": "media uploaded successfully"})
    return jsonify({"error": "file type not allowed"}), 400

get_args = reqparse.RequestParser()
get_args.add_argument("disease", type=str, help="Type of fruit disease", required=True)

class AIModel(Resource):
    def get(self):
        """
        Retrieves description for a given fruit disease.
        """
        args = get_args.parse_args()
        
        fruit_disease_descriptions = {
            "APPLE_blotch": "A disease affecting apple trees characterized by dark, irregular blotches on the fruit's surface.",
            "APPLE_normal": "Healthy state of apple trees without any significant diseases or abnormalities.",
            "APPLE_rot": "A condition in apple fruits where decay or decomposition sets in, often caused by fungal or bacterial infection.",
            "APPLE_scab": "A common apple tree disease caused by a fungus, resulting in scaly or scabby lesions on leaves and fruit.",
            "GUAVA_pytopthora": "A disease affecting guava plants caused by the Pytophthora pathogen, leading to wilting and root rot.",
            "GUAVA_root": "A condition in guava plants characterized by issues in the root system, potentially leading to stunted growth or other symptoms.",
            "GUAVA_scab": "A fungal disease affecting guava trees, causing scaly or scabby lesions on leaves and fruit similar to apple scab.",
            "LEMON_canker": "A bacterial infection affecting lemon trees, resulting in raised lesions on leaves, fruit, and stems.",
            "LEMON_healthy": "Healthy state of lemon trees without any significant diseases or abnormalities.",
            "LEMON_mold": "A condition in lemon fruits where mold growth occurs, often due to environmental factors or improper storage.",
            "LEMON_scab": "A fungal disease affecting lemon trees, causing scaly or scabby lesions on leaves and fruit similar to apple and guava scab."
        }
        
        disease_name = args["disease"]
        if disease_name in fruit_disease_descriptions:
            return {"disease": disease_name, "description": fruit_disease_descriptions[disease_name]}
        else:
            return {"error": "Disease not found"}, 404
            
    def post(self):
        """
        Handles image upload for disease detection and returns the result.
        """
        fruit_disease_descriptions = {
            "APPLE_blotch": "A disease affecting apple trees characterized by dark, irregular blotches on the fruit's surface.",
            "APPLE_normal": "Healthy state of apple trees without any significant diseases or abnormalities.",
            "APPLE_rot": "A condition in apple fruits where decay or decomposition sets in, often caused by fungal or bacterial infection.",
            "APPLE_scab": "A common apple tree disease caused by a fungus, resulting in scaly or scabby lesions on leaves and fruit.",
            "GUAVA_pytopthora": "A disease affecting guava plants caused by the Pytophthora pathogen, leading to wilting and root rot.",
            "GUAVA_root": "A condition in guava plants characterized by issues in the root system, potentially leading to stunted growth or other symptoms.",
            "GUAVA_scab": "A fungal disease affecting guava trees, causing scaly or scabby lesions on leaves and fruit similar to apple scab.",
            "LEMON_canker": "A bacterial infection affecting lemon trees, resulting in raised lesions on leaves, fruit, and stems.",
            "LEMON_healthy": "Healthy state of lemon trees without any significant diseases or abnormalities.",
            "LEMON_mold": "A condition in lemon fruits where mold growth occurs, often due to environmental factors or improper storage.",
            "LEMON_scab": "A fungal disease affecting lemon trees, causing scaly or scabby lesions on leaves and fruit similar to apple and guava scab."
        }
        
        if 'file' not in request.files:
            return {"error": "media not provided"}, 400
        file = request.files["file"]
        if file.filename == "":
            return {"error": "no file selected"}, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            
            # This is where the AI model detection would be called.
            # I'm using a placeholder for now, as the `detect` function is not provided.
            # You will need to uncomment the `detect` function import and the line below.
            # detection = detect(file_path)
            
            # Placeholder for demonstration purposes
            detection = "APPLE_scab"
            
            if detection in fruit_disease_descriptions:
                return {"disease": detection, "description": fruit_disease_descriptions[detection]}
            else:
                return {"error": "Detection failed or disease not recognized"}, 500
        return {"error": "file type not allowed"}, 400
        
api.add_resource(AIModel, "/model")

if __name__ == "__main__":
    app.run(debug=True)
