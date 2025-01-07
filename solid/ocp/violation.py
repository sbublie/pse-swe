"""
This code violates the OCP.

If we wish to add a new payment method, we have to make modifications to the 
PaymentService class. 

This violates the Open-Closed Principle!

It states that software entities should be open for extension 
but closed for modification.

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

