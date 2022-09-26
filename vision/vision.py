from oauthlib.oauth2.rfc6749.endpoints import base
import google.oauth2.credentials as oauth2_credentials
from google.auth import credentials as ga_credentials
from google.cloud import vision
from google.cloud.vision import Image
from urllib.request import urlopen
import base64
from merchant.rubik_product import RubikProduct

from google.auth.transport.requests import Request
from utils.logger import logger


class Vision:
    def __init__(self, config):
        self._access_token = config['access_token']
        self._refresh_token = config['refresh_token']
        self._client_id = config['client_id']
        self._client_secret = config['client_secret']
        self._token_uri = 'https://accounts.google.com/o/oauth2/token'
    
    def get_api_client(self):
        scopes = [
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/cloud-platform.read-only',
            'https://www.googleapis.com/auth/cloud-vision'
        ]
        credentials = oauth2_credentials.Credentials(
          self._access_token,
          refresh_token=self._refresh_token,
          token_uri=self._token_uri,
          client_id=self._client_id,
          client_secret=self._client_secret,
          scopes=scopes)
        credentials.refresh(Request())
        return vision.ImageAnnotatorClient(credentials=credentials)

    def read_image(self, url: str) -> str:
        response = urlopen(url)
        img_binary = response.read()
        return base64.b64encode(img_binary).decode('ascii')
    
    def score_image(self, url: str):
        client = self.get_api_client()

        base64str = self.read_image(url)
        image = Image(content=base64str)

        logo_object = client.logo_detection(
            image=image)
        logo_object = logo_object.logo_annotations if logo_object else []

        multiple_object = client.object_localization(
            image=image).localized_object_annotations

        text_object = client.text_detection(
            image=image)
        text_object = text_object.text_annotations if text_object else []
        return (len(logo_object) * 5 + len(multiple_object) + len(text_object) * 2)

    def find_best_image(self, product: RubikProduct) -> RubikProduct:
        logger(self.__class__.__name__).info("Analysing offer...")
        best_score = 0
        score = self.score_image(product.image_link)
        logger(self.__class__.__name__).info(f"Score for actual image: {score}")
        best_score = score
        for additional_image in product.additional_image_links:
            score = self.score_image(additional_image)
            logger(self.__class__.__name__).info(f"Score for aditional image {additional_image}: {score}")
            if score < best_score:
                product.image_link = additional_image
                best_score = score
        return product
