"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread, currentThread
import time

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """

        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        for cart in self.carts:
            id_cart = self.marketplace.new_cart()
            for operation in cart:
                op_count = 0
                while op_count < operation['quantity']:
                    if operation['type'] == 'add':
                        if self.marketplace.add_to_cart(id_cart, operation['product']) is False:
                            time.sleep(self.retry_wait_time)        #reincearca pana reusesc toate operatiile
                        else:
                            op_count += 1
                    elif operation['type'] == 'remove':
                        self.marketplace.remove_from_cart(id_cart, operation['product'])
                        op_count += 1

            products_in_cart = self.marketplace.place_order(id_cart)
            for product in products_in_cart:                               #afiseaza produsele din cart
                print(currentThread().getName() + " bought " + str(product))
