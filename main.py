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


import logging
from typing import Tuple, List, Iterable
import sys

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from merchant.merchant_center_uploader import MerchantCenterUpdaterDoFn
from merchant.rubik_options import RubikOptions
from merchant.rubik_product import RubikProduct, rubik_product_from_csv_line, rubik_product_from_big_query_row
from utils.logger import logger
from config.read_from_yaml import read_from_yaml
from vision.vision import Vision


class BatchElements(beam.DoFn):
    def __init__(self, batch_size: int):
        self._batch_size = batch_size

    def process(self, grouped_elements: Tuple[str, Iterable[RubikProduct]]) -> Tuple[str, List[RubikProduct]]:
        merchant_id = grouped_elements[0]
        batch: List[RubikProduct] = []
        for i, element in enumerate(grouped_elements[1]):
            if i != 0 and i % self._batch_size == 0:
                yield merchant_id, batch
                batch = []
            batch.append(element)
        yield merchant_id, batch


class Rubik:
    def __init__(self, config_file):
        config = read_from_yaml(config_file)
        pipeline_options = PipelineOptions()
        rubik_options = config
        with beam.Pipeline(options=pipeline_options) as pipeline:
            if rubik_options['csv_file'] is not None:
                (pipeline
                 | "Load rows" >> beam.io.ReadFromText(rubik_options['csv_file'])
                 | "Map lines to objects" >> beam.Map(rubik_product_from_csv_line)
                 | "Vision AI to select best image" >> beam.Map(Vision(config).find_best_image)
                 | "Build Tuples" >> beam.Map(lambda product: (product.merchant_id, product))
                 | "Group by Merchant Id" >> beam.GroupByKey()
                 | "Batch elements" >> beam.ParDo(BatchElements(rubik_options['batch_size'])).with_output_types(
                            Tuple[str, List[RubikProduct]])
                 | "Upload to Merchant Center" >> beam.ParDo(
                            MerchantCenterUpdaterDoFn(rubik_options['client_id'], rubik_options['client_secret'],
                                                      rubik_options['access_token'], rubik_options['refresh_token'], rubik_options['rubik_custom_label']))
                 )
            elif rubik_options['big_query'] is not None:
                (pipeline
                 | "Load rows" >> beam.io.gcp.bigquery.ReadFromBigQuery(table=rubik_options["big_query"], gcs_location=rubik_options["big_query_gcs_location"])
                 | "Map rows to objects" >> beam.Map(rubik_product_from_big_query_row)
                 | "Vision AI to select best image" >> beam.Map(Vision(config).find_best_image)
                 | "Build Tuples" >> beam.Map(lambda product: (product.merchant_id, product))
                 | "Group by Merchant Id" >> beam.GroupByKey()
                 | "Batch elements" >> beam.ParDo(BatchElements(rubik_options["batch_size"])).with_output_types(
                            Tuple[str, List[RubikProduct]])
                 | "Upload to Merchant Center" >> beam.ParDo(
                            MerchantCenterUpdaterDoFn(rubik_options["client_id"], rubik_options["client_secret"],
                                                      rubik_options["access_token"], rubik_options["refresh_token"], rubik_options['rubik_custom_label']))
                 )


if __name__ == "__main__":
    logger().info("Starting Rubik execution")
    config_file = str(sys.argv[1:][0])
    Rubik(config_file)
