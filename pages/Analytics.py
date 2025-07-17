from flask import Blueprint, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio
from wordcloud import WordCloud
import pickle

analytics_bp = Blueprint('analytics', __name__)

# Load data and sectors
df = pd.read_pickle("pickel_file/df.pkl")  # FIXED path
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

# Load sector features
try:
    with open("sector_features.pkl", "rb") as f:
        sector_feature_dict = pickle.load(f)
except:
    sector_feature_dict = {}

@analytics_bp.route("/info", methods=['GET', 'POST'])
def info():
    try:
        df_viz = pd.read_csv("Dataset/data_viz1.csv")  # FIXED path
        for col in ['price', 'price_per_sqft', 'built_up_area']:
            df_viz[col] = pd.to_numeric(df_viz[col], errors='coerce')

        group_df = df_viz.groupby('sector', as_index=False)[
            ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
        ].mean().dropna()

        fig = px.scatter_mapbox(
            group_df,
            lat="latitude",
            lon="longitude",
            color="price_per_sqft",
            size="built_up_area",
            color_continuous_scale=px.colors.cyclical.IceFire,
            zoom=10,
            mapbox_style="open-street-map",
            width=1000,
            height=600,
            hover_name="sector"
        )

        plot_html = pio.to_html(fig, full_html=False)

        selected_sector = request.form.get('sector')
        wordcloud_img_path = None
        message = None

        if selected_sector:
            features = sector_feature_dict.get(selected_sector, [])
            feature_text = " ".join(features)

            if feature_text.strip():
                wordcloud = WordCloud(
                    width=800,
                    height=600,
                    background_color='white',
                    stopwords=set(['s']),
                    min_font_size=10
                ).generate(feature_text)

                img_filename = f"static/{selected_sector.replace(' ', '_')}_wordcloud.png"
                wordcloud.to_file(img_filename)
                wordcloud_img_path = img_filename
            else:
                message = f"No features found for {selected_sector.title()} to generate a word cloud."

        return render_template(
            "info.html",
            plot_html=plot_html,
            sectors=sectors,
            selected_sector=selected_sector,
            wordcloud_img_path=wordcloud_img_path,
            message=message
        )
    except Exception as e:
        return f"Error rendering /info: {e}"
