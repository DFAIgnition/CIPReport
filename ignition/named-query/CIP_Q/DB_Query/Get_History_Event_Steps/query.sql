SELECT 			s.name as 'System',
				l.name as 'Line',
				c.name as 'Circuit',
				c.description as 'Description',
				hs.*
		

FROM 			cip_report.dbo.history_events_steps as hs

INNER JOIN 		cip_report.dbo.history_events AS he ON he.id = hs.event_id
INNER JOIN 		cip_report.dbo.circuit AS c ON he.circuit_id = c.id
INNER JOIN 		cip_report.dbo.line AS l ON l.id = c.line_id
INNER JOIN 		cip_report.dbo.system AS s ON s.id = l.system_id

WHERE			(hs.event_id =  :event_id )
AND 			hs.duration> :filter