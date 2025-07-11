from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

# Load the trained model and dataset
model = pickle.load(open("pipeline.pkl", "rb"))
df = pickle.load(open("df.pkl", "rb"))

# Define dropdown options
sectors = sorted([
    'dwarka expressway', 'gwal pahari', 'manesar', 'sector 1', 'sector 10', 'sector 102',
    'sector 103', 'sector 104', 'sector 105', 'sector 106', 'sector 107', 'sector 108', 'sector 109',
    'sector 11', 'sector 110', 'sector 111', 'sector 112', 'sector 113', 'sector 12', 'sector 13',
    'sector 14', 'sector 15', 'sector 17', 'sector 2', 'sector 21', 'sector 22', 'sector 23',
    'sector 24', 'sector 25', 'sector 26', 'sector 27', 'sector 28', 'sector 3', 'sector 30',
    'sector 31', 'sector 33', 'sector 36', 'sector 37', 'sector 37d', 'sector 38', 'sector 39',
    'sector 4', 'sector 40', 'sector 41', 'sector 43', 'sector 45', 'sector 46', 'sector 47',
    'sector 48', 'sector 49', 'sector 5', 'sector 50', 'sector 51', 'sector 52', 'sector 53',
    'sector 54', 'sector 55', 'sector 56', 'sector 57', 'sector 58', 'sector 59', 'sector 6',
    'sector 60', 'sector 61', 'sector 62', 'sector 63', 'sector 63a', 'sector 65', 'sector 66',
    'sector 67', 'sector 67a', 'sector 68', 'sector 69', 'sector 7', 'sector 70', 'sector 70a',
    'sector 71', 'sector 72', 'sector 73', 'sector 74', 'sector 76', 'sector 77', 'sector 78',
    'sector 79', 'sector 8', 'sector 80', 'sector 81', 'sector 82', 'sector 82a', 'sector 83',
    'sector 84', 'sector 85', 'sector 86', 'sector 88', 'sector 88a', 'sector 89', 'sector 9',
    'sector 90', 'sector 91', 'sector 92', 'sector 93', 'sector 95', 'sector 99', 'sohna road'
])

# Dynamic dropdowns from df
property_types = df['property_type'].unique()
balconies = sorted(df['balcony'].unique())
age_possessions = df['agePossession'].unique()
furnishing_types = df['furnishing_type'].unique()
luxury_categories = df['luxury_category'].unique()
floor_categories = df['floor_category'].unique()

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        try:
            # Extract data from form
            data = {
                'property_type': request.form.get('property_type'),
                'sector': request.form.get('sector'),
                'bedRoom': float(request.form.get('bedRoom')),
                'bathroom': float(request.form.get('bathroom')),
                'balcony': request.form.get('balcony'),
                'agePossession': request.form.get('agePossession'),
                'built_up_area': float(request.form.get('built_up_area')),
                'servant room': float(request.form.get('servant_room')),
                'store room': float(request.form.get('store_room')),
                'furnishing_type': request.form.get('furnishing_type'),
                'luxury_category': request.form.get('luxury_category'),
                'floor_category': request.form.get('floor_category'),
            }

            # Convert to DataFrame
            input_df = pd.DataFrame([data])

            # Predict log price and convert back
            pred_log_price = model.predict(input_df)[0]
            prediction = round(np.expm1(pred_log_price), 2)

        except Exception as e:
            prediction = f"Error: {e}"

    return render_template("index.html",
                           sectors=sectors,
                           property_types=property_types,
                           balconies=balconies,
                           age_possessions=age_possessions,
                           furnishing_types=furnishing_types,
                           luxury_categories=luxury_categories,
                           floor_categories=floor_categories,
                           prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
