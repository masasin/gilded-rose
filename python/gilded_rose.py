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
    def __init__(self, name, sell_in, quality, *, min_quality=0, max_quality=50, change=-1):
        super().__init__(name, sell_in, quality)
        self.min_quality = min_quality
        self.max_quality = max_quality
        self.change = change

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, sell_in={self.sell_in}, quality={self.quality})"

    @property
    def multiplier(self):
        return 1 if self.sell_in > 0 else 2

    def _clip_quality(self, value):
        return min(max(value, self.min_quality), self.max_quality)

    def _next_quality(self):
        return self._clip_quality(self.quality + self.change * self.multiplier)

    def update_quality(self):
        self.quality = self._next_quality()


class Brie(Category):
    def __init__(self, name, sell_in, quality, change=1):
        super().__init__(name, sell_in, quality, change=change)


class Conjured(Category):
    def __init__(self, name, sell_in, quality, change=-2):
        super().__init__(name, sell_in, quality, change=change)


class Passes(Category):
    def __init__(self, name, sell_in, quality, change=1):
        super().__init__(name, sell_in, quality, change=change)

    def _next_quality(self):
        if self.sell_in <= 0:
            return 0
        return super()._next_quality()

    @property
    def multiplier(self):
        return max(1, (20 - self.sell_in) // 5)


class Sulfuras(Category):
    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality, min_quality=80, max_quality=80, change=0)


class GildedRose:
    def __init__(self, items: List[Category]):
        self.items = items

    def update_quality(self):
        for item in self.items:
            item.update_quality()
