DROP VIEW IF EXISTS view_top_artists
;

CREATE VIEW view_top_artists AS
	SELECT
		artist_name
		, PRINTF("%,d", followers) AS num_followers
	FROM artist
	ORDER BY followers DESC
;