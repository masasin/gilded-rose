# -*- coding: utf-8 -*-
class GildedRose:
    categories = {
        "Magical foo": "other",
        "Aged Brie": "brie",
        "Backstage passes to a TAFKAL80ETC concert": "passes",
        "Sulfuras, Hand of Ragnaros": "sulfuras",
        "Conjured Mana Cake": "conjured",
    }

    changes = {
        "passes": 1,
        "brie": 1,
        "conjured": -2,
        "other": -1,
    }

    def __init__(self, items):
        self.items = items

    @staticmethod
    def _clip(value, min_=0, max_=50):
        return min(max(value, min_), max_)

    def update_quality(self):
        for item in self.items:
            category = self.categories[item.name]
            if category == "sulfuras":
                continue
            change = self.changes.get(category)
            if category == "passes":
                if item.sell_in <= 0:
                    item.quality = 0
                    continue
                multiplier = max(1, (20 - item.sell_in) // 5)
            else:
                multiplier = 1 if item.sell_in >= 1 else 2
            item.quality = self._clip(item.quality + change * multiplier)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
