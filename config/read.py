# import pyyaml module
import yaml
from yaml.loader import SafeLoader
from utils.logger import logger
from merchant.offer import RubikOffer, RubikCsvFields

"""
Read functions

#TODO Improvements:
    - Read functions could be on different module
    - Read from CSV function can have a better definition __dict__ from class
"""


def read_from_yaml(file_name="rubik.yaml"):
    logger().info(f"Attempting to read YAML: {file_name}")
    try:
        with open(file_name) as f:
            data = yaml.load(f, Loader=SafeLoader)
        logger().debug("Read yaml with data: " + str(data))
        return data
    except Exception as ex:
        logger().error("Error when attempting to read yaml: " + str(ex))
        raise ex


def rubik_offer_from_csv_line(line: str) -> RubikOffer:
    fields = line.split(",")
    product_id = f"{fields[RubikCsvFields.CHANNEL]}:{fields[RubikCsvFields.CONTENT_LANGUAGE]}:{fields[RubikCsvFields.TARGET_COUNTRY]}:{fields[RubikCsvFields.OFFER_ID]}"
    additional_image_links = fields[RubikCsvFields.ADDITIONAL_IMAGE_LINKS].split(
        RubikCsvFields.ADDITIONAL_IMAGE_LINKS_SEPARATOR
    )
    return RubikOffer(
        product_id,
        fields[RubikCsvFields.MERCHANT_ID],
        fields[RubikCsvFields.IMAGE_LINK],
        additional_image_links,
    )


def rubik_offer_from_big_query_row(row):
    product_id = f"{row['channel']}:{row['content_language']}:{row['target_country']}:{row['offer_id']}"
    merchant_id = f"{row['merchant_id']}"
    image_link = row["image_link"]
    additional_image_links = row["additional_image_links"]
    return RubikOffer(product_id, merchant_id, image_link, additional_image_links)
