import os
import random
import csv
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# Folder where images are stored
IMAGE_FOLDER = "static/images"  # Put your images inside a "static/images" folder

# File to store responses
CSV_FILE = "responses.csv"

# Ensure CSV file exists
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp"] + [f"image_{i}" for i in range(1, 11)] + [f"rank_{i}" for i in range(1, 11)])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the filenames of the images shown
        image_filenames = request.form.getlist("image_filenames")

        # Save rankings to CSV
        rankings = [request.form.get(f"image_{i}") for i in range(1, 11)]
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([request.remote_addr] + image_filenames + rankings)
        return "Moltes gràcies per la teva resposta!"
    
    # Select 10 random images
    all_images = os.listdir(IMAGE_FOLDER)
    selected_images = random.sample(all_images, 10)
    return render_template("form.html", images=selected_images, image_filenames=selected_images)

@app.route('/download')
def download():
    # Send the CSV file as a download
    return send_from_directory(directory=os.getcwd(), filename=CSV_FILE)

if __name__ == "__main__":
    init_csv()
    app.run(debug=True)
