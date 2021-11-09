#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Union
from abc import ABC, abstractmethod
import re
from copy import deepcopy

class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną
    #  przyjmującą argumenty wyrażające nazwę produktu (typu str)
    #  i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)

    def is_name_correct(self, name: str) -> bool:
        if not name[0].isalpha():
            return False
        else:
            i: int = 1
            while i < len(name) and name[i].isalpha():
                i += 1
            if i >= len(name):
                return False
            while i < len(name) and name[i].isdecimal():
                i += 1
            if i >= len(name):
                return True
        return False

    def __init__(self, name: str, price: float) -> None:
        if not self.is_name_correct(name):
            raise ValueError

        self.name: str = name
        self.price: float = price

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.price == other.price


    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, length: int):
        msg: str = f"The length of the list is above the limit equal to :{length}"
        super().__init__(msg)

    pass


# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class Server(ABC):
    n_max_returned_entries: int = 3

    @abstractmethod
    def get_entries(self, n_letters: Optional[int] = 1) -> List[Optional[Product]]:
        raise NotImplementedError


class ListServer(Server):

    def __init__(self, products: List[Product]):
        self.products: List[Product] = deepcopy(products)

    def get_entries(self, n_letters: Optional[int] = 1) -> List[Optional[Product]]:
        lst: List = []
        for i in self.products:
            if re.fullmatch(r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$', i.name):
                lst.append(i)
        if len(lst) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError(Server.n_max_returned_entries)
        else:
            return sorted(lst, key=lambda product: product.price)


class MapServer(Server):

    def __init__(self, products: List[Product]):
        self.products: Dict[str: float] = {product.name: product.price for product in products}

    def get_entries(self, n_letters: Optional[int] = 1) -> List[Optional[Product]]:
        lst = []
        for i in self.products.keys():
            if re.fullmatch(r'^[a-zA-Z]{' + str(n_letters) + r'}\d{2,3}$', i):
                lst.append(Product(i, self.products[i]))
        if len(lst) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError(Server.n_max_returned_entries)
        else:
            return sorted(lst, key=lambda product: product.price)


class Client:

    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server: Union[ListServer, MapServer]):
        self.server: Union[ListServer, MapServer] = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            lst: List = self.server.get_entries(n_letters)
        except TooManyProductsFoundError:
            return None
        if not lst:
            return None
        else:
            sum: int = 0
            for i in lst:
                sum += i.price
            return sum