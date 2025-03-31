# Guided steps to integrate the *recommendation model* in a Django ecommerce application.

----

1. Clone the application from github.
2. Setup and activate your virtual environment.
3. Go into the project directory [ecommerce] and pip install the dependencies.
4. Setup your MongoDB database, if you already have MongoDB installed.
5. Go into the project directory [ecommerce] >> settings.py, and connect your database settings to your MongoDB database.
    > If you are using "djongo". ensure you pip install the library, the setup is there.

    > If you are using NoSQL to use pymongo directly the setup is there.

    > There is a provided dummy csv file that contains ecommerce products, which you can migrate into your MongoDB database.

6. Go into the project directory [ecommerce] >> settings.py, and setup your templates.
7. Run the *makemigrations* and *migrate* command to fill up your database.
8. For the UI, ensure you setup correctly the url in the template. See how to insert urls in django templates.

    >> You can add this one in the javascript file (optional).
    ```javascript
   // Fetch Recommendations when users make a purchase
   
   function fetchRecommendations(itemId) {
    fetch(`/recommendations/${itemId}/`)
    .then(response => response.json())
    .then(data => {
        let recommendationsDiv = document.getElementById("recommendations");
        recommendationsDiv.innerHTML = "<h3>Recommended Items</h3>";

        data.recommended_items.forEach(item => {
            recommendationsDiv.innerHTML += `<p>Item ID: ${item.item_id} (Shop: ${item.shop})</p>`;
        });
    })
    .catch(error => console.error("Error fetching recommendations:", error));
}
    ```

    ```html
    <button onclick="fetchRecommendations(1)">Get Recommendations</button>
    <div id="recommendations"></div>
    ```


8. Run the application to start up the app on your web browser.
9. Test the server and the recommendation url "recommendations/product_id".

>   **Provided also are the following**: ecommerce_product_dataset.csv, ecommerce_recommendation_model.ipynb, ecommerce_recommendation_model.py & recommendation_model.pkl
