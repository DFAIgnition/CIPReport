SELECT 			st.id,st.site_id,st.name,st.description,s.step_number,s.step_description

FROM 			cip_report.dbo.step_type as st

INNER JOIN 		cip_report.dbo.step AS s ON st.id = s.step_type_id

WHERE			(:site_id IS NULL OR st.site_id = :site_id)
AND				(:name IS NULL OR st.name = :name)