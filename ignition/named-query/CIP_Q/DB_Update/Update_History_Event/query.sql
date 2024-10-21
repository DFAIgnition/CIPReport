UPDATE cip_report.dbo.history_events
SET
	circuit_id = :circuit_id,
	time_start = :time_start,
    time_end = :time_end,
    duration = :duration,
    stop_reason = :stop_reason,
    pause_count = :pause_count,
    held_count = :held_count,
    advanced_count = :advanced_count,
    pause_duration = :pause_duration,
    held_duration = :held_duration,
    type_sanitizer = :type_sanitizer,
    type_acid = :type_acid,
    type_caustic = :type_caustic,
    type_alkaline = :type_alkaline,
    updated_at = GETDATE(),
    updated_by = 'Ignition'
    
WHERE id = :id;