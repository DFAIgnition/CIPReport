SELECT id FROM cip_report.dbo.history_events
WHERE 	circuit_id = :circuit_id 
AND		time_start >= DATEADD(MILLISECOND, -1000, :time_start )
AND 	time_start <= DATEADD(MILLISECOND, 1000,  :time_start );