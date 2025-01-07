"""
By separating our concerns, we are able to 
- add new methods of payment 
- add new attributes to product
without having to modify the Order class.
"""
from order import Order
from product import Product
from payment import PaymentService

if __name__ == "__main__":

    order = Order()
    print(order.status)
        
    order.add_item(product=Product("Keyboard", 50.0), quantity=1)
    order.add_item(product=Product("SSD", 150.0), quantity=1)
    order.add_item(product=Product("USB cable", 5.0), quantity=2)
    
    service = PaymentService()
    total_price = service.pay(order=order,
                              payment_type="debit", 
                              security_code="0372846")

    print(order.status)

