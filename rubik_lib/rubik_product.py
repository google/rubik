# Copyright 2022 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List


class RubikCsvFields:
    """Constants for accessing fields on the CSV file"""
    CHANNEL = 0
    CONTENT_LANGUAGE = 1
    TARGET_COUNTRY = 2
    OFFER_ID = 3
    MERCHANT_ID = 4
    IMAGE_LINK = 5
    ADDITIONAL_IMAGE_LINKS = 6
    ADDITIONAL_IMAGE_LINKS_SEPARATOR = '|'


class RubikProduct:
    """Model Class that represents an entry that needs to be updated."""

    def __init__(self, product_id: str, merchant_id: str, image_link: str, additional_image_links: List[str]):
        self.product_id = product_id
        self.merchant_id = merchant_id
        self.image_link = image_link
        self.additional_image_links = additional_image_links


def rubik_product_from_csv_line(line: str) -> RubikProduct:
    fields = line.split(',')
    product_id = f"{fields[RubikCsvFields.CHANNEL]}:{fields[RubikCsvFields.CONTENT_LANGUAGE]}:{fields[RubikCsvFields.TARGET_COUNTRY]}:{fields[RubikCsvFields.OFFER_ID]}"
    additional_image_links = fields[RubikCsvFields.ADDITIONAL_IMAGE_LINKS].split(
        RubikCsvFields.ADDITIONAL_IMAGE_LINKS_SEPARATOR)
    return RubikProduct(product_id, fields[RubikCsvFields.MERCHANT_ID],
                        fields[RubikCsvFields.IMAGE_LINK], additional_image_links)


def rubik_product_from_big_query_row(row):
    product_id = f"{row['channel']}:{row['content_language']}:{row['target_country']}:{row['offer_id']}"
    merchant_id = f"{row['merchant_id']}"
    image_link = row['image_link']
    additional_image_links = row['additional_image_links']
    return RubikProduct(product_id, merchant_id, image_link, additional_image_links)
