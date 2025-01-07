# SOLID 

The folllowing SOLID examples are found in:

<https://arjancodes.com/blog/solid-principles-in-python-programming/>

Go through the code step by step: SRP, OCP, LSP, ISP and lat DIP

At start all code in within one module violation.py

1.SRP:

We are separating our concerns and split into different modules and we refactor the Order class. Now we are able to to:

    - add new methods of payment
    - add new attributes to product

without having to modify the Order class.

2.OCP:

If we wish to add a new payment method, we have to make modifications to the PaymentService class. Because the actual code This code violates the OCP we have to modify the code:

    - introduce an interface. So we can add new payment methods without modifying the PaymentService class.

3.LSP:

Paypal uses email addresses for verification, whereas credit and debit cards
use security codes.

This means we are abusing the Liskov Substitution Principle because we are
using a subclass in a way that is not compatible with its parent class.

We can fix this with contract by design: Giving the payment processors an init method as contract.

4.ISP:

Now we want to add the ability to send the user an SMS to authenticate their 
payment with a security code, but only Credit and Debit payment will use it.

So we force also the PaypalPaymentProcessor to implement it, if we add a new
method to the interface. This would be a violation to the Interface Segregation Principle.

The solution ist to split the interface into two interfaces.

5.DIP:

Now we want to decouple the payment processor from authentication methods. It should only be concerned with how its payment is processed, not how it is valifdated, whether that be by SMS, a robot check, or an email.

For that we follow the Dependency Inversion Principle.

The Dependency Inversion Principle states that high-level modules should not depend on low-level modules, but both should depend on abstractions. This means that you should not have to change other sections of your code when you change the implementation of a class.

As you can see, by thoughtfully applying the SOLID design principles, you can improve the maintainability and scalability of your applications. The practical application of these principles can lead to software that is more cohesive, less coupled, and easier to improve over the long term.

Thanks to the author of the post: <https://arjancodes.com/blog/solid-principles-in-python-programming/>

