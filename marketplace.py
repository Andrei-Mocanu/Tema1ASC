"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import  Lock

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.all_carts = {}
        self.id_carts_lock = Lock()
        self.id_cart = -1
        self.id_producer = -1
        self.id_producer_lock = Lock()
        self.products_in_marketplace = []
        self.producers_queues = {}
        self.producers_products = {}
        self.add_remove_lock = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        self.id_producer_lock.acquire()
        self.id_producer += 1               #inregistreaza producatorul
        self.id_producer_lock.release()

        self.producers_products[self.id_producer] = []     #initiliazieaza lista de produse
        self.producers_queues[self.id_producer] = 0        #initiliazieaza coada

        return self.id_producer

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        if not self.producers_queues[int(producer_id)] < self.queue_size_per_producer:
            return False

        self.producers_queues[int(producer_id)] += 1
        self.products_in_marketplace.append(product)                   #adauga produsul in market
        self.producers_products[int(producer_id)].append(product)

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """

        self.id_carts_lock.acquire()
        self.id_cart += 1                       #initializeaza cartul
        self.id_carts_lock.release()
        self.all_carts[self.id_cart] = []

        return self.id_cart

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """


        with self.add_remove_lock:
            if product not in self.products_in_marketplace:
                return False
            self.products_in_marketplace.remove(product)
            for producer in self.producers_products:
                if product in self.producers_products[producer]:            #adauga in cart primul element
                    self.producers_queues[producer] -= 1                    #de tipul specificat din dictionarul
                    self.producers_products[producer].remove(product)       #de producatori
                    break

        self.all_carts[cart_id].append(product)
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        self.all_carts[cart_id].remove(product)

        with self.add_remove_lock:
            self.products_in_marketplace.append(product)
            for producer in self.producers_products:
                if product in self.producers_products[producer]:        #scoate din cart produsul
                    self.producers_queues[producer] += 1                #dat ca parametru din dictionarul
                    self.producers_products[producer].append(product)   #de produse
                    break


    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """

        return self.all_carts[cart_id]                             #intoarce lista cu elemente din cart
