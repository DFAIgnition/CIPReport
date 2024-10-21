UPDATE cip_report.dbo.step_type

SET description = 	:description,
    updated_at = 	GETDATE(),
    updated_by = 	:updated_by
    
WHERE id = :id; 