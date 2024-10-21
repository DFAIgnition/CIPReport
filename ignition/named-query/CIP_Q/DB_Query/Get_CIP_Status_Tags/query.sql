SELECT 			site_id as site, s.id as system,l.id as line, c.id as circuit,l.cmd_advance,l.cmd_pause,l.cmd_hold,l.cmd_resume,l.type_sanitizer,l.type_acid,l.type_caustic,l.type_alkaline,
				c.step_number,c.state_idle,c.state_running,c.state_paused,c.state_held,c.state_completed,c.state_stopped,
				l.supply_temp_transmitter,l.supply_flow_transmitter,l.supply_press_transmitter,l.supply_cond_transmitter,
				l.return_temp_transmitter,l.return_flow_transmitter,l.return_press_transmitter,l.return_cond_transmitter

FROM 			cip_report.dbo.circuit as c

INNER JOIN 		cip_report.dbo.line AS l ON l.id = c.line_id
INNER JOIN 		cip_report.dbo.system AS s ON s.id = l.system_id

WHERE			(:site_id IS NULL OR :site_id='' OR :site_id=0 OR s.site_id = :site_id)
AND				(:system_id IS NULL OR :system_id='' OR :system_id=0 OR s.id = :system_id)
AND				(:line_id IS NULL OR :line_id='' OR :line_id=0 OR l.id = :line_id)
AND				(:circuit_id IS NULL OR :circuit_id='' OR :circuit_id=0 OR c.id = :circuit_id)