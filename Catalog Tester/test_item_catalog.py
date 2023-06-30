# Copyright 2022 Moloco, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pandas import read_csv, isna, notna
import datatest as dt
import datetime
import pandas as pd
import pytest
import validators

#
#
# Helper functions
#
#
@pytest.fixture()
def df():
    filename = 'item_catalog.tsv'
    df = read_csv(filename, sep='\t', encoding='utf8')
    return df

def iterate_rows(df, assert_wellformed_column):
    for index, row in df.iterrows():
        assert_wellformed_column(index, row)
    del df

def print_message(test_passed, index, row, func_name):
    if not test_passed:
        print(func_name, 'failed at row number', index)
        print(row)

def valid_datetime(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        return False
    return True

#
#
# Pytest harness
#
#

@pytest.mark.mandatory
def test_column_names(df):
    required_names = {
        'id',
        'seller_id',
        'seller_name',
        'title',
        'normal_price',
        'price_pc',
        'link', 
        'image_link',
        'category',
        'review_count',
        'rating',
        'shipping',
        'brand',
        'longtail_yn',
        'updated_at',
        'availability',
        'blocked'}
    dt.validate(df.columns, required_names)

def test_column_id(df):
    iterate_rows(df, assert_wellformed_id)

def test_column_seller_id(df):
    iterate_rows(df, assert_wellformed_seller_id)

def test_column_seller_name(df):
    iterate_rows(df, assert_wellformed_seller_name)

def test_column_title(df):
    iterate_rows(df, assert_wellformed_title)

def test_column_normal_price(df):
    iterate_rows(df, assert_wellformed_normal_price)

def test_column_price_pc(df):
    iterate_rows(df, assert_wellformed_price_pc)

def test_column_link(df):
    iterate_rows(df, assert_wellformed_link)

def test_column_image_link(df):
    iterate_rows(df, assert_wellformed_image_link)

def test_column_category(df):
    iterate_rows(df, assert_wellformed_category)

def test_column_review_count(df):
    iterate_rows(df, assert_wellformed_review_count)

def test_column_rating(df):
    iterate_rows(df, assert_wellformed_rating)

def test_column_shipping(df):
    iterate_rows(df, assert_wellformed_shipping)

def test_column_brand(df):
    iterate_rows(df, assert_wellformed_brand)

def test_column_longtail_yn(df):
    iterate_rows(df, assert_wellformed_longtail_yn)

def test_column_updated_at(df):
    iterate_rows(df, assert_wellformed_updated_at)

def test_column_availability(df):
    iterate_rows(df, assert_wellformed_availability)

def test_column_blocked(df):
    iterate_rows(df, assert_wellformed_blocked)


#
#
# Column value validation rules
#
#
def assert_wellformed_id(index, row):
    """
    id length can be up to 50 characters.
    """
    col = str(row.id)
    test_passed = notna(col) and len(col) <= 50

    print_message(test_passed, index, row, assert_wellformed_id.__name__)
    assert test_passed

def assert_wellformed_seller_id(index, row):
    """
    seller_id length can be up to 50 characters.
    """
    col = str(row.seller_id)
    test_passed = notna(col) and len(col) <= 50
    print_message(test_passed, index, row, assert_wellformed_seller_id.__name__)
    assert test_passed

def assert_wellformed_seller_name(index, row):
    """
    If blocked is None or 'in_stock,' seller_name must have valune with length of up to 200 characters.
    If blocked is 'unavailable,' seller_name must be 'undefined'
    """
    blocked = row.blocked
    seller_name = row.seller_name

    test_passed = True
    if isna(blocked) or blocked == 'in_stock':
        test_passed = seller_name is not None and len(seller_name) <= 200
    elif blocked == 'unavailable':
        test_passed = seller_name == 'undefined'

    print_message(test_passed, index, row, assert_wellformed_seller_name.__name__)
    assert test_passed

def assert_wellformed_title(index, row):
    """
    title length can be up to 200 characters.
    """
    col = str(row.title)
    test_passed = notna(col) and len(col) <= 200
    print_message(test_passed, index, row, assert_wellformed_title.__name__)
    assert test_passed

def assert_wellformed_normal_price(index, row):
    """
    normal_price column must be integer
    """
    col = row.normal_price
    test_passed = isna(col) or pd.api.types.is_integer(col)
    print_message(test_passed, index, row, assert_wellformed_normal_price.__name__)
    assert test_passed

def assert_wellformed_price_pc(index, row):
    """
    price_pc column must be float
    """
    col = row.price_pc
    test_passed = isna(col) or pd.api.types.is_float(col)
    print_message(test_passed, index, row, assert_wellformed_price_pc.__name__)
    assert test_passed

def assert_wellformed_link(index, row):
    """
    link length can be up to 2000 characters.
    It should start with 'https'
    It should follow RFC 2396 or RFC 1738
    """
    col = row.link
    test_passed = notna(col) \
        and len(col) <= 2000 \
        and col.startswith('https') \
        and validators.url(col)
    print_message(test_passed, index, row, assert_wellformed_link.__name__)
    assert test_passed

def assert_wellformed_image_link(index, row):
    """
    image_link length can be up to 2000 characters.
    It should start with 'https'
    It should follow RFC 2396 or RFC 1738
    """
    col = row.image_link
    test_passed = notna(col) \
        and len(col) <= 2000 \
        and col.startswith('https') \
        and validators.url(col)
    print_message(test_passed, index, row, assert_wellformed_image_link.__name__)
    assert test_passed

def assert_wellformed_category(index, row):
    """
    category can be up to 750 characters.
    It should use '>' character to indicate the category levels.
    """
    col = row.category
    test_passed = notna(col) and len(col) <= 750 and '>' in col
    print_message(test_passed, index, row, assert_wellformed_category.__name__)
    assert test_passed

def assert_wellformed_review_count(index, row):
    """
    review_count column must be integer
    """
    col = row.review_count
    test_passed = isna(col) or pd.api.types.is_integer(col)
    print_message(test_passed, index, row, assert_wellformed_review_count.__name__)
    assert test_passed

def assert_wellformed_rating(index, row):
    """
    rating column must be float
    """
    col = row.rating
    test_passed = isna(col) or pd.api.types.is_float(col)
    print_message(test_passed, index, row, assert_wellformed_rating.__name__)
    assert test_passed

def assert_wellformed_shipping(index, row):
    """
    shipping column must be float
    """
    col = row.shipping
    test_passed = isna(col) or pd.api.types.is_float(col)
    print_message(test_passed, index, row, assert_wellformed_shipping.__name__)
    assert test_passed

def assert_wellformed_brand(index, row):
    """
    brand can be up to 70 characters.
    """
    col = row.brand
    test_passed = notna(col) and len(col) <= 70
    print_message(test_passed, index, row, assert_wellformed_brand.__name__)
    assert test_passed

def assert_wellformed_longtail_yn(index, row):
    """
    longtail_yn must be 'Y' or 'N'
    """
    col = row.longtail_yn
    test_passed = notna(col) and (col == 'Y' or col == 'N')
    print_message(test_passed, index, row, assert_wellformed_longtail_yn.__name__)
    assert test_passed

def assert_wellformed_updated_at(index, row):
    """
    updated_at must be '%Y-%m-%d %H:%M:%S.%f'
    """
    col = row.updated_at
    test_passed = notna(col) and valid_datetime(col)
    print_message(test_passed, index, row, assert_wellformed_updated_at.__name__)
    assert test_passed

def assert_wellformed_availability(index, row):
    """
    availability must be empty, 'in_stock' or 'out_of_stock'
    """
    col = row.availability
    test_passed = isna(col) or col == 'in_stock' or col == 'out_of_stock'
    print_message(test_passed, index, row, assert_wellformed_availability.__name__)
    assert test_passed

def assert_wellformed_blocked(index, row):
    """
    Blocked column must be empty, 'in_stock', or 'unavailable'
    """
    col = row.blocked
    test_passed = isna(col) or col == 'in_stock' or col == 'unavailable'
    print_message(test_passed, index, row, assert_wellformed_blocked.__name__)
    assert test_passed



