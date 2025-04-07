# products/utility.py
import pickle
import os

from django.conf import settings


# Load the model when the module is imported
model_path = os.path.join(settings.BASE_DIR, 'resources/recommendation_model.pkl')

try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    model = None
    print("Warning: Recommendation model not found at", model_path)
except Exception as e:
    print(f"Error loading recommendation model: {e}")


def get_recommendations(product_id: int, top_n: int = 5):
    """
    Get similar products using the recommendation model
    """
    if model is None:
        print("Recommendation model not loaded")
        return []

    try:
        # Assuming the model has a 'similar_items' method that takes product name and returns similar products
        similar_items, scores = model.similar_items(product_id, top_n)
        # Convert indices to product names - this part depends on how your model works
        # You might need to adjust this based on your actual model implementation
        recommended_ids = [int(item) for item in similar_items]
        return recommended_ids
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return []
