SELECT 			he.type_event,he.time_start,he.time_end

FROM 			cip_report.dbo.history_events_op as he

WHERE			he.event_id =  :event_id 
