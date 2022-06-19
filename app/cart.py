import db_connection
from app.product import ProductDBManager


class CartManager:
    def __init__(self):
        self.cursor = db_connection.cursor()
        self.db_manager = CartDBManager(self.cursor)

    def get_product_from_cart(self):
        return self.db_manager.get_cart_product_from_db()

    def add_product_into_cart(self):
        product_id = int(input('Enter product id to add in cart: '))
        return self.db_manager.add_product_into_cart(product_id)

    def remove_product_from_cart(self):
        product_id = int(input('Enter product id to remove from cart: '))
        return self.db_manager.remove_product_from_cart(product_id)


class CartUtil:
    @staticmethod
    def get_cart_product_from_cursor(db_cursor):
        columns = [col[0] for col in db_cursor.description]
        product_list = [dict(zip(columns, row)) for row in db_cursor.fetchall()]
        response_data = {'product_list': product_list,
                         'cart_amount': '{:20,.2f}'.format(float(sum(item['price'] for item in product_list))).strip()}
        return response_data


class CartDBManager:
    def __init__(self, cursor):
        self._cursor = cursor
        self._util = CartUtil

    def get_cart_product_from_db(self):
        query = f"SELECT p.id, p.productName, p.price FROM products p inner join cart c on p.id = c.productId;"
        self._cursor.execute(query)
        product_list = self._util.get_cart_product_from_cursor(self._cursor)
        if product_list:
            return product_list
        return None

    def add_product_into_cart(self, product_id):
        product_obj = ProductDBManager().get_product(product_id)
        if not product_obj:
            return "No product found."

        query = f"INSERT INTO cart (productId) SELECT {str(product_id)} WHERE NOT EXISTS (SELECT productId FROM " \
                f"cart WHERE productId={product_id}); "
        self._cursor.execute(query)
        db_connection.commit()
        return f"Product added in cart."

    def remove_product_from_cart(self, product_id):
        query = f"delete from cart where productId={product_id}"
        self._cursor.execute(query)
        db_connection.commit()
        return f"Product removed from cart."

