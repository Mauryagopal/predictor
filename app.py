from flask import Flask
from pages.Predict import predict_bp
from pages.Analytics import analytics_bp
from pages.Recommend import recommend_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(predict_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(recommend_bp)

if __name__ == "__main__":
    app.run(debug=True)
