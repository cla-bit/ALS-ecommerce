from django.shortcuts import render
from typing import Dict, Optional
import logging
import joblib
from pymongo import MongoClient

from django.http import JsonResponse, HttpRequest
from django.conf import settings

# Create your views here.

logger = logging.getLogger(__name__)


# Load the trained recommendation model
model = joblib.load("recommendation_model.pkl")


#TODO: Connect correctly your MongoDB connection

# Connect to MongoDB
client = MongoClient(settings.MONGO_CONNECTION_STRING)  # Replace with your MongoDB URI
db = client[settings.MONGO_DB_NAME]
collection = db[settings.MONGO_COLLECTION_NAME]  # Ensure this matches your actual collection name


def get_product_details(product_id: int) -> Optional[Dict]:
    """
    Fetch the shop name for a given item from MongoDB.

    Parameters:
    product_id (int): The unique identifier of the product.

    Returns:
    dict: A dictionary containing the product details if found, otherwise None.
          The dictionary will contain the following keys: 'ProductID', 'ProductName', 'Category', 'Price', 'Rating', 'NumReviews', 'StockQuantity', 'Discount', 'Sales', 'DateAdded'.
    """
    item = collection.find_one({"ProductID": product_id})  # You can add other arguments here 'ProductName', 'Category', 'Price', 'Rating', 'NumReviews','StockQuantity', 'Discount', 'Sales', 'DateAdded'
    return item if item else None


def get_recommendations(request: HttpRequest, product_id: int) -> JsonResponse:
    """
    Returns recommended items and their shops.

    Parameters:
    request (HttpRequest): The incoming request object.
    product_id (int): The ID of the product for which recommendations are requested.

    Returns:
    JsonResponse: A JSON response containing the recommended items. If an error occurs, it returns a JSON response with an error message and a status code of 500.
    """
    try:
        recommendations = model.similar_items(product_id, 5)  # Get top 5 similar items

        recommended_items = []
        for rec_id, _ in recommendations:
            product = get_product_details(rec_id)  # Fetch shop from MongoDB
            if product:
                recommended_items.append(product)

        return JsonResponse({"recommended_items": recommended_items})

    except Exception as e:
        logger.error(f"Error fetching recommendations: {e}")
        return JsonResponse({"error": str(e)}, status=500)

