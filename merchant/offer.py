import logging
from typing import Tuple, List, Iterable
import sys

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
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


class RubikOffer:
    """Model Class that represents an entry that needs to be updated."""

    def __init__(self, product_id: str, merchant_id: str, image_link: str, additional_image_links: List[str]):
        self.product_id = product_id
        self.merchant_id = merchant_id
        self.image_link = image_link
        self.additional_image_links = additional_image_links

class BatchOffers(beam.DoFn):
    def __init__(self, batch_size: int):
        self._batch_size = batch_size

    def process(self, grouped_elements: Tuple[str, Iterable[RubikOffer]]) -> Tuple[str, List[RubikOffer]]:
        merchant_id = grouped_elements[0]
        batch: List[RubikOffer] = []
        for i, element in enumerate(grouped_elements[1]):
            if i != 0 and i % self._batch_size == 0:
                yield merchant_id, batch
                batch = []
            batch.append(element)
        yield merchant_id, batch

