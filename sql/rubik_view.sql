-- 
-- Copyright 2022 Google Inc.
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at 
-- 
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
-- Template for creating the required table for Rubik on BigQuery.


CREATE OR REPLACE TABLE `project.dataset.tablename` AS (
    WITH
        ProductTable AS (
            SELECT *, DATE(_PARTITIONTIME) AS `date`
            FROM `project.dataset.Products_*`
        ),
        TodayProducts AS (
            SELECT *
            FROM ProductTable
            WHERE `date` = (SELECT MAX(`date`) FROM ProductTable) 
            ),
        ProductsWithImageIssues AS (
            SELECT
                offer_id,
                merchant_id,
                channel,
                content_language,
                target_country,
                image_link,
                (
                    SELECT
                        ARRAY_AGG(additional_image_link)
                    FROM
                        UNNEST(additional_image_links) AS additional_image_link
                    WHERE
                        image_link != additional_image_link 
                ) AS additional_image_links,
                issue
            FROM
                TodayProducts,
                TodayProducts.issues AS issue
            WHERE
                issue.short_description = "Promotional overlay on image [image link]"
        ),
        ProductsWithAdditionalImages AS (
            SELECT *
            FROM ProductsWithImageIssues
            WHERE ARRAY_LENGTH(additional_image_links) > 0 
        )
    SELECT
        offer_id,
        merchant_id,
        channel,
        content_language,
        target_country,
        additional_image_links[SAFE_OFFSET(0)] AS image_link,
        ARRAY_CONCAT((
            SELECT
            ARRAY_AGG(additional_image_link)
            FROM
            UNNEST(additional_image_links) AS additional_image_link
            WHERE
            additional_image_link != additional_image_links[SAFE_OFFSET(0)]), [image_link]) AS additional_image_links
    FROM ProductsWithAdditionalImages
);
