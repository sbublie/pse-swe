"""
Now the code is closed for modification and open for extension
because we can add new payment methods without modifying the PaymentService class.
"""
from order import Order
from product import Product
from payment import DebitCardPaymentProcessor

if __name__ == "__main__":

    order = Order()
    print(order.status)
        
    order.add_item(product=Product("Keyboard", 50.0), quantity=1)
    order.add_item(product=Product("SSD", 150.0), quantity=1)
    order.add_item(product=Product("USB cable", 5.0), quantity=2)
    
    service = DebitCardPaymentProcessor()
    total_price = service.pay(order=order,
                              security_code="0372846")

    print(order.status)

