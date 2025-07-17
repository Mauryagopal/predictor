from flask import Blueprint, render_template, request
import pandas as pd
import pickle
import os

# Define Blueprint with proper url_prefix and template path
recommend_bp = Blueprint("recommend", __name__, url_prefix="/recommend", template_folder="../templates")

# Set base directory for loading pickles
# Base directory where this file (e.g., Recommend.py) is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Go one level up, then into pickel_file/
PICKLE_DIR = os.path.join(BASE_DIR, "..", "pickel_file")

# Load pickle files
try:
    cosine_sim1 = pickle.load(open(os.path.join(PICKLE_DIR, "cosine_sim1.pkl"), "rb"))
    cosine_sim2 = pickle.load(open(os.path.join(PICKLE_DIR, "cosine_sim2.pkl"), "rb"))
    cosine_sim3 = pickle.load(open(os.path.join(PICKLE_DIR, "cosine_sim3.pkl"), "rb"))
    location_df_normalized = pickle.load(open(os.path.join(PICKLE_DIR, "location_df.pkl"), "rb"))
except Exception as e:
    raise RuntimeError(f"❌ Failed to load recommendation data: {e}")

# Recommendation logic
def recommend_properties_with_scores(property_name, top_n=5):
    try:
        if property_name not in location_df_normalized.index:
            return pd.DataFrame(columns=["PropertyName", "SimilarityScore"])

        # Weighted sum of similarity matrices
        cosine_sim_matrix = 30 * cosine_sim1 + 20 * cosine_sim2 + 8 * cosine_sim3
        idx = location_df_normalized.index.get_loc(property_name)
        sim_scores = list(enumerate(cosine_sim_matrix[idx]))
        sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
        top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
        top_properties = location_df_normalized.index[top_indices].tolist()

        return pd.DataFrame({
            "PropertyName": top_properties,
            "SimilarityScore": top_scores
        })
    except Exception as e:
        print(f"Error in recommendation logic: {e}")
        return pd.DataFrame(columns=["PropertyName", "SimilarityScore"])

# Flask route
@recommend_bp.route("/", methods=["GET", "POST"])
def recommend():
    try:
        selected_property = None
        results_df = None

        if request.method == "POST":
            selected_property = request.form.get("property_name")
            if selected_property:
                results_df = recommend_properties_with_scores(selected_property)

        return render_template(
            "recommend.html",
            property_names=location_df_normalized.index.tolist(),
            selected_property=selected_property,
            results_df=results_df
        )

    except Exception as e:
        return f"Error rendering /recommend: {e}"
