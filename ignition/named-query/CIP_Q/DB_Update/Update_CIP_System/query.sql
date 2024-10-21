UPDATE cip_report.dbo.system

SET name = 			:name,
    description = 	:description,
    type_id = 		:type_id,
    updated_at = 	GETDATE(),
    updated_by = 	:updated_by
    
WHERE id = :id; 