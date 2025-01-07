from order import Order, OrderStatus
from product import Product
from payment import DebitCardPaymentProcessor, CreditCardPaymentProcessor
from payment import PaypalPaymentProcessor

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
    


