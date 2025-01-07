"""
Now we want to add the ability to send the user an SMS to authenticate their 
payment with a security code, but only Credit and Debit payment will use it.

So we force also the PaypalPaymentProcessor to implement it, if we add a new
method to the interface.

This is a violation to the Interface Segregation Principle.

"""
from order import Order
from product import Product
from old_payment import OldDebitCardPaymentProcessor
from old_payment import OldCreditCardPaymentProcessor
from old_payment import OldPaypalPaymentProcessor

if __name__ == "__main__":

    order = Order()    
    order.add_item(product=Product("Keyboard", 50.0), quantity=1)
    order.add_item(product=Product("SSD", 150.0), quantity=1)
    order.add_item(product=Product("USB cable", 5.0), quantity=2)
    try:
        print(order.status)
        service = OldCreditCardPaymentProcessor(security_code="0372846")
        total_price = service.pay(order=order)
    except Exception as e:
        print(f"Payment was not successful, reason was an error: {e}")

    try:
        print(order.status)
        service = OldDebitCardPaymentProcessor(security_code="0372846")
        service.send_security_code("1234567")
        total_price = service.pay(order=order)
    except Exception as e:
        print(f"Payment was not successful, reason was an error: {e}")

    try:
        print(order.status)
        service = OldPaypalPaymentProcessor(email_address="nick@abc.com")
        total_price = service.pay(order=order)
    except Exception as e:
        print(f"Payment was not successful, reason was an error: {e}")
    
    order.status = "open"

    try:
        print(order.status)
        service = OldPaypalPaymentProcessor(email_address="nick@abc.com")
        total_price = service.pay(order=order)
    except Exception as e:
        print(f"Payment was not successful, reason was an error: {e}")

