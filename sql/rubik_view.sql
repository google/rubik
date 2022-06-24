-- Template for creating the required view for Rubik on BigQuery.

CREATE OR REPLACE VIEW `megalista-robsantos-340012.rubik_mc_test.rubik_view` AS (
    WITH
        ProductTable AS (
            SELECT *, DATE(_PARTITIONTIME) AS `date`
            FROM `megalista-robsantos-340012.rubik_mc_test.Products_*`
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