SELECT 			st.*

FROM 			cip_report.dbo.step_type as st

WHERE			(:site_id IS NULL OR st.site_id = :site_id)