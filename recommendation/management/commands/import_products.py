import os
from datetime import datetime
import pandas as pd

from django.core.management.base import BaseCommand
from django.conf import settings

from .models import Product


class Command(BaseCommand):
    help = 'Imports products from a CSV file into the database'

    def handle(self, *args, **kwargs):
        # Read CSV file into a DataFrame
        csv_file_path = os.path.join(settings.BASE_DIR, 'resources/ecommerce_product_dataset.csv')
        df = pd.read_csv(csv_file_path)

        # Iterate through the DataFrame and create model instances
        for index, row in df.iterrows():
            try:
                # Parse date if format is not YYYY-MM-DD
                date_added = datetime.strptime(row['DateAdded'], '%Y-%m-%d').date()  # Adjust format as needed

                # Create the Product instance
                product, created = Product.objects.get_or_create(
                    product_id=row['ProductID'],
                    defaults={
                        'product_name': row['ProductName'],
                        'category': row['Category'],
                        'price': row['Price'],
                        'rating': row['Rating'],
                        'reviews': row['NumReviews'],
                        'quantity': row['StockQuantity'],
                        'discount': row['Discount'],  # Fixed this line
                        'sales': row['Sales'],
                        'date_added': date_added
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Product {row['ProductName']} created"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Product {row['ProductName']} already exists"))
            except Exception as error:
                self.stdout.write(self.style.ERROR(f"Error importing row {index}: {error}"))
        self.stdout.write(self.style.SUCCESS("CSV data has been loaded into the Django database."))
