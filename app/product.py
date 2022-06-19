from my_cart_app import db_connection
from my_cart_app.app.categories import CategoryManager


class ProductManager:
    def __init__(self):
        self.cursor = db_connection.cursor()
        self.db_manager = ProductDBManager(self.cursor)

    def get_product_id_and_return_product_detail(self):
        product_id = int(input('Enter product id: '))
        return self.db_manager.get_product(product_id)

    def get_product_category_id_and_return_product_details(self):
        category_id = int(input('Enter category id: '))
        return self.db_manager.get_products_for_category(category_id)

    def add_new_product(self):
        product_category_id = str(input('Enter product category id: '))
        product_name = str(input('Enter product name: '))
        product_price = float(input('Enter product price: '))
        count = int(input("Enter a number of elements in the description dictionary: "))
        product_description = {}
        for i in range(count):
            key = str(input("Enter key : "))
            value = str(input("Enter values :"))

            key = key.lower()
            key = key.replace(' ', '_')
            product_description.update({key: value})

        # validate the data
        ProductUtil().validate_product_data(product_category_id, product_name, product_price, product_description)
        # add new product
        return self.db_manager.add_new_product(product_category_id, product_name, product_price, product_description)


class ProductUtil:
    @staticmethod
    def get_product_details_from_cursor(db_cursor):
        columns = [col[0] for col in db_cursor.description]
        return [dict(zip(columns, row)) for row in db_cursor.fetchall()]

    def validate_product_data(self, product_category_id, product_name, product_price, product_description):
        # check product category
        category_obj = CategoryManager().get_product_category_by_id(product_category_id)
        if not category_obj:
            return "Product category not found"

        # check if product exist by name
        product_obj = ProductDBManager().get_product_by_name(product_name)
        if product_obj:
            return "Product exist in database"


class ProductDBManager:
    def __init__(self, cursor):
        self._cursor = cursor
        self._util = ProductUtil

    def get_product(self, product_id):
        query = f"select * from products where id={product_id};"
        self._cursor.execute(query)
        products = self._util.get_product_details_from_cursor(self._cursor)
        if products:
            return products[0]

    def get_product_by_name(self, product_name):
        query = f"select id from products where productName={product_name};"
        self._cursor.execute(query)
        products = self._util.get_product_details_from_cursor(self._cursor)
        if products:
            return products
        return None

    def get_products_for_category(self, category_id):
        query = f"select id, productName, price from products where category={category_id};"
        self._cursor.execute(query)
        return self._util.get_product_details_from_cursor(self._cursor)

    def add_new_product(self, product_category_id, product_name, product_price, product_description):
        query = f"INSERT INTO products (productName, price, description, category) " \
                f"VALUES ({str(product_name)}, {float(product_price)}, '{dict(product_description)}'," \
                f" {int(product_category_id)});"

        self._cursor.execute(query)
        db_connection.commit()
        return "New product added successfully."
