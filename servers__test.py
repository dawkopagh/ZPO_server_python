import unittest
from servers import Client, Server, Product, ListServer, TooManyProductsFoundError


class ClientTest(unittest.TestCase):
    def test_price_equal_zero_if_exception(self):
        products = [Product('ABC2137', 2)] * 4
        server = ListServer(products)
        client = Client(server)

        self.assertEqual(0, client.get_total_price(2))


class ServerTest(unittest.TestCase):
    def test_get_entries_common_equals_sorted_entries(self):
        products = [Product('A21', 1), Product('AA37', 2), Product('AA696', 1)]
        server = ListServer(products)
        entries = server.get_entries_common(2)

        self.assertListEqual([products[2], products[1]], entries)

    def test_get_entries_raises_exceptions_if_too_many_results(self):
        products = [Product('PP234', 2)] * (Server.n_max_returned_entries+1)
        server = ListServer(products)

        with self.assertRaises(TooManyProductsFoundError):
            server.get_entries_common(2)


if __name__ == '__main__':
    unittest.main()
