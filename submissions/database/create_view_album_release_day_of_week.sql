CREATE VIEW view_album_release_dow AS
	WITH release_count_cte AS (
		SELECT
			CASE
				WHEN STRFTIME("%w", release_date) == "0"
					THEN 'Sunday'
				WHEN STRFTIME("%w", release_date) == "1"
					THEN 'Monday'
				WHEN STRFTIME("%w", release_date) == "2"
					THEN 'Tuesday'
				WHEN STRFTIME("%w", release_date) == "3"
					THEN 'Wednesday'
				WHEN STRFTIME("%w", release_date) == "4"
					THEN 'Thursday'
				WHEN STRFTIME("%w", release_date) == "5"
					THEN 'Friday'
				WHEN STRFTIME("%w", release_date) == "6"
					THEN 'Saturday'
			END AS release_day_of_week
			, COUNT(*) AS num_releases
		FROM album
		-- since some albums only have a release year, they default to 1 January of that year; we'll remove those for this analysis
		WHERE STRFTIME("%m-%d", release_date) != "01-01"
		GROUP BY release_day_of_week
	)

	SELECT
		release_day_of_week
		, num_releases
		, ROUND(
			CAST(num_releases AS REAL) / (SELECT SUM(num_releases) FROM release_count_cte) * 100.0
			, 2
			) AS percent_of_total
	FROM release_count_cte
	ORDER BY num_releases DESC
;