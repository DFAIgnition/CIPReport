UPDATE cip_report.dbo.line

SET 
    system_id = 					:system_id,
    name = 							:name,
    description = 					:description,
    supply_temp_transmitter = 		:supply_temp_transmitter,
    supply_flow_transmitter = 		:supply_flow_transmitter,
    supply_cond_transmitter = 		:supply_cond_transmitter,
    supply_press_transmitter = 	:supply_press_transmitter,
    supply_temp_switch = 			:supply_temp_switch,
    supply_flow_switch = 			:supply_flow_switch,
    supply_cond_switch = 			:supply_cond_switch,
    supply_press_switch = 			:supply_press_switch,
    return_temp_transmitter = 		:return_temp_transmitter,
    return_flow_transmitter = 		:return_flow_transmitter,
    return_cond_transmitter = 		:return_cond_transmitter,
    return_press_transmitter = 	:return_press_transmitter,
    return_temp_switch = 			:return_temp_switch,
    return_flow_switch = 			:return_flow_switch,
    return_cond_switch = 			:return_cond_switch,
    return_press_switch = 			:return_press_switch,
   	type_acid = 					:type_acid,
    type_caustic = 					:type_caustic,
   	type_sanitizer = 				:type_sanitizer,
    type_alkaline = 				:type_alkaline,
    cmd_advance = 					:cmd_advance,
    cmd_hold = 						:cmd_hold,
    cmd_pause = 					:cmd_pause,
    cmd_resume = 					:cmd_resume,
    updated_at = 					GETDATE(),
    updated_by = 					:updated_by
    
WHERE id = :id;


