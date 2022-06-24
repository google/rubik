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

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from rubik_lib.merchant_center_uploader import MerchantCenterUpdaterDoFn
from rubik_lib.rubik_options import RubikOptions
from rubik_lib.rubik_product import RubikProduct, rubik_product_from_csv_line, rubik_product_from_big_query_row


class BatchElements(beam.DoFn):
    def __init__(self, batch_size: int):
        self._batch_size = batch_size

    def process(self, grouped_elements: Tuple[str, Iterable[RubikProduct]]) -> Tuple[str, List[RubikProduct]]:
        merchant_id = grouped_elements[0]
        batch: List[RubikProduct] = []
        for i, element in enumerate(grouped_elements[1]):
            if i != 0 and i % int(self._batch_size.get()) == 0:
                yield merchant_id, batch
                batch = []
            batch.append(element)
        yield merchant_id, batch


def run(argv=None):
    pipeline_options = PipelineOptions()
    rubik_options = pipeline_options.view_as(RubikOptions)
    with beam.Pipeline(options=pipeline_options) as pipeline:
        if rubik_options.csv is not None:
            (pipeline
             | "Load rows" >> beam.io.ReadFromText(rubik_options.csv)
             | "Map lines to objects" >> beam.Map(rubik_product_from_csv_line)
             | "Build Tuples" >> beam.Map(lambda product: (product.merchant_id, product))
             | "Group by Merchant Id" >> beam.GroupByKey()
             | "Batch elements" >> beam.ParDo(BatchElements(rubik_options.batch_size)).with_output_types(
                        Tuple[str, List[RubikProduct]])
             | "Upload to Merchant Center" >> beam.ParDo(
                        MerchantCenterUpdaterDoFn(rubik_options.client_id, rubik_options.client_secret,
                                                  rubik_options.access_token, rubik_options.refresh_token))
             )
        if rubik_options.bq is not None:
            (pipeline
             | "Load rows" >> beam.io.gcp.bigquery.ReadFromBigQuery(table=rubik_options.bq)
             | "Map rows to objects" >> beam.Map(rubik_product_from_big_query_row)
             | "Build Tuples" >> beam.Map(lambda product: (product.merchant_id, product))
             | "Group by Merchant Id" >> beam.GroupByKey()
             | "Batch elements" >> beam.ParDo(BatchElements(rubik_options.batch_size)).with_output_types(
                        Tuple[str, List[RubikProduct]])
             | beam.ParDo(MerchantCenterUpdaterDoFn(rubik_options.client_id, rubik_options.client_secret,
                                                    rubik_options.access_token, rubik_options.refresh_token)))


if __name__ == "__main__":
    logging.basicConfig(filename='rubik.log', level=logging.INFO)
    run()
