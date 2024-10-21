SELECT 			TOP 1 st.id
FROM 			cip_report.dbo.step_type as st

WHERE			(st.site_id = :site_id)
AND				(:name IS NULL OR st.name = :name)