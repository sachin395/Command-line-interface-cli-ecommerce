import pprint

from app.billing import BillingManager
from app.cart import CartManager
from app.categories import CategoryManager
from app.product import ProductManager


def mycart(choice):
    if choice==1:
        CategoryManager().get_product_categories()
    elif choice==2:
        ProductManager().get_product_category_id_and_return_product_details()
    elif choice==3:
        ProductManager().get_product_id_and_return_product_detail()
    elif choice==4:
        CartManager().add_product_into_cart()
    elif choice==5:
         CartManager().get_product_from_cart()
    elif choice==6:
         CartManager().remove_product_from_cart()
    elif choice==7:
        BillingManager().create_bill()
    else:
        print('invaild choice!!!!')


if __name__ == '__main__':
    while True:
        print('\n---------------MyCart E-commerce app---------------')
        print('\n1. List of categories')
        print('\n2. View product category wise')
        print('\n3. View product details')
        print('\n4. Add products to cart')
        print('\n5. Display added product in cart')
        print('\n6. Remove Product from cart')
        print('\n7. Buy product bill')
        print('---------------------------------------------------')

        choice = int(input('Enter your choice: '))
        data = mycart(choice)
        pprint.pprint(data)

