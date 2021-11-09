#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from collections import Counter

from servers import ListServer,MapServer,Client,Product,TooManyProductsFoundError

server_types = MapServer,ListServer

class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('PEE12', 1), Product('R4567', 2), Product('R235', 1), Product('PPG1', 1), Product('PPR23', 4)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(3)
            self.assertEqual(Counter([products[0], products[4]]), Counter(entries))


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PR235', 3), Product('PP235', 3), Product('PN235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))

class ExceptTest(unittest.TestCase):
    def test_too_many_products_exception(self):
        with self.assertRaises(TooManyProductsFoundError):
            products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1), Product('PP236', 3), Product('PP237', 2)]
            for server_type in server_types:
                server = server_type(products)
                return server.get_entries(2)


if __name__ == '__main__':
    unittest.main()
