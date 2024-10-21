SELECT			s.step_description

FROM			cip_report.dbo.step as s

INNER JOIN 		cip_report.dbo.circuit AS c ON s.step_type_id = c.step_type_id

WHERE			c.id =  :circuit_id AND s.step_number =  :step_number 