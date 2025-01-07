from order import Order
from product import Product
from payment import DebitCardPaymentProcessor, PaypalPaymentProcessor

if __name__ == "__main__":

    order = Order()    
    order.add_item(product=Product("Keyboard", 50.0), quantity=1)
    order.add_item(product=Product("SSD", 150.0), quantity=1)
    order.add_item(product=Product("USB cable", 5.0), quantity=2)
    try:
        print(order.status)
        service = DebitCardPaymentProcessor(security_code="0372846")
        total_price = service.pay(order=order)
    except Exception as e:
        print(f"Payment was not successful, reason was an error: {e}")
    
    try:
        print(order.status)
        service = PaypalPaymentProcessor(email_address="nick@abc.com")
        total_price = service.pay(order=order)
    except Exception as e:
        print(f"Payment was not successful, reason was an error: {e}")
    
    order.status = "open"

    try:
        print(order.status)
        service = PaypalPaymentProcessor(email_address="nick@abc.com")
        total_price = service.pay(order=order)
    except Exception as e:
        print(f"Payment was not successful, reason was an error: {e}")
