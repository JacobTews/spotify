CREATE VIEW view_longest_tracks AS
	WITH long_cte AS (
		SELECT DISTINCT
			artist.artist_name
			, track.song_name
			, track.duration_ms
			, DENSE_RANK() OVER (
				PARTITION BY artist_name
				ORDER BY duration_ms DESC
				) AS song_rank
		FROM track
		LEFT JOIN album
			ON album.album_id = track.album_id
		LEFT JOIN artist
			ON artist.artist_id = album.artist_id
		WHERE artist_name IS NOT NULL
		ORDER BY artist_name, duration_ms DESC
	)

	SELECT
		artist_name
		, song_name
		, duration_ms
	FROM long_cte
	WHERE song_rank <= 5
;