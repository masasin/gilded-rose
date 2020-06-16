# -*- coding: utf-8 -*-
import pytest

from gilded_rose import Item, GildedRose


FOR_SALE = {
    "other": "Magical foo",
    "brie": "Aged Brie",
    "passes": "Backstage passes to a TAFKAL80ETC concert",
    "sulfuras": "Sulfuras, Hand of Ragnaros",
    "conjured": "Conjured Mana Cake"
}

items_to_try = [
    # Once the sell by date has passed, `quality` degrades twice as fast
    [Item(FOR_SALE["other"], 10, 8), 7],
    [Item(FOR_SALE["other"], 0, 8), 6],
    [Item(FOR_SALE["other"], -1, 8), 6],

    # The quality of an item is never negative
    [Item(FOR_SALE["other"], 10, 1), 0],
    [Item(FOR_SALE["other"], 10, 0), 0],
    [Item(FOR_SALE["other"], -1, 1), 0],
    [Item(FOR_SALE["other"], -1, 0), 0],

    # "Aged Brie" increases in quality the older it gets
    [Item(FOR_SALE["brie"], 20, 5), 6],
    [Item(FOR_SALE["brie"], 10, 5), 6],
    [Item(FOR_SALE["brie"], 0, 5), 7],
    [Item(FOR_SALE["brie"], -1, 5), 7],
    [Item(FOR_SALE["brie"], -10, 5), 7],

    # Backstage passes increase in quality until concert
    [Item(FOR_SALE["passes"], 20, 5), 6],
    [Item(FOR_SALE["passes"], 10, 5), 7],
    [Item(FOR_SALE["passes"], 5, 5), 8],
    [Item(FOR_SALE["passes"], 0, 5), 0],
    [Item(FOR_SALE["passes"], -1, 0), 0],

    # The quality of an item is never more than 50
    [Item(FOR_SALE["brie"], 10, 50), 50],
    [Item(FOR_SALE["brie"], 0, 50), 50],
    [Item(FOR_SALE["brie"], -10, 50), 50],
    [Item(FOR_SALE["passes"], 10, 50), 50],
    [Item(FOR_SALE["passes"], 3, 50), 50],

    # Sulfuras is always 80
    [Item(FOR_SALE["sulfuras"], 10, 80), 80],
    [Item(FOR_SALE["sulfuras"], 0, 80), 80],
    [Item(FOR_SALE["sulfuras"], -10, 80), 80],

    # Conjured items decrease at double rate
    [Item(FOR_SALE["conjured"], 10, 8), 6],
    [Item(FOR_SALE["conjured"], 0, 8), 4],
    [Item(FOR_SALE["conjured"], -1, 8), 4],
    [Item(FOR_SALE["conjured"], 10, 1), 0],
    [Item(FOR_SALE["conjured"], 10, 0), 0],
    [Item(FOR_SALE["conjured"], -1, 1), 0],
    [Item(FOR_SALE["conjured"], -1, 0), 0],
]

item_ids = [f"Item({item.name}, sell_in={item.sell_in}, quality={item.quality}) -> {next_quality}"
            for item, next_quality in items_to_try]


@pytest.mark.parametrize(["item", "next_quality"], items_to_try, ids=item_ids)
def test_next_quality(item, next_quality):
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()
    assert item.quality == next_quality
