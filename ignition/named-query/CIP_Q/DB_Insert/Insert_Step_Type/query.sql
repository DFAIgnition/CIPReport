INSERT INTO cip_report.dbo.step_type
(
    site_id, 
    name, 
    description, 
    updated_at,
    updated_by

) 

VALUES 

(
    :site_id, 
    :name, 
    :description, 
    GETDATE(),
    :updated_by

);
