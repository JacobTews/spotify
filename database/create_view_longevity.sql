CREATE VIEW view_longevity_award AS
	SELECT
		artist.artist_name
		, STRFTIME("%Y", MIN(album.release_date)) AS earliest_release_yr
		, STRFTIME("%Y", MAX(album.release_date)) AS recent_release_yr
		, CAST(STRFTIME("%Y", MAX(album.release_date)) AS INTEGER) - 
			CAST(STRFTIME("%Y", MIN(album.release_date)) AS INTEGER) as longevity_yrs
	FROM album
	LEFT JOIN artist
		ON artist.artist_id = album.artist_id
	GROUP BY artist_name
	ORDER BY longevity_yrs DESC
;