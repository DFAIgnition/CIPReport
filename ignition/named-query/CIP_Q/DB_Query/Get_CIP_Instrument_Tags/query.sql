SELECT 			c.step_number as step_number,c.step_number as step_description,
				l.supply_temp_transmitter,l.supply_flow_transmitter,l.supply_press_transmitter,l.supply_cond_transmitter,
				l.return_temp_transmitter,l.return_flow_transmitter,l.return_press_transmitter,l.return_cond_transmitter,
				l.supply_temp_switch,l.supply_flow_switch,l.supply_press_switch,l.supply_cond_switch,
				l.return_temp_switch,l.return_flow_switch,l.return_press_switch,l.return_cond_switch

FROM 			cip_report.dbo.circuit as c

INNER JOIN 		cip_report.dbo.line AS l ON l.id = c.line_id
INNER JOIN 		cip_report.dbo.system AS s ON s.id = l.system_id

WHERE			(:circuit_id IS NULL OR :circuit_id='' OR :circuit_id=0 OR c.id = :circuit_id)