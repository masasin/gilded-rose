# -*- coding: utf-8 -*-
import pytest

from gilded_rose import GildedRose, Category, Brie, Conjured, Passes, Sulfuras


items_to_try = [
    # Once the sell by date has passed, `quality` degrades twice as fast
    [Category(10, 8), 7],
    [Category(0, 8), 6],
    [Category(-1, 8), 6],

    # The quality of an item is never negative
    [Category(10, 1), 0],
    [Category(10, 0), 0],
    [Category(-1, 1), 0],
    [Category(-1, 0), 0],

    # "Aged Brie" increases in quality the older it gets
    [Brie(20, 5), 6],
    [Brie(10, 5), 6],
    [Brie(0, 5), 7],
    [Brie(-1, 5), 7],
    [Brie(-10, 5), 7],

    # Backstage passes increase in quality until concert
    [Passes(20, 5), 6],
    [Passes(10, 5), 7],
    [Passes(5, 5), 8],
    [Passes(0, 5), 0],
    [Passes(-1, 0), 0],

    # The quality of an item is never more than 50
    [Brie(10, 50), 50],
    [Brie(0, 50), 50],
    [Brie(-10, 50), 50],
    [Passes(10, 50), 50],
    [Passes(3, 50), 50],

    # Sulfuras is always 80
    [Sulfuras(10, 80), 80],
    [Sulfuras(0, 80), 80],
    [Sulfuras(-10, 80), 80],

    # Conjured items decrease at double rate
    [Conjured(10, 8), 6],
    [Conjured(0, 8), 4],
    [Conjured(-1, 8), 4],
    [Conjured(10, 1), 0],
    [Conjured(10, 0), 0],
    [Conjured(-1, 1), 0],
    [Conjured(-1, 0), 0],
]

item_ids = [f"{item} -> {next_quality}" for item, next_quality in items_to_try]


@pytest.mark.parametrize(["item", "next_quality"], items_to_try, ids=item_ids)
def test_next_quality(item, next_quality):
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()
    assert item.quality == next_quality
