# <img src="https://github.com/google/rubik/blob/main/images/rubik_logo.png?raw=true" width="100%" height="20%">

Rubik is an algorithm that reads Merchant Center feed and try to approve reproved offers by image.

The main image is reproved, but the additional images can be approved. Rubik will try every additional image from each offer and update them automatically

## How it Works?

### The Problem

When uploading new offers on Merchant Center, the Main Image may contain logos, additional text or any other component that will reprove the offer on the near future and can be fixed by a new upload (Please see: https://support.google.com/merchants/answer/6101131?hl=en).

### How to Avoid this Problem

Every Offer need to follow Merchant Center Guidelines to have a better long-term performance: [Merchant Center Guidelines](https://support.google.com/merchants/answer/6324350?hl=en#:~:text=We%20recommend%20images%20of%20at%20least%20800%20x%20800%20pixels.&text=Frame%20your%20product%20in%20the,%25%2C%20of%20the%20full%20image).

### Rubik

Rubik aims to resolve "The Problem" by selecting reproved offers by image and re-inserting them on Merchant Center automatically. 


![Rubik Present](images/rubik_3.png?raw=true "Rubik Present")

#### Demo with Vision AI

In this demo, Rubik replace the main reproved image with a better image using Vision AI:

![Rubik Example](images/rubik_example.gif?raw=true "Rubik Example")

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
 6. Google Cloud Storage - Bucket created (Required)
 7. Google Cloud Vision AI - Enabled on your GCP project (Required) (https://cloud.google.com/vision)

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

### Questions or Suggestions?

Please use the Discussions tab, we will respond :)


