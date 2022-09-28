-- Average track length per album
CREATE VIEW view_avg_track_len_per_album AS
	SELECT
		artist.artist_name
		, album.album_name
		, ROUND(
			AVG(track.duration_ms) / 1000.0 / 60
			, 1
			) AS average_track_duration_min
	FROM track
	LEFT JOIN album
		ON album.album_id = track.album_id
	LEFT JOIN artist
		ON album.artist_id = artist.artist_id
	WHERE album_name IS NOT NULL
	GROUP BY album_name
	ORDER BY AVG(track.duration_ms) DESC
;