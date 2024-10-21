SELECT 			l.*,s.name as system_name

FROM 			cip_report.dbo.line as l

INNER JOIN 		cip_report.dbo.system AS s ON s.id = l.system_id

WHERE			(:site_id IS NULL OR s.site_id = :site_id)
AND				(:system_id IS NULL OR :system_id='' OR :system_id=0 OR s.id = :system_id)
AND				(:line_id IS NULL OR :line_id='' OR :line_id=0 OR l.id = :line_id)
