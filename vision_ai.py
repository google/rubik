from oauthlib.oauth2.rfc6749.endpoints import base
import google.oauth2.credentials as oauth2_credentials
from google.auth import credentials as ga_credentials
from google.cloud import vision
from google.cloud.vision import Image

from google.auth.transport.requests import Request


# pip3.7 install --upgrade google-cloud-vision

def localize_objects(base64str: str):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    client = get_api_client()

    image = Image(content=base64str)

    logo_object = client.logo_detection(
        image=image)
    logo_object = logo_object.logo_annotations if logo_object else []
    print(f"Logos: {len(logo_object)}")

    multiple_object = client.object_localization(
        image=image).localized_object_annotations

    print(f"Multiple Objects {len(multiple_object)}")

    text_object = client.text_detection(
        image=image)
    text_object = text_object.text_annotations if text_object else []
    print(f"Texts: {len(text_object)}")

    print(f"Total classification: {len(logo_object) * 5 + len(multiple_object) + len(text_object) * 2}")
    
    #print(objects)
    # print('Number of objects found: {}'.format(len(objects)))
    # for object_ in objects:
    #     print('\n{} (confidence: {})'.format(object_.name, object_.score))
    #     print('Normalized bounding polygon vertices: ')
    #     for vertex in object_.bounding_poly.normalized_vertices:
    #         print(' - ({}, {})'.format(vertex.x, vertex.y))

def get_api_client():


  scopes = [
      'https://www.googleapis.com/auth/cloud-platform',
      'https://www.googleapis.com/auth/cloud-platform.read-only',
      'https://www.googleapis.com/auth/cloud-vision'
  ]
  credentials = oauth2_credentials.Credentials(
    access_token,
    refresh_token=refresh_token,
    token_uri=token_uri,
    client_id=client_id,
    client_secret=client_secret,
    scopes=scopes)
  credentials.refresh(Request())
  
  return vision.ImageAnnotatorClient(credentials=credentials)

def read_image(url: str) -> str:
  from urllib.request import urlopen
  import base64
  # Urlopen travado com https://images-submarino.b2w.io/produtos/5261042428/imagens/ssd-kingston-a400-240gb-sata-leitura-500mb-s-gravacao-350mb-s-sa400s37-240g/5261042428_1_xlarge.jpg
  response = urlopen(url)
  img_binary = response.read()
  return base64.b64encode(img_binary).decode('ascii')

base64_img = read_image('https://a-static.mlcdn.com.br/1500x1500/cama-box-bau-casal-colchao-mola-ensacada-138x188x72cm-preto-blue-votobox/votobox/12931741132/ebfa79d067db6c19c414a0cb67db4b39.jpg')
localize_objects(base64_img)