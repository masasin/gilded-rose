# -*- coding: utf-8 -*-
import pytest

from gilded_rose import Item, GildedRose


items_to_try = [
    [Item("foo", 10, 8), 7],
]

item_ids = [f"Item(name={item[0].name}, sell_in={item[0].sell_in}, quality={item[0].quality})" for item in items_to_try]


@pytest.mark.parametrize(["item", "next_quality"], items_to_try, ids=item_ids)
def test_next_quality(item, next_quality):
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()
    assert item.quality == next_quality
