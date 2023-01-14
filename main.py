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


from typing import Tuple, List
import sys

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from merchant.merchant_center_uploader import MerchantCenterUpdaterDoFn
from merchant.offer import BatchOffers, RubikOffer
from utils.logger import logger
from config.read import (
    read_from_yaml,
    rubik_offer_from_csv_line,
    rubik_offer_from_big_query_row,
)
from vision.vision import Vision

"""Rubik's main module

#TODO Improvements:
    - Create a separate class for Rubik
    - Create getters and setters
    - For each read_option, assign to a different method
"""


class Rubik:
    def __init__(self, config_file):
        config = read_from_yaml(config_file)
        pipeline_options = PipelineOptions()
        rubik_options = config
        with beam.Pipeline(options=pipeline_options) as pipeline:
            if rubik_options["csv_file"] is not None:
                process = (
                    pipeline
                    | "Load rows" >> beam.io.ReadFromText(rubik_options["csv_file"])
                    | "Map lines to objects" >> beam.Map(rubik_offer_from_csv_line)
                )
            elif rubik_options["big_query"] is not None:
                process = (
                    pipeline
                    | "Load rows"
                    >> beam.io.gcp.bigquery.ReadFromBigQuery(
                        table=rubik_options["big_query"],
                        gcs_location=rubik_options["big_query_gcs_location"],
                    )
                    | "Map rows to objects" >> beam.Map(rubik_offer_from_big_query_row)
                )
            if rubik_options["vision_ai"] is True:
                process | "Vision AI to select best image" >> beam.Map(
                    Vision(config).find_best_image
                )
            (
                process
                | "Build Tuples"
                >> beam.Map(lambda product: (product.merchant_id, product))
                | "Group by Merchant Id" >> beam.GroupByKey()
                | "Batch elements"
                >> beam.ParDo(
                    BatchOffers(rubik_options["batch_size"])
                ).with_output_types(Tuple[str, List[RubikOffer]])
                | "Upload to Merchant Center"
                >> beam.ParDo(
                    MerchantCenterUpdaterDoFn(
                        rubik_options["client_id"],
                        rubik_options["client_secret"],
                        rubik_options["access_token"],
                        rubik_options["refresh_token"],
                        rubik_options["rubik_custom_label"],
                    )
                )
            )


if __name__ == "__main__":
    logger().info("Starting Rubik execution")
    config_file = str(sys.argv[1:][0])
    Rubik(config_file)
