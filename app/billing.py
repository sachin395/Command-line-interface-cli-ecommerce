import json

from my_cart_app import *


class BillingManager:
    def __init__(self):
        self.cursor = db_connection.cursor()
        self.db_manager = BillingDBManager(self.cursor)

    def create_bill(self):
        username = str(input("Enter name: "))
        return self.db_manager.create_bill(username)

    def get_bill(self):
        return self.db_manager.getbill()


class BillingUtil:
    @staticmethod
    def get_cart_added_products_for_billing(db_cursor):
        columns = [col[0] for col in db_cursor.description]
        product_list = [dict(zip(columns, row)) for row in db_cursor.fetchall()]
        return product_list


class BillingDBManager:
    def __init__(self, cursor):
        self._cursor = cursor
        self._util = BillingUtil

    def create_bill(self, username):
        query = f"SELECT p.id, p.productName, p.price FROM products p inner join cart c on p.id = c.productId;"
        self._cursor.execute(query)

        products = self._util.get_cart_added_products_for_billing(self._cursor)

        if products:
            cart_amount = sum(item['price'] for item in products)
            discount = 0.00
            final_amount = cart_amount
            if cart_amount > MAX_AMT_TO_DISCOUNT:
                discount = DISCOUNT_
                final_amount -= DISCOUNT

            insert_query = f"INSERT INTO billing (username, particulars, actual_amount, discount_amount, final_amount)" \
                           f" VALUES ('{username}', '{json.dumps(products)}', {cart_amount}, {discount}, {final_amount});"
            self._cursor.execute(insert_query)
            self._cursor.execute("delete from cart;")
            db_connection.commit()
            return f"Bill generated successfully."
        return None

    def get_bill(self):
        query = f"SELECT * from billing;"
        self._cursor.execute(query)

        all_bills = self._util.get_cart_added_products_for_billing(self._cursor)
        if not all_bills:
            return None
        return all_bills


