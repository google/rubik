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


from apache_beam.options.pipeline_options import PipelineOptions


class RubikOptions(PipelineOptions):
    """This Class configures the command line options that can be passed to the pipeline."""

    @classmethod
    def _add_argparse_args(cls, parser):
        # OAUTH
        parser.add_value_provider_argument(
            '--client_id', help='Client Id for the Google APIs')
        parser.add_value_provider_argument(
            '--client_secret', help='Client Secret for the Google APIs')
        parser.add_value_provider_argument(
            '--refresh_token', help='OAUTH Refresh Token for the Google APIs')
        parser.add_value_provider_argument(
            '--access_token', help='OAUTH Access Token for the Google APIs')
        # INPUT
        parser.add_argument(
            '--csv', help='Local CSV file with Product Data')
        parser.add_argument(
            '--bq', help='BigQuery table with product data. Specify in format project:dataset.table')
        # BATCH
        parser.add_value_provider_argument(
            '--batch_size', default=8000, help='Uri for the BigQuery Table in the format project.dataset.table')
