# Rubik

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

Rubik is a open-source solution that enables Merchant Center users to improve their offers. It can improve reproved offers or actual ones, with best Merchant Center guidelines. (https://support.google.com/merchants/answer/6101131?hl=en)

## How it Works?

### Fix Offers

Merchant Center offers can be reproved by a number of factors, Rubik aims to find those factors and fix it.
The errors that Rubik aims to solve:

- Offers reproved by Image
- Offers reproved by GTIN

#### Offers reproved by Image

Rubik will select reproved offers and re-inserting them on Merchant Center automatically with different images from the same offer

![Rubik Present](images/rubik_3.png?raw=true "Rubik Present")

##### Demo with Vision AI

In this demo, Rubik replace the main reproved image with a better image using Vision AI:

![Rubik Example](images/rubik_example.gif?raw=true "Rubik Example")

#### Offers reproved by GTIN

Rubik will clean the offer GTIN, this could lead to another error (Required GTIN) but in most cases that offer will be approved.


## How to Use

### Sheets Version (Manual)

1. Copy this Spreadsheet: [Rubik - Spreadsheet Version](https://docs.google.com/spreadsheets/d/1V9Sim1E6waqWJaqppjDDuhgfYQqUKTXkcF-zGQXOBIA/copy?usp=sharing)
2. Read this Documentation: [Rubik - Spreadsheet Version Docs](https://docs.google.com/document/d/1q7rgzG88ZS9-SKSItI4H1DPsXmmNDDfr1V_VaQNEpZ8/copy)
3. Merchant Center Admin Acess (Account Access -> Users)
4. If you have any questions, please reach out in Discussions tab


### Cloud Version (Automatic)

#### Prerequisites

 1. Content API - Enabled on GCP (Required) - See: https://developers.google.com/shopping-content/guides/quickstart
 2. Machine with Docker and Python3+ (Required)
 3. Merchant Center Admin Acess (Account Access -> Users), your user need to be MCA admin and with validated status
 4. OAuth Desktop Credentials on GCP, with CLIENT_ID and CLIENT_SECRET (Required)
    - Go to API & Services > OAuth Consent Screen > Mark it as Internal, there is no need to fill other fields
    - Then go to API & Services > Credentials > Create Credentials > OAuth Client ID
        - Application Type: Desktop
        - Name: rubik-desktop (can be anything)
 5. Google Big Query - Enabled (Required)
    - Rubik will read from your dataset. You need to have Bigquery's Merchant Center data transfer running: https://cloud.google.com/bigquery/docs/merchant-center-transfer
 6. Google Cloud Storage - Bucket created (Required)
 7. Google Cloud Vision AI - Enabled on your GCP project (Required if you want to use Vision AI) (https://cloud.google.com/vision)

#### Example

Assuming that you have 100 offers with each offer having 6 images and the main image (first) is reproved.

1 - The rubik_view.sql will find those 100 offers and will rotate the first image of each offer with the second one, so the second one will be the main image
2 - If you don't want to use vision ai it will send all offers with the second offer being the main image. However, if you want to use vision AI it will score all images and chose the best one (from 2 to 6)
3 - The output should be a offer updated with a different image, use the custom_label to see if that image will be approved and displayed into Google Ads.

#### Test

1 - Prepare the CSV file (follow the sample.CSV) or Bigquery table (follow the sql/rubik_view.sql)


2 - Generate your tokens, the following code should output your Access Token and Secret Access Token to use Merchant Center API:

``` shell
git clone https://github.com/google/rubik
cd rubik
python3 generate_token.py --client_id <GCP_CLIENT_ID> --client_secret <GCP_CLIENT_SECRET>
```

3 - Fill rubik.yaml file with your values. If CSV file is informed, it will execute only the CSV file.

4 - Run:

``` python3

python3.7 main.py rubik.yaml

```

#### Deploy

1 - Use the following, don't forget to check if rubik.yaml and your gcp-rubik-project is configured:

``` docker

docker build --no-cache . -t rubik:latest
docker run --rm rubik:latest

```


### Troubleshooting

### Comming Soon

- Better model for Vision AI
- Rubik for Kubernetes (daily execution deploy)
- Version with service account

### Questions or Suggestions?

Please use the Discussions tab, we will respond :)


