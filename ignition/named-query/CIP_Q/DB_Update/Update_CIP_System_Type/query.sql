UPDATE cip_report.dbo.system_type

SET name = 			:name,
    description = 	:description,
    updated_at = 	GETDATE(),
    updated_by = 	:updated_by
    
WHERE id = :id; 