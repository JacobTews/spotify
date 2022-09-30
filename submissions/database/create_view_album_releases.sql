CREATE VIEW view_top_release_months AS
	SELECT
		CASE 
			WHEN STRFTIME("%m", release_date) == "01"
				THEN "01 - January"
			WHEN STRFTIME("%m", release_date) == "02"
				THEN "02 - February"
			WHEN STRFTIME("%m", release_date) == "03"
				THEN "03 - March"
			WHEN STRFTIME("%m", release_date) == "04"
				THEN "04 - April"
			WHEN STRFTIME("%m", release_date) == "05"
				THEN "05 - May"
			WHEN STRFTIME("%m", release_date) == "06"
				THEN "06 - June"
			WHEN STRFTIME("%m", release_date) == "07"
				THEN "07 - July"
			WHEN STRFTIME("%m", release_date) == "08"
				THEN "08 - August"
			WHEN STRFTIME("%m", release_date) == "09"
				THEN "09 - September"
			WHEN STRFTIME("%m", release_date) == "10"
				THEN "10 - October"
			WHEN STRFTIME("%m", release_date) == "11"
				THEN "11 - November"	
			WHEN STRFTIME("%m", release_date) == "12"
				THEN "12 - December"	
		END
			AS release_month
		, PRINTF("%-d", COUNT(*)) AS num_releases
	FROM album
	-- since some albums only have a release year, they default to 1 January of that year; we'll remove those for this analysis
	WHERE STRFTIME("%m-%d", release_date) != "01-01"
	GROUP BY release_month
	ORDER BY num_releases DESC
;