DROP VIEW IF EXISTS view_fastest_tempos
;

CREATE VIEW view_fastest_tempos AS
	WITH tempo_rank_cte AS (
		SELECT DISTINCT
			track.song_name
			, artist.artist_name
			, track_features.tempo
			, DENSE_RANK() OVER (
				PARTITION BY artist_name
				ORDER BY tempo DESC
				) AS song_tempo_rank
		FROM track_features
		LEFT JOIN track
			ON track.track_id = track_features.track_id
		LEFT JOIN album
			ON album.album_id = track.album_id
		LEFT JOIN artist
			ON artist.artist_id = album.artist_id
		WHERE artist_name IS NOT NULL
	)

	SELECT
		song_name
		, artist_name
		, PRINTF(
			"%10.3f"
			, tempo
			) AS tempo
	FROM tempo_rank_cte
	WHERE song_tempo_rank <= 5
;