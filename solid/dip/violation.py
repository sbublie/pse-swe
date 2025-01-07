"""
Now we want to decouple the our payment processor from authentication method.
It should only be concerned with how its payment is processed, not how it is 
valifdated, whether that be by SMS, a robot check, or an email.

For that we follow the Dependency Inversion Principle. 

The Dependency Inversion Principle states that high-level modules should not 
depend on low-level modules, but both should depend on abstractions. 
This means that you should not have to change other sections of your code when 
you change the implementation of a class.

"""
# some hack to get the old version of DebitCardPaymentProcessor
import os
import sys
print(os.getcwd())
path = os.sep.join(os.getcwd().split(os.sep)[0:-1])
sys.path.append(path)
print(sys.path)

from order import Order, OrderStatus
from product import Product
from isp.payment import DebitCardPaymentProcessor, CreditCardPaymentProcessor
from isp.payment import PaypalPaymentProcessor

if __name__ == "__main__":

    order = Order()    
    order.add_item(product=Product("Keyboard", 50.0), quantity=1)
    order.add_item(product=Product("SSD", 150.0), quantity=1)
    order.add_item(product=Product("USB cable", 5.0), quantity=2)

    try:
        print(order.status)
        service = CreditCardPaymentProcessor(sms="+491721234567")
        security_code = service.send_security_code()
        total_price = service.pay(order=order)
    except Exception as e:
        print(f"Payment was not successful, reason was an error: {e}")

    order.status = OrderStatus.ORDER_OPEN
    try:
        print(order.status)
        service = DebitCardPaymentProcessor(sms="+491721234567")
        total_price = service.pay(order=order)
    except Exception as e:
        print(f"Payment was not successful, reason was an error: {e}")
    
    try:
        print(order.status)
        service = PaypalPaymentProcessor(email_address="nick@abc.com")
        total_price = service.pay(order=order)
    except Exception as e:
        print(f"Payment was not successful, reason was an error: {e}")
    
    try:
        print(order.status)
        service = PaypalPaymentProcessor(email_address="nick@abc.com")
        total_price = service.pay(order=order)
    except Exception as e:
        print(f"Payment was not successful, reason was an error: {e}")
    


