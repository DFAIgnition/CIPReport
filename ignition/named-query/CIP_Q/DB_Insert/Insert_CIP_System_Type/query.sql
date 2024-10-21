INSERT INTO cip_report.dbo.system_type
(
    name, 
    description, 
    updated_at,
    updated_by

) 

VALUES 

(
    :name, 
    :description, 
    GETDATE(),
    :updated_by

);