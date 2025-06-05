from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle
import os

app = Flask(__name__)

# Load model and features
with open("best_rf.pkl", "rb") as f:
    best_rf = pickle.load(f)

with open("feature_cols.pkl", "rb") as f:
    feature_cols = pickle.load(f)

# Load original DataFrame just for medians
df = pd.read_excel("CodeCraft ML Competition Dataset.xlsx", sheet_name="Sheet1")
for col in ['Votes', 'Reviews', 'Delivery_Time']:
    df[col] = pd.to_numeric(df[col].astype(str).str.extract(r'(\d+)')[0], errors='coerce')
median_votes = df['Votes'].median()
median_reviews = df['Reviews'].median()
median_delivery = df['Delivery_Time'].median()

# 🔥 Serve homepage
@app.route("/")
def index():
    return render_template("index.html")

# 🔮 Prediction API
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    city = data.get("city", "").strip()
    cuisine_input = data.get("cuisine", "").split(",")
    rating = float(data.get("rating", 0))

    X_new = pd.DataFrame(0, index=[0], columns=feature_cols)
    X_new.at[0, "Rating"] = rating
    X_new.at[0, "Votes"] = median_votes
    X_new.at[0, "Reviews"] = median_reviews
    X_new.at[0, "Delivery_Time"] = median_delivery

    if f"City_{city}" in feature_cols:
        X_new.at[0, f"City_{city}"] = 1

    for c in [c.strip() for c in cuisine_input]:
        if f"Cuisine_{c}" in feature_cols:
            X_new.at[0, f"Cuisine_{c}"] = 1

    pred_price = best_rf.predict(X_new)[0]
    return jsonify({"predicted_price": round(float(pred_price), 2)})

if __name__ == "__main__":
    app.run(debug=True)
