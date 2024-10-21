UPDATE cip_report.dbo.step

SET step_number = 	:step_number,
    updated_at = 	GETDATE(),
    updated_by = 	:updated_by
    
WHERE  :step_type_id  = :step_type_id AND step_description = :step_description ; 