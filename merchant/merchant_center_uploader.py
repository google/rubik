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

from datetime import datetime
from typing import List, Tuple

import apache_beam as beam
import json
import logging
from apache_beam.options.value_provider import ValueProvider
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from merchant.offer import RubikOffer

logger = logging.getLogger("rubik")

class MerchantCenterUpdaterDoFn(beam.DoFn):
    """
      This uploader handles a batch of product updates for the Content API.
      """

    def __init__(self, client_id: ValueProvider, client_secret: ValueProvider, access_token: ValueProvider,
                 refresh_token: ValueProvider, custom_label: ValueProvider) -> None:
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.custom_label = custom_label

    def _get_merchant_center_service(self):
        credentials = Credentials(
            token=self.access_token,
            refresh_token=self.refresh_token,
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_uri='https://accounts.google.com/o/oauth2/token',
            scopes=[
                'https://www.googleapis.com/auth/content'
            ])

        service = build('content', 'v2.1', credentials=credentials)
        return service

    def start_bundle(self):
        pass

    def process(self, batch: Tuple[str, List[RubikOffer]], **kwargs):
        try:
            merchant_id, products = batch
            request_body = {
                'entries': [{
                    'batchId': i,
                    'merchantId': merchant_id,
                    'productId': product.product_id,
                    'method': 'update',
                    'updateMask': f'imageLink,additionalImageLinks,{self.custom_label}',
                    'product': {
                        'imageLink': product.image_link,
                        'additionalImageLinks': product.additional_image_links,
                        f'{self.custom_label}': 'rubik'
                    }
                } for i, product in enumerate(products)]
            }

            logger.info(f"Making request: {request_body}")

            request = self._get_merchant_center_service().products().custombatch(body=request_body)
            result = request.execute()

            if result['kind'] == 'content#productsCustomBatchResponse':
                entries = result['entries']
                for entry in entries:
                    product = entry.get('product')
                    errors = entry.get('errors')
                    if product:
                        logger.info(f"Product {product['id']} was updated.")
                    elif errors:
                        logger.error(f"Errors for batch entry {entry['batchId']}:")
                        logger.error(json.dumps(errors, sort_keys=True, indent=2, separators=(',', ': ')))
            else:
                logger.error(f"There was an error. Response: {result}")
        except Exception as ex:
            logger.error(ex)
