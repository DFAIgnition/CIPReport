SELECT 			s.name as 'System',
				l.name as 'Line',
				c.name as 'Circuit',
				c.description as 'Description',
				c.id as 'circuit_id',
				h.*		

FROM 			cip_report.dbo.history_events as h

INNER JOIN 		cip_report.dbo.circuit AS c ON h.circuit_id = c.id
INNER JOIN 		cip_report.dbo.line AS l ON l.id = c.line_id
INNER JOIN 		cip_report.dbo.system AS s ON s.id = l.system_id

WHERE			(:site_id IS NULL OR :site_id='' OR :site_id=0 OR s.site_id = :site_id)
AND				(:system_id IS NULL OR :system_id='' OR :system_id=0 OR s.id = :system_id)
AND				(:line_id IS NULL OR :line_id='' OR :line_id=0 OR l.id = :line_id)
AND				(:circuit_id IS NULL OR :circuit_id='' OR :circuit_id=0 OR c.id = :circuit_id)
ORDER BY 		h.time_end DESC