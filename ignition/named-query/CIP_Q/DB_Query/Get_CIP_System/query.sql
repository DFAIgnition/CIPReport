SELECT 			*

FROM 			cip_report.dbo.system as s

WHERE			(:site_id IS NULL OR s.site_id = :site_id)
