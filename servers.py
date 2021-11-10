#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List, Dict, Optional, TypeVar
from abc import ABC, abstractmethod
import re


class Product:

    def __init__(self, name: str, price: float) -> None:

        match_pattern = "^[a-zA-Z]+[0-9]+$"
        if not re.fullmatch(match_pattern, name):
            raise ValueError

        self.name: str = name
        self.price: float = price

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.price == other.price

    def __hash__(self):
        return hash((self.name, self.price))


class ServerError(Exception):
    def __init__(self, server, msg=None):
        if msg is None:
            msg = f"An error occured with server {server}"
        super().__init__(msg)
        self.server = server


class TooManyProductsFoundError(ServerError, ValueError):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self, msg):
        super().__init__(msg)


class Server(ABC):
    n_max_returned_entries: int = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_entries(self, n_letters: Optional[int] = 1) -> List[Product]:
        match_pattern = "^[a-zA-Z]{{{n_letters}}}[0-9]{{2,3}}$".format(n_letters=n_letters)
        entries_list = [product for product in self._get_products_list() if re.match(match_pattern, product.name)]
        if len(entries_list) > Server.n_max_returned_entries:
            raise TooManyProductsFoundError("Too many products on server.")
        return sorted(entries_list, key=lambda product: product.price)

    @abstractmethod
    def _get_products_list(self, n_letters: Optional[int] = 1) -> List[Product]:
        raise NotImplementedError


HelperType = TypeVar('HelperType', bound=Server)


class ListServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        self.products = products
        super().__init__(*args, *kwargs)

    def _get_products_list(self, n_letters: Optional[int] = 1) -> List[Product]:
        return self.products


class MapServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        self.products: Dict[str, Product] = {elem.name: elem for elem in products}
        super().__init__(*args, *kwargs)

    def _get_products_list(self, n_letters: Optional[int] = 1) -> List[Product]:
        return list(self.products.values())


class Client:
    def __init__(self, server: HelperType):
        self.server = server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            if n_letters is None:
                matching_products = self.server.get_entries()
            else:
                matching_products = self.server.get_entries(n_letters)
            return sum([product.price for product in matching_products])
        except TooManyProductsFoundError:
            return None