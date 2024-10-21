INSERT INTO cip_report.dbo.system
(
    site_id, 
    name, 
    description, 
    type_id,
    updated_at,
    updated_by

) 

VALUES 

(
    :site_id, 
    :name, 
    :description, 
    :type_id,
    GETDATE(),
    :updated_by

);
