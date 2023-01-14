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

from oauthlib.oauth2.rfc6749.endpoints import base
import google.oauth2.credentials as oauth2_credentials
from google.auth import credentials as ga_credentials
from google.cloud import vision
from google.cloud.vision import Image
from urllib.request import urlopen
import base64
from merchant.offer import RubikOffer

from google.auth.transport.requests import Request
from utils.logger import logger


class Vision:
    def __init__(self, config):
        self._access_token = config["access_token"]
        self._refresh_token = config["refresh_token"]
        self._client_id = config["client_id"]
        self._client_secret = config["client_secret"]
        self._token_uri = "https://accounts.google.com/o/oauth2/token"

    def get_api_client(self):
        scopes = [
            "https://www.googleapis.com/auth/cloud-platform",
            "https://www.googleapis.com/auth/cloud-platform.read-only",
            "https://www.googleapis.com/auth/cloud-vision",
        ]
        credentials = oauth2_credentials.Credentials(
            self._access_token,
            refresh_token=self._refresh_token,
            token_uri=self._token_uri,
            client_id=self._client_id,
            client_secret=self._client_secret,
            scopes=scopes,
        )
        credentials.refresh(Request())
        return vision.ImageAnnotatorClient(credentials=credentials)

    def read_image(self, url: str) -> str:
        """
        Fetch image from url

        #TODO Improvements:
            - It receives a 403 forbidden in some ocasions
            - Error handling

        Args:
            url (str): url to read

        Returns:
            str: base64 image
        """
        response = urlopen(url)
        img_binary = response.read()
        return base64.b64encode(img_binary).decode("ascii")

    def score_image(self, url: str):
        """
        Score image access vision ai and uses a simple formula

        (number of logos * 5) + (number of objects) + (number of texts * 2)

        It worked for almost 83% of offers

        #TODO Improvements:
            - Create a better formula
            - Batch requests

        Args:
            url (str): _description_

        Returns:
            _type_: _description_
        """
        client = self.get_api_client()

        base64str = self.read_image(url)
        image = Image(content=base64str)

        logo_object = client.logo_detection(image=image)
        logo_object = logo_object.logo_annotations if logo_object else []

        multiple_object = client.object_localization(
            image=image
        ).localized_object_annotations

        text_object = client.text_detection(image=image)
        text_object = text_object.text_annotations if text_object else []
        return len(logo_object) * 5 + len(multiple_object) + len(text_object) * 2

    def find_best_image(self, product: RubikOffer) -> RubikOffer:
        """
        After scoring a image, the lowest value for image is the best one

        Args:
            product (RubikOffer): The offer to analyse

        Returns:
            RubikOffer: The offer updated with the best image
        """
        logger(self.__class__.__name__).info("Analysing offer...")
        best_score = 0
        score = self.score_image(product.image_link)
        logger(self.__class__.__name__).info(f"Score for actual image: {score}")
        best_score = score
        for additional_image in product.additional_image_links:
            score = self.score_image(additional_image)
            logger(self.__class__.__name__).info(
                f"Score for aditional image {additional_image}: {score}"
            )
            if score < best_score:
                product.image_link = additional_image
                best_score = score
        return product
