UPDATE cip_report.dbo.history_events

SET 
    notes = 			:note,
    updated_at = 		GETDATE(),
    updated_by = 		:updated_by
    
WHERE id = :id;
