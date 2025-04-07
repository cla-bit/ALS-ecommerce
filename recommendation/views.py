from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpRequest

from .models import Product
from .utility import get_recommendations


# Create your views here.

def home(request: HttpRequest):
    return render(request, 'index.html')


def recommend_products(request: HttpRequest, product_id: int):
    """
    Returns a rendered template with recommended items and their shops..

    Parameters:
    request (HttpRequest): The incoming request object.
    product_id (int): The ID of the product for which recommendations are requested.

    Returns:
    HttpResponse: A rendered template containing the recommended items.    """
    try:
        product = get_object_or_404(Product, pk=product_id)
        # Get recommended product IDs
        recommended_ids = get_recommendations(product_id, top_n=5)
        # Fetch Product instances for the recommended IDs
        recommended_products = Product.objects.filter(id__in=recommended_ids)

        context = {
            "product": product,
            "recommended_products": recommended_products
        }

        return render(request, "recommendations.html", context)
    except Exception as e:
        # Handle any errors gracefully
        return render(request, "error.html", {"error_message": str(e)})


def search_and_recommend(request: HttpRequest):
    """
    Handle the search for a product by name and provide recommended similar products.
    """
    query = request.GET.get('q', '')  # Get the search query from the GET parameter (default to empty string)

    # Search for product by name, case-insensitive match
    products = Product.objects.filter(name__icontains=query)

    if products.exists():
        # If we have search results, pick the first match
        product = products.first()

        # Get recommended product IDs
        recommended_ids = get_recommendations(product.id, top_n=5)

        # Fetch recommended products from the database
        recommended_products = Product.objects.filter(id__in=recommended_ids)

        context = {
            "product": product,
            "recommended_products": recommended_products,
            "search_query": query
        }
        return render(request, "recommendations.html", context)
    else:
        # No products found, return an empty result message
        context = {
            "error_message": f"No products found for '{query}'",
            "search_query": query
        }
        return render(request, "search_result.html", context)