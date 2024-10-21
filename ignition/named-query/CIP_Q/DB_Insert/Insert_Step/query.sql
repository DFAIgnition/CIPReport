
INSERT INTO cip_report.dbo.step
(
    step_type_id,
    step_number,
    step_description, 
    updated_at,
    updated_by

) 

VALUES 

(
    :step_type_id, 
    :step_number,
    :step_description, 
    GETDATE(),
    :updated_by

);