#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List, Dict, Optional
from abc import ABC, abstractmethod
import re


class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self,name: str, price: float):
        self.name = name
        self.price = price

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price  # FIXME: zwróć odpowiednią wartość

    def __hash__(self):
        return hash((self.name, self.price))

    # TODO: Dodać wyjątek ValueError

class ServerError(Exception):
    pass
    # def __init__(self, server, msg=None):
    #     if msg is None:
    #         msg = f"An error occured with server {server}"
    #     super().__init__(msg)
    #     self.server = server

class TooManyProductsFoundError(ServerError, ValueError):
    pass
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    # def __init__(self, msg):
    #     super().__init__(msg)


class Server(ABC):
    n_max_returned_entries: int = 3

    def __init__(self, *args, **kwargs):
        super.__init__(*args,**kwargs)

    def get_entries_len_check(self, n_letters: Optional[int]=1) -> List[Product]:
        if len(self.products) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError("Too many products on server.")


    @abstractmethod
    def _get_entries(self, n_letters: Optional[int] = 1) -> List[Product]:
        raise NotImplementedError

# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class ListServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        self.products = products
        super.__init__(*args, *kwargs)

    def get_entries(self, n_letters: Optional[int]=1) -> List[Product]:
        matching_products: List[Product] = []
        for iteration, prod in enumerate(self.products):
            if iteration > 2:
                raise TooManyProductsFoundError
            if re.match("^[a-zA-Z]{n_letters}[0-9]{2,3}".format(n_letters=n_letters), prod.name):
                matching_products.append(prod)
        return matching_products

class MapServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        self.products = {elem.name : elem for elem in products}
        super.__init__(*args, *kwargs)

    def get_entries(self, n_letters: Optional[int] = 1) -> List[Product]:
        matching_products: List[Product] = []
        for iteration, (name, prod) in enumerate(self.products.items()):
            if iteration > 2:
                raise TooManyProductsFoundError
            if re.fullmatch("^[a-zA-Z]{n_letters}[0-9]{2,3}".format(n_letters=n_letters), prod.name):
                matching_products.append(prod)
        return matching_products

class Client:
    def __init__(self, server: Server):
        self.server = server
    #def get_total_price(self, n_letters: Optional[int]): Optional[float]
        #for product in self.server:
         #   pass

