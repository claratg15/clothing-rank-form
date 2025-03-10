import os
import random
import csv
from flask import Flask, render_template, request

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
            writer.writerow(["timestamp"] + [f"image_{i}" for i in range(1, 11)])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Save rankings to CSV
        rankings = [request.form.get(f"image_{i}") for i in range(1, 11)]
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([request.remote_addr] + rankings)
        return "Thank you for your response!"
    
    # Select 10 random images
    all_images = os.listdir(IMAGE_FOLDER)
    selected_images = random.sample(all_images, 10)
    return render_template("form.html", images=selected_images)

if __name__ == "__main__":
    init_csv()
    app.run(debug=True)
