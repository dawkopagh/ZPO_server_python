
#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Union
from abc import ABC, abstractmethod
import re
from copy import deepcopy

class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
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

    def __init__(self,name:str,price:float) ->None:
        if not self.is_name_correct(name):
            raise ValueError

        self.name:str = name
        self.price:float = price

    def __eq__(self, other)->bool:
        return self.name == other.name and self.price == other.price

    def __hash__(self):
        return hash((self.name,self.price))






    # TODO: Dodać wyjątek ValueError


class TooManyProductsFoundError(Exception): #Wyjątek zdefiniowany przez użytkownika

    def __init__(self,length:int,msg = None):
        if msg is None:
            msg: str = f"The length of the list is above the limit equal to :{length}"
        super().__init__(msg)#Wywołanie konstruktora klasy 'Exception'
        self.length=length
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.

    pass


class Server(ABC):
    n_max_returned_intries= int

    def __init__(self, *args, **kwargs):
        super.__init__(*args,**kwargs)

    @abstractmethod
    def get_entries(self, n_letters: Optional[int]=1): List[Product]

# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania

class ListServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        self.products = products
        super.__init__(*args, *kwargs)

    def get_entries(self, n_letters: Optional[int]=1) -> List[Product]:





class MapServer(Server):
    def __init__(self, products: List[Product], *args, **kwargs):
        self.products = {elem.name : elem for elem in products}
        super.__init__(*args, *kwargs)

    def get_entries(self, n_letters: Optional[int] = 1) -> List[Product]:
        matching_products: List[Product] = []
        for prod in self.products:
            if prod.name


class Client:
    def __init__(self, server: Server):
        self.server = server

    def get_total_price(self, n_letters: Optional[int]): Optional[float]
        raise NotImplementedError()
