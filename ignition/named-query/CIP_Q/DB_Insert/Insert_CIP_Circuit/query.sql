INSERT INTO cip_report.dbo.circuit
(
    line_id, 
    name, 
    description, 
    step_number, 
    step_type_id,
    state_idle, 
    state_running, 
    state_held, 
    state_completed, 
    state_stopped, 
    state_paused,
    updated_at,
    updated_by

) 

VALUES 

(
    :line_id, 
    :name, 
    :description, 
    :step_number, 
    :step_type_id,
    :state_idle, 
    :state_running, 
    :state_held, 
    :state_completed, 
    :state_stopped, 
    :state_paused,
    GETDATE(),
    :updated_by
);
