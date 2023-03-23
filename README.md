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


<img src="https://github.com/google/rubik/blob/main/images/rubik_3.png?raw=true" height="400px" width="100%">

## How to Use

### Cloud Version (Automatic, Procfile)

#### Prerequisites

 1. Content API enabled on GCP (Required) - See: https://developers.google.com/shopping-content/guides/quickstart
 2. Machine with python3 (Required)
 3. Merchant Center Admin Acess (Account Access -> Users)
 4. OAuth Desktop Credentials on GCP, with CLIENT_ID and CLIENT_SECRET (Required)
    - Go to API & Services > OAuth Consent Screen > Mark it as Internal, there is no need to fill other fields
    - Then go to API & Services > Credentials > Create Credentials > OAuth Client ID
        - Application Type: Desktop
        - Name: rubik-desktop (can be anything)
 5. Big Query (Optional).

#### Deploy

1 - Prepare the CSV file (follow the sample.CSV) or Bigquery table (follow the sql/rubik_view.sql)

2 - Generate your tokens, the following code should output your Access Token and Secret Access Token to use Merchant Center API:

``` shell
$ git clone https://github.com/google/rubik
$ cd rubik
$ python3 generate_token.py --client_id <OAUTH_CLIENT_ID> --client_secret <OAUTH_CLIENT_SECRET>
```
This command will output refresh and access tokens. Save them to use later on this config.

3 - Edit config files

On a text editor replace the placeholders on the config files:

- To run locally configure run_local.sh 
- To run on Cloud configure Procfile


- GCP_PROJECT_ID: GCP Project ID where Rubik will run.
- GCP REGION: the region, for example: us-central1.
- SERVICE ACCOUNT: can be the defalt one or one special for the project. It needs roles:
- OAUTH_CLIENT_ID
- OAUTH_CLIENT_SECRET
- OAUTH_CLIENT_REFRESH_TOKEN
- BQ_DATASET
- BQ_TABLE
- BUCKET_NAME

3 - Run Rubik locally, look at rubik.log to see the output. Before running the run_local.sh, enter the necessary information:

Using CSV (remember to set option to CSV):

``` python3

$ ./run_local.sh

```
Using Bigquery (remember to set option to BQ):

``` python3

$ ./run_local.sh

```
4 - Create Cloud Run job

- GCP_PROJECT_ID is the GCP Project ID where Rubik will run.
- GCP REGION is the region, for example: us-central1.
- SERVICE ACCOUNT can be the defalt one or one special for the project. It needs roles:
  - roles/bigquery.user
  - roles/cloudscheduler.admin
  - roles/run.invoker
  - roles/run.viewer
  - roles/run.serviceAgent
  - roles/runtimeconfig.admin
  - roles/cloudbuild.builds.editor


``` shell
$ gcloud builds submit --pack=env=GOOGLE_PYTHON_VERSION="3.9.2",image=gcr.io/<GCP_PROJECT ID>/run-rubik
$ gcloud beta run jobs create job-rubik \ 
--image gcr.io/<GCP_PROJECT ID>/run-rubik \
--max-retries 2 \
--region <GCP REGION> \
--service-account=<SERVICE ACCOUNT> \
--execute-now 

```

When the last command finish running an URL will be written on screen. This will take you to the executing Cloud Run Job.

5 - Schedule execution
To do this, we create a Cloud Scheduler job with the Cloud Run job as a target.

SCHEDULER_JOB_NAME 
TIMEZONE is in format: America/Buenos_Aires
Schedule is in CRON format. For example daily at 00.00hs : 0 0 * * *

``` shell
gcloud scheduler jobs create http <SCHEDULER_JOB_NAME> \
  --location <GCP REGION> \
  --schedule="<SCHEDULE>" \
  --time-zone="<TIMEZONE>" \
  --uri="https://<GCP REGION>-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/<GCP_PROJECT ID>/jobs/job-rubik:run" \
  --http-method POST \
  --oauth-service-account-email <SERVICE ACCOUNT>
```


### Troubleshooting

### Comming Soon

- Vision AI Integration - See docs: https://cloud.google.com/vision
- Sheets Docs Version in English

### Questions or Suggestions?

Please use the Discussions tab, we will respond :)


