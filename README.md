# Rubik

Rubik is an algorithm that reads Merchant Center feed and try to approve reproved offers by image.

The main image is reproved, but the additional images can be approved. Rubik will try every additional image from each offer and update them automatically

## How it Works?

The Problem

When uploading new offers on Merchant Center, the Main Image may contain logos, additional text or any other component that will reprove the offer on the near future and can be fixed by a new upload (Please see: https://support.google.com/merchants/answer/6101131?hl=en).

How to Avoid this Problem

Every Offer need to follow Merchant Center Guidelines to have a better long-term performance: https://support.google.com/merchants/answer/6324350?hl=en#:~:text=We%20recommend%20images%20of%20at%20least%20800%20x%20800%20pixels.&text=Frame%20your%20product%20in%20the,%25%2C%20of%20the%20full%20image.

Rubik

Rubik aims to resolve "The Problem" by selecting reproved offers by image and re-inserting them on Merchant Center automatically. 

![Rubik Example](images/rubik_1.png?raw=true "Rubik Example")

## Deploy

### Prerequisites

 - Merchant Center API enabled on GCP
 - A local or virtual machine with python3
 - OAuth Credentials on GCP, with CLIENT_ID and CLIENT_SECRET
 - Big Query, if you don't want to use a CSV

### Deploy

1 - Prepare the CSV file (follow the sample.CSV) or Bigquery table (follow the sql/rubik_view.sql)

2 - Generate your tokens, the following code should output your Access Token and Secret Access Token to use Merchant Center API:

``` shell
git clone https://github.com/google/rubik
cd rubik
python3 generate_token.py --client_id <GCP_CLIENT_ID> --client_secret <GCP_CLIENT_SECRET>
```

3 - Execute Rubik, look at rubik.log to see the output:

Using CSV:

``` python3

python3 main.py --runner DirectRunner --csv=sample.csv --client_id=<YOUR_CLIENT_ID>  --client_secret=<YOUR_CLIENT_SECRET> --access_token=<YOUR_ACCESS_TOKEN> --refresh_token=<YOUR_REFRESH_TOKEN>

```
Using Bigquery:

``` python3

python3 main.py --runner DirectRunner --csv=sample.csv --client_id=<YOUR_CLIENT_ID>  --client_secret=<YOUR_CLIENT_SECRET> --access_token=<YOUR_ACCESS_TOKEN> --refresh_token=<YOUR_REFRESH_TOKEN>

```



