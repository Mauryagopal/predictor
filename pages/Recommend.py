from flask import Blueprint, render_template, request
import pandas as pd
import pickle

recommend_bp = Blueprint("recommend", __name__, template_folder="../templates")

# Safe loading of required files
try:
    cosine_sim1 = pickle.load(open("cosine_sim1.pkl", "rb"))
    cosine_sim2 = pickle.load(open("cosine_sim2.pkl", "rb"))
    cosine_sim3 = pickle.load(open("cosine_sim3.pkl", "rb"))
    location_df_normalized = pickle.load(open("location_df.pkl", "rb"))
except Exception as e:
    raise RuntimeError(f"Failed to load recommendation data: {e}")

# Recommendation logic
def recommend_properties_with_scores(property_name, top_n=20):
    try:
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
        return pd.DataFrame(columns=["PropertyName", "SimilarityScore"])

# Route to render recommendation UI
@recommend_bp.route("/recommend", methods=["GET", "POST"])
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
