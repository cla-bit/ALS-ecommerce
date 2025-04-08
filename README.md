# Guided steps to integrate the *recommendation model* in a Django ecommerce application.

----

1. Clone the application from github.
2. Setup and activate your virtual environment.
3. Go into the project directory [ecommerce] and pip install the dependencies. Run `pip install -r requirements.txt`.
4. Setup your MongoDB database, if you already have MongoDB installed or any database of your choice.
5. Go into the project directory [ecommerce] >> settings.py, and connect your database settings to your MongoDB database or database of your choice.
    > If you are using "djongo". ensure you pip install the library, the setup is there.

    > If you are using NoSQL to use pymongo directly the setup is there.

    > There is a provided dummy csv file that contains ecommerce products, which you can migrate into your MongoDB database.

6. Go into the project directory [ecommerce] >> settings.py, and setup your templates. This has been done. Skip.
7. Run the *makemigrations* and *migrate* command to fill up your database.
Run these commands:
```bash
python manage.py makemigrations
python manage.py migrate

```
8. (Optional) For the UI, ensure you setup correctly the url in the template. See how to insert urls in django templates.

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

9. Run the `import_products.py` script `python manage.py import_products`
10. Run the application to start up the app on your web browser. Run this command: `python manage.py runserver`.
11. Open the server url on your browser and test.

>   **Provided also are the following**: ecommerce_product_dataset.csv, ecommerce_recommendation_model.ipynb, ecommerce_recommendation_model.py & recommendation_model.pkl



---

# Alternating Least Squares (ALS) Algorithm for Recommendation Systems

### Overview of ALS Algorithm:
The **Alternating Least Squares (ALS)** algorithm is a matrix factorization method often used for building recommendation systems. It is particularly useful for collaborative filtering problems where the task is to predict missing values in a user-item interaction matrix, such as recommending products, movies, or music.

### Matrix Factorization:
ALS decomposes the user-item interaction matrix \( R \) into two smaller matrices:
- **User matrix** \( U \) of size \( m \times k \), where \( m \) is the number of users and \( k \) is the number of latent factors.
- **Item matrix** \( I \) of size \( n \times k \), where \( n \) is the number of items and \( k \) is the number of latent factors.

The objective is to approximate the original matrix \( R \) as the product of these two matrices:

\[
R \approx U \times I^T
\]

Where:
- \( R \) is the matrix of ratings or interactions (e.g., purchases, likes, ratings).
- \( U \) and \( I \) are learned latent feature matrices that explain the interactions.

### Alternating Optimization:
The "alternating" in **Alternating Least Squares** comes from the way the optimization process works:
1. **Fix the item matrix** \( I \) and solve for the user matrix \( U \) by minimizing the least squares error.
2. **Fix the user matrix** \( U \) and solve for the item matrix \( I \).

This alternating process is repeated iteratively until the model converges.

### Key Parameters:
1. **`factors=50`**:
   - The number of latent factors \( k \). These factors represent hidden features that explain the interactions between users and items.
   - Example: In a movie recommendation system, these latent factors might represent genres like "action", "romance", or "comedy".
   - A higher value for `factors` allows the model to capture more complex relationships, but can also lead to overfitting.

2. **`regularization=0.01`**:
   - Regularization is used to prevent overfitting by adding a penalty term to the cost function.
   - The regularization term controls how large the values in the user and item matrices can become.
   - A small regularization value (e.g., 0.01) allows for a more flexible model, while a larger value helps simplify the model.

3. **`iterations=15`**:
   - The number of times the model alternates between updating the user matrix and the item matrix.
   - More iterations generally improve the model's accuracy, but increase computation time.
   - The optimal number of iterations depends on the complexity of the data and convergence speed.

### Cost Function (Loss Function):
ALS aims to minimize the error between the actual values and the predicted values. The cost function is:

\[
\text{Loss} = \sum_{(u, i) \in \text{observed}} (r_{ui} - u_u^T \cdot i_i)^2 + \lambda \left( \sum_u \| u_u \|^2 + \sum_i \| i_i \|^2 \right)
\]

Where:
- \( r_{ui} \) is the actual rating or interaction between user \( u \) and item \( i \),
- \( u_u \) and \( i_i \) are the corresponding user and item vectors,
- \( \lambda \) is the regularization parameter.

The first part of the loss function minimizes the error, and the second part applies regularization to avoid overfitting.

### Training Process:
1. **Initialize**: Start with random values for the user and item matrices.
2. **Alternating Optimization**:
   - Fix the item matrix \( I \), and update the user matrix \( U \).
   - Fix the user matrix \( U \), and update the item matrix \( I \).
3. **Repeat** the alternating optimization process for a set number of iterations (e.g., `iterations=15`).
4. **Result**: After training, you get two matrices \( U \) and \( I \) that can be used to predict missing values (e.g., recommend items to users).

### Advantages of ALS:
- **Scalability**: ALS is efficient and scalable, which makes it suitable for large datasets.
- **Sparse Data**: It works well with sparse data, which is common in recommendation systems where most users haven't interacted with all items.
- **Prediction**: It allows for predicting missing interactions (e.g., recommending products to users even when no prior interaction exists).

### Disadvantages of ALS:
- **Assumes Positive Interactions**: ALS assumes all interactions are positive, which may not be ideal for systems with negative feedback (e.g., dislikes or ratings of "1").
- **Cold Start Problem**: It can struggle with new users or items that have no interaction history.

### Conclusion:
The **Alternating Least Squares (ALS)** algorithm is a matrix factorization method used in collaborative filtering. It learns to predict missing values in the user-item matrix by decomposing it into latent factors. The model is trained by alternating between optimizing the user and item matrices, and regularization helps prevent overfitting. ALS is highly effective for building scalable recommendation systems, especially when dealing with sparse data.
