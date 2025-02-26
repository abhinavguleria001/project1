from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Set the absolute path for the dataset
DATA_PATH = r"C:\Users\abhis\Downloads\flask\automobile.csv"

# Load the automobile dataset with error handling
try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    print(f"Error loading dataset: {e}")
    df = pd.DataFrame()  # Empty dataframe to prevent crashes

@app.route("/", methods=["GET", "POST"])
def home():
    results = df.to_html(classes="table table-striped table-bordered", index=False)  # Show all cars by default

    if request.method == "POST":
        search_query = request.form.get("search", "").strip().lower()
        print("Columns in the dataset:", df.columns)


        if search_query:
            # Filter dataset based on 'CarName' column (case-insensitive)
            filtered_df = df[df["make"].str.lower().str.contains(search_query, na=False)]
            if not filtered_df.empty:
                results = filtered_df.to_html(classes="table table-striped table-bordered", index=False)
            else:
                results = "<p class='text-danger'>No results found.</p>"

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)