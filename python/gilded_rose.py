# -*- coding: utf-8 -*-
from typing import List


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class Category(Item):
    def __init__(self, sell_in, quality, *, name=None, min_quality=0, max_quality=50, change=-1):
        if name is None:
            name = self.__class__.__name__
        super().__init__(name, sell_in, quality)
        self.min_quality = min_quality
        self.max_quality = max_quality
        self.change = change
        self.multiplier = 1 if self.sell_in > 0 else 2

    def __repr__(self):
        if self.name != self.__class__.__name__:
            return f"{self.__class__.__name__}(sell_in={self.sell_in}, quality={self.quality}, name={self.name!r})"
        else:
            return f"{self.name}(sell_in={self.sell_in}, quality={self.quality})"

    def _clip_quality(self, value):
        return min(max(value, self.min_quality), self.max_quality)

    def _next_quality(self):
        return self._clip_quality(self.quality + self.change * self.multiplier)

    def update_quality(self):
        self.quality = self._next_quality()


class Brie(Category):
    def __init__(self, sell_in, quality, name=None):
        super().__init__(sell_in, quality, name=name, change=1)


class Conjured(Category):
    def __init__(self, sell_in, quality, name=None):
        super().__init__(sell_in, quality, name=name, change=-2)


class Passes(Category):
    def __init__(self, sell_in, quality, name=None):
        super().__init__(sell_in, quality, name=name, change=1)
        self.multiplier = 1 if self.sell_in > 10 else 2 if self.sell_in > 5 else 3

    def _next_quality(self):
        if self.sell_in <= 0:
            return 0
        return super()._next_quality()


class Sulfuras(Category):
    def __init__(self, sell_in, quality, name=None):
        super().__init__(sell_in, quality, name=name, min_quality=80, max_quality=80, change=0)


class GildedRose:
    def __init__(self, items: List[Category]):
        self.items = items

    def update_quality(self):
        for item in self.items:
            item.update_quality()
