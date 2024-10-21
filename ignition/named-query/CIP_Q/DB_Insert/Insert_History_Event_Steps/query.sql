INSERT INTO cip_report.dbo.history_events_steps (
    history_id, 
    time_start, 
    time_end, 
    duration,
    step_number,
    step_description,
    advance_count, 
    pause_count, 
    held_count, 
    pause_duration, 
    held_duration, 
    updated_at, 
    updated_by
)
VALUES (
    :history_id, 
    :time_start, 
    :time_end, 
    :duration,
    :step_number,
    :step_description,
    :pause_count, 
    :held_count, 
    :advanced_count, 
    :pause_duration, 
    :held_duration, 
    GETDATE(), 
    'Ignition'
)

