"""
In our OCP refactoring, we have introduced a new violation of SOLID principles. 

Paypal uses email addresses for verification, whereas credit and debit cards
use security codes. 

This means we are abusing the Liskov Substitution Principle because we are
using a subclass in a way that is not compatible with its parent class.

This is because of the concept of Design by Contract, which in this context 
dictates classes should adhere to the “contract” set out by their interface for 
consistency and integrity

"""
# some hack to get the old version of DebitCardPaymentProcessor
import os
import sys
print(os.getcwd())
path = os.sep.join(os.getcwd().split(os.sep)[0:-1])
sys.path.append(path)
print(sys.path)

from order import Order
from product import Product
from ocp.payment import DebitCardPaymentProcessor

if __name__ == "__main__":

    order = Order()
    print(order.status)
        
    order.add_item(product=Product("Keyboard", 50.0), quantity=1)
    order.add_item(product=Product("SSD", 150.0), quantity=1)
    order.add_item(product=Product("USB cable", 5.0), quantity=2)
    
    service = DebitCardPaymentProcessor()
    total_price = service.pay(order=order,security_code="0372846")

    print(order.status)

