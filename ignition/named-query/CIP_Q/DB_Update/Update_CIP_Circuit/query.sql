UPDATE cip_report.dbo.circuit

SET 
    name = 				:name,
    description = 		:description,
    step_number = 		:step_number,
    step_type_id = 		:step_type_id,
    line_id = 			:line_id,
    state_idle = 		:state_idle, 
    state_running = 	:state_running, 
    state_held = 		:state_held, 
    state_completed = 	:state_completed, 
    state_stopped = 	:state_stopped, 
    state_paused = 		:state_paused,
    updated_at = 		GETDATE(),
    updated_by = 		:updated_by
    
WHERE id = :id;
