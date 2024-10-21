import java.util.Date

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Helper Function for Duration Calculation
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def help_get_duration(start, end):
	try:
		return (end.getTime() - start.getTime()) / 1000  # Convert milliseconds to seconds
	except:
		help_send_log_message('CIPReport Error','Error calculating duration.',show=True)

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Helper Function to Handle Database Transactions
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def help_handle_db_transaction(query, parameters,timeout_value=5000):

    txId = system.db.beginTransaction(timeout=timeout_value)
    
    try:
		result = system.db.runNamedQuery(system.project.getProjectName(), query, parameters, tx=txId, getKey=1)
		system.db.commitTransaction(txId)
		return result
    except Exception as e: 
		system.db.rollbackTransaction(txId)
		help_send_log_message('CIPReport Error','Error during database operation.' + str(e),show=True)
		return None
    finally:
        system.db.closeTransaction(txId)
        
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Helper Function for logging. Set show to False when not testing
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def help_send_log_message(logger, text, parameter='', show=False):

	if show:
		system.util.getLogger(logger).info(text+str(parameter))

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Helper function to get step descriptions
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def help_get_step_dictionary(circuit_id):

    try:
        query = "CIP_Q/DB_Query/Get_Step_Discription_For_Circuit"
        params = {'circuit_id': circuit_id}
        result = system.db.runNamedQuery(system.project.getProjectName(), query, params)
        step_descriptions = {row["step_number"]: row["step_description"] for row in system.dataset.toPyDataSet(result)}
        return step_descriptions
    except Exception as e: 
		help_send_log_message('CIPReport Error','Error getting step description.' + str(e),show=True)
		return {}
        


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Helper function to calculate stats
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def help_calc_step_stats(row, stats=None):

    # Define the transmitters we're interested in
    transmitters = [
        'supply_temp_transmitter', 'supply_flow_transmitter', 'supply_press_transmitter', 'supply_cond_transmitter',
        'return_temp_transmitter', 'return_flow_transmitter', 'return_press_transmitter', 'return_cond_transmitter'
    ]

    # Initialize the statistics dictionary if not already done
    if stats is None:
        stats = {trans: {'max': None, 'min': None, 'avg' : None , 'sum': 0, 'count': 0} for trans in transmitters}

    try:
        for trans in transmitters:
            if trans in row and row[trans] is not None:
				value = row[trans]
				
				# Update maximum
				if value > stats[trans]['max'] or stats[trans]['max']==None:
				    stats[trans]['max'] = value
				
				# Update minimum
				if value < stats[trans]['min'] or stats[trans]['min']==None:
				    stats[trans]['min'] = value
				
				# Update sum and count for averaging
				stats[trans]['sum'] += value
				stats[trans]['count'] += 1
				
				# Update average
				if stats[trans]['count'] >0:
					stats[trans]['avg'] =  stats[trans]['sum']/ stats[trans]['count']


    except Exception as e: 
		help_send_log_message('CIPReport Error','Error calculating step statistics' + str(e),show=True)

    return stats


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Helper function to Initialize event variables
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 
def help_initialize_variables(last_check=None):

	try:

	    return {
	        'event_start': None, 'event_end': None,'event_duration': 0,
	        'advanced_count': 0, 'pause_count': 0, 'held_count': 0,
	        'pause_duration': 0, 'held_duration': 0,
	        'last_advanced_time': None, 'last_pause_time': None, 'last_held_time': None,
	        'last_advance_count': 0, 'last_pause_count': 0, 'last_held_count': 0,
	        'last_pause_duration': 0, 'last_held_duration': 0,
	        'stop_reason': None, 'last_step': None, 'current_step': None, 'step_start_time': None, 'step_end_time': None,
	        'steps': [], 'operation_events': [],'step_duration': 0,'step_description': None, 'stats': None,'last_check': last_check,
	        'type_sanitizer':0,'type_caustic':0,'type_acid':0,'type_alkaline':0
	    }
	    
	except Exception as e: 
		help_send_log_message('CIPReport Error','Error initilizing variables' + str(e),show=True)
		return
		

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Helper function to prepare event data
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// 		
def help_prepare_event_data(vars, tag_row):

    return {
        'circuit_id': tag_row['circuit'],
        'time_start': vars['event_start'],
        'time_end': vars['event_end'],
        'duration': vars['event_duration'],
        'stop_reason': vars['stop_reason'],
        'advanced_count': vars['advanced_count'],
        'pause_count': vars['pause_count'],
        'held_count': vars['held_count'],
        'pause_duration': vars['pause_duration'],
        'held_duration': vars['held_duration'],
        'type_sanitizer': vars['type_sanitizer'],
        'type_acid': vars['type_acid'],
        'type_caustic': vars['type_caustic'],
        'type_alkaline': vars['type_alkaline'],
        'steps': vars['steps'],
        'operation_events': vars['operation_events'],
    }


#=========================================================================================================================================
# Sub Function In Processing To Detect Start Of New Event
#=========================================================================================================================================		
def sub_get_start_events(vars,row):

	try:

	    # Check if a new event should start based on 'state_running' and no active event
	    if vars['event_start'] is None and row.get('state_running') == 1:
	    	
			# Set the start timestamp of the event
			#vars = help_initialize_variables()
			vars['event_start'] = row['t_stamp']
			
			help_send_log_message('CIPReport Start','Found start event: ',row['t_stamp'])
			
			# Initialize CIP type flags
			vars['type_sanitizer'] = row.get('type_sanitizer') if row.get('type_sanitizer') is not None else 0
			vars['type_acid'] = row.get('type_acid') if row.get('type_acid') is not None else 0
			vars['type_caustic'] = row.get('type_caustic') if row.get('type_caustic') is not None else 0
			vars['type_alkaline'] = row.get('type_alkaline') if row.get('type_alkaline') is not None else 0
	        
	except Exception as e: 
		help_send_log_message('CIPReport Error','Error finding start event' + str(e),show=True)
		return

		
#=========================================================================================================================================
# Sub Function In Processing To Generate Step Details
#=========================================================================================================================================		
def sub_get_step_events(vars, row, tag_row,step_descriptions):

	try:

	    vars['current_step'] = row.get('step_number')
	    
	    # Calculate instrument statistics for the step using the pre-fetched history
	    vars['stats'] = help_calc_step_stats(row, vars['stats'])
	    
	    # Check for step change and update step data
	    if vars['last_step'] is None or vars['last_step'] != vars['current_step']:
	    
	        if vars['step_start_time'] is not None:  # Ensure step_start_time is initialized
				vars['step_end_time'] = row['t_stamp']
				vars['step_duration'] = help_get_duration(vars['step_start_time'], vars['step_end_time'])
				
								
				# Get step description from dictionary we built
				try:
					vars['step_description'] = step_descriptions.get(int(vars['last_step']), "Description not found")
				except:	
					vars['step_description'] = step_descriptions.get(str(vars['last_step']), "Description not found")
				
				# Append the step data to the steps list
				
				vars['steps'].append({
					'step_number': 			vars['last_step'],
				    'start_time': 			vars['step_start_time'],
				    'end_time':  			vars['step_end_time'],
				    'step_duration':  		vars['step_duration'],
				    'step_description': 	vars['step_description'],
				    'advanced_count': 		vars['advanced_count'] - vars['last_advance_count'],
				    'pause_count': 			vars['pause_count'] - vars['last_pause_count'],
				    'held_count': 			vars['held_count'] - vars['last_held_count'],
				    'pause_duration': 		vars['pause_duration'] - vars['last_pause_duration'],
				    'held_duration': 		vars['held_duration'] - vars['last_held_duration'],
				    'supply_temp_max': 	vars['stats']['supply_temp_transmitter']['max'],
				    'supply_flow_max': 	vars['stats']['supply_flow_transmitter']['max'],
				    'supply_press_max': 	vars['stats']['supply_press_transmitter']['max'],
				    'supply_cond_max': 	vars['stats']['supply_cond_transmitter']['max'],
				    'return_temp_max': 	vars['stats']['return_temp_transmitter']['max'],
				    'return_flow_max': 	vars['stats']['return_flow_transmitter']['max'],
				    'return_press_max': 	vars['stats']['return_press_transmitter']['max'],
				    'return_cond_max': 	vars['stats']['return_cond_transmitter']['max'],
				    'supply_temp_min': 	vars['stats']['supply_temp_transmitter']['min'],
				    'supply_flow_min': 	vars['stats']['supply_flow_transmitter']['min'],
				    'supply_press_min': 	vars['stats']['supply_press_transmitter']['min'],
				    'supply_cond_min': 	vars['stats']['supply_cond_transmitter']['min'],
				    'return_temp_min': 	vars['stats']['return_temp_transmitter']['min'],
				    'return_flow_min': 	vars['stats']['return_flow_transmitter']['min'],
				    'return_press_min':	vars['stats']['return_press_transmitter']['min'],
				    'return_cond_min': 	vars['stats']['return_cond_transmitter']['min'],
				    'supply_temp_avg': 	vars['stats']['supply_temp_transmitter']['avg'] ,
				    'supply_flow_avg': 	vars['stats']['supply_flow_transmitter']['avg'] ,
				    'supply_press_avg': 	vars['stats']['supply_press_transmitter']['avg'] ,
				    'supply_cond_avg': 	vars['stats']['supply_cond_transmitter']['avg'] ,
				    'return_temp_avg': 	vars['stats']['return_temp_transmitter']['avg'] ,
				    'return_flow_avg': 	vars['stats']['return_flow_transmitter']['avg'] ,
				    'return_press_avg': 	vars['stats']['return_press_transmitter']['avg'] ,
				    'return_cond_avg': 	vars['stats']['return_cond_transmitter']['avg'] ,
				    })
	            
	        # Initialize new step
	        vars['stats']=None
	        vars['step_start_time'] = row['t_stamp']
	        vars['last_step'] = vars['current_step']
	        vars['last_advance_count'] = vars['advanced_count']
	        vars['last_pause_count'] = vars['pause_count']
	        vars['last_held_count'] = vars['held_count']
	        vars['last_pause_duration'] = vars['pause_duration']
	        vars['last_held_duration'] = vars['held_duration']

	except Exception as e:
		help_send_log_message('CIPReport Error','Error processing steps:' + str(e),show=True)
		return
            
#=========================================================================================================================================
# Sub Function In Processing To Generate Operation Events:
#=========================================================================================================================================		
def sub_get_operator_events(vars,row):

	try:

	    # Collect advance information
	    if vars['event_start'] is not None and row.get('cmd_advance') == 1:
	        if vars['last_advanced_time'] is None:  # Transition into advance
	            vars['last_advanced_time'] = row['t_stamp']
	    elif vars['last_advanced_time'] is not None:  # Transition out of advance
	        vars['operation_events'].append({
	            'type_event': 1,
	            'time_start': vars['last_advanced_time'],
	            'time_end': row['t_stamp'],
	            'duration': help_get_duration(vars['last_advanced_time'], row['t_stamp'])
	        })
	        vars['last_advanced_time'] = None
	        vars['advanced_count'] += 1
	
	    # Collect pause information
	    if vars['event_start'] is not None and (row.get('state_paused') == 1 or row.get('cmd_paused') == 1):
	        if vars['last_pause_time'] is None:  # Transition into pause
	            vars['last_pause_time'] = row['t_stamp']
	    elif vars['last_pause_time'] is not None:  # Transition out of pause
	        vars['pause_duration'] += help_get_duration(vars['last_pause_time'], row['t_stamp'])
	        vars['operation_events'].append({
	            'type_event': 2,
	            'time_start': vars['last_pause_time'],
	            'time_end': row['t_stamp'],
	            'duration': help_get_duration(vars['last_pause_time'], row['t_stamp'])
	        })
	        vars['last_pause_time'] = None
	        vars['pause_count'] += 1
	
	    # Collect held information
	    if vars['event_start'] is not None and (row.get('state_held') == 1 or row.get('cmd_held') == 1):
	        if vars['last_held_time'] is None:  # Transition into hold
	            vars['last_held_time'] = row['t_stamp']
	    elif vars['last_held_time'] is not None:  # Transition out of hold
	        vars['held_duration'] += help_get_duration(vars['last_held_time'], row['t_stamp'])
	        vars['operation_events'].append({
	            'type_event': 3,
	            'time_start': vars['last_held_time'],
	            'time_end': row['t_stamp'],
	            'duration': help_get_duration(vars['last_held_time'], row['t_stamp'])
	        })
	        vars['last_held_time'] = None
	        vars['held_count'] += 1
	        
	except Exception as e: 
		help_send_log_message('CIPReport Error','Error processing operation events' + str(e),show=True)
		return
        
#=========================================================================================================================================
# Sub Function In Processing To Generate End Event:Either end if idle, stopped or completed exists or running goes away if not
#=========================================================================================================================================	

def sub_get_end_events(vars, row):
    try:
        
        end_conditions_met = False
        state_columns = ['state_completed', 'state_stopped', 'state_idle']
        
        # Check if any of the state columns exist
        state_columns_exist = any(col in row for col in state_columns)
        
        if state_columns_exist:
            # Check if any state column transition from 0 to 1
            for col in state_columns:
                if row.get(col) == 1:
                    end_conditions_met = True
                    break
        else:
            # Check for state_running signal
            if row.get('state_running') == 0:
                end_conditions_met = True

        if end_conditions_met:
            vars['event_end'] = row['t_stamp']
            vars['event_duration'] = help_get_duration(vars['event_start'], vars['event_end'])
            
            help_send_log_message('CIPReport End', 'Found end event: ', row['t_stamp'])
            
            # Determine the stop reason based on the state flags
            if 'state_stopped' in row and row['state_stopped']:
                vars['stop_reason'] = 'Stopped'
            elif 'state_completed' in row and row['state_completed']:
                vars['stop_reason'] = 'Completed'
            elif 'state_idle' in row and row['state_idle']:
                vars['stop_reason'] = 'Idle'
            elif not state_columns_exist:
                vars['stop_reason'] = 'Completed'
            else:
                vars['stop_reason'] = 'Unknown'
            
            return True
        
        return False
            
    except Exception as e: 
        help_send_log_message('CIPReport Error', 'Error processing end event: ' + str(e), show=True)
        return False
		
		

		
#######################################################################################################################################
# Main Function to Get CIP Events
#######################################################################################################################################
def main_get_all_cip_events(time_start, time_end, site_id=0, system_id=0, line_id=0, circuit_id=0,check_last=True):

	try:
	
		# Get configured tag names
		
		namedQuery = "CIP_Q/DB_Query/Get_CIP_Status_Tags"
		parameters = {'site_id': site_id, 'system_id': system_id, 'line_id': line_id, 'circuit_id': circuit_id}
		tag_data = help_handle_db_transaction(namedQuery, parameters)
		
		
		last_event_dict={}
		
		# Get last completed event for each circuit if check_last is selected
		if check_last:
		
			query = 'SELECT circuit_id, last_check_time AS time_start FROM cip_report.dbo.circuit_last_check'
			last_event = system.db.runPrepQuery(query, [])
			
			# Create a dictionary for quick lookup of last events by circuit
			last_event_dict = {event['circuit_id']: event['time_start'] for event in last_event}
			
		
		if tag_data is None:
		    return 'error'
		
		# Get events based on history and tags
		
		events = []
		
		for index, tag_row in enumerate(tag_data, start=1):
		
			# Show each 10th log message
			show_log = index % 10 == 1
			help_send_log_message('CIPReport','Working on circuit ' + str(index) + ' from: ' + str(len(tag_data)),show=show_log)
			
			# Retrieve the circuit-specific start and end times if available to not query things that already have been captured
			circuit_specific_data = last_event_dict.get(tag_row['circuit'])
			
			if circuit_specific_data:
			    circuit_start_time = circuit_specific_data
			else:
			    circuit_start_time = time_start
			
			circuit_end_time = time_end
			    			    			
			events.extend(main_query_data(tag_row, circuit_start_time, circuit_end_time))
			
		help_send_log_message('CIPReport','Getting CIP Events - Complete',show=True)

		return events
	    
	except Exception as e: 
		help_send_log_message('CIPReport Error','Error getting events' + str(e),show=True)
		return
		
						
#=========================================================================================================================================
# Sub Function to Get Tag History for states
#=========================================================================================================================================
def main_query_data(tag_row, time_start, time_end):
		
	try:
		event_tags = 		['step_number', 'state_running', 'state_idle', 'state_held', 'state_paused', 'state_stopped', 'state_completed',
		               		 'type_caustic', 'type_acid', 'type_sanitizer', 'type_alkaline','cmd_advance','cmd_pause','cmd_hold']
		               
		instrument_tags = 	['supply_temp_transmitter', 'supply_flow_transmitter', 'supply_press_transmitter', 'supply_cond_transmitter',
				        	 'return_temp_transmitter', 'return_flow_transmitter', 'return_press_transmitter', 'return_cond_transmitter']
		
		# Safely build list of tags that exist and are truthy
		ordered_tags = []
		filtered_tag_columns = []
		for col in event_tags + instrument_tags:
		    try:
		        # Check if the column has a truthy value
		        value = tag_row[col]
		        if value:
		            ordered_tags.append(value)
		            filtered_tag_columns.append(col)
		    except KeyError:
		        # Skip this column if it's not present in the tag_row
		        continue
		
		if not ordered_tags:
		    CORE_P.Utils.errorPopup('No valid tags found for querying')
		    return
		
		all_tags = [CORE_P.Tags.getFullyQualifiedTagName(tag) for tag in ordered_tags]
		
		history = system.tag.queryTagHistory(
		    paths=all_tags, startDate=time_start, endDate=time_end,
		    returnSize=-1, includeBoundingValues=True, noInterpolation=False,
		    ignoreBadQuality=True, columnNames=filtered_tag_columns, returnFormat='Wide'
		)
		
		help_send_log_message('CIPReport', 'Pulled history for circuit ' + str(tag_row['circuit']) + 
		                              '. Found: ' + str(history.getRowCount()) + ' rows of data between Start: ' + 
		                              str(time_start) + ' and End ' + str(time_end))
		
		return main_process_data(history, tag_row, time_start, time_end)
		
	except Exception as e: 
		help_send_log_message('CIPReport Error','Error getting history' + str(e),show=True)
		return

		
#=========================================================================================================================================
# Sub Function to Process History Results and Detect Events
#=========================================================================================================================================		
def main_process_data(history, tag_row, time_start, time_end):

    try:
		vars = help_initialize_variables()
		events = []
		step_descriptions = help_get_step_dictionary(tag_row['circuit'])
		
		if not history or history.getRowCount() == 0:
			return events
		
		for i in range(history.getRowCount()):
			row = {col: history.getValueAt(i, col) for col in history.getColumnNames()}

			sub_get_start_events(vars,row)
			
			if vars['event_start']:
			
				sub_get_step_events(vars, row, tag_row,step_descriptions)
				sub_get_operator_events(vars, row)
			
				if sub_get_end_events(vars, row):
				    event_data = help_prepare_event_data(vars, tag_row)
				    events.append(event_data)
				    vars = help_initialize_variables(last_check=vars['last_check'])
				    
			else:
				vars['last_check'] = row['t_stamp']
			
		if events:
			
			#system.util.invokeAsynchronous(CIP_P.Aggregator.db_write_events, args=(events,check_last,))
			db_write_events(events)
			
		# Update last check time
		if vars['last_check'] is not None:
			update_last_check_time(tag_row['circuit'],CORE_P.Time.adjustTimestamp(vars['last_check'],offset_minutes=-5))
			
		return events

    except Exception as e: 
		help_send_log_message('CIPReport Error','Error processing history' + str(e),show=True)
		return []

#=========================================================================================================================================
# Sub Function to Insert Events into the Database cip_report.dbo.history_events
#=========================================================================================================================================
def db_write_events(events):
    txId = system.db.beginTransaction(timeout=20000)
    
    try:
        for event in events:
            # Check if the event already exists
            query_check = """
                SELECT id FROM cip_report.dbo.history_events
                WHERE circuit_id = ? AND time_start = ?
            """
            params_check = [event['circuit_id'], event['time_start']]
            exists = system.db.runPrepQuery(query_check, params_check, tx=txId)
            
            if exists:
                help_send_log_message('CIPReport Write', 'Event already exists')
            else:
                help_send_log_message('CIPReport Write', 'Event Not Found')
                insert_query = """
                    INSERT INTO cip_report.dbo.history_events (
                        circuit_id, time_start, time_end, duration, stop_reason, 
                        pause_count, held_count, advanced_count, pause_duration, 
                        held_duration, type_sanitizer, type_acid, type_caustic, 
                        type_alkaline, updated_at, updated_by
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), 'Ignition')
                """
                params_insert = [
                    event['circuit_id'], event['time_start'], event['time_end'], 
                    event['duration'], event['stop_reason'], event['pause_count'], 
                    event['held_count'], event['advanced_count'], event['pause_duration'], 
                    event['held_duration'], event['type_sanitizer'], event['type_acid'], 
                    event['type_caustic'], event['type_alkaline']
                ]
                
                help_send_log_message('CIPReport Write', 'Parameter: ',params_insert)
                
                event_id = system.db.runPrepUpdate(insert_query, params_insert, tx=txId, getKey=1)
                
                if event_id:
                    CIP_P.Aggregator.db_write_steps(event['steps'], event_id, txId)
                    CIP_P.Aggregator.db_write_operator(event['operation_events'], event_id, txId)
                    
                    help_send_log_message('CIPReport Write', 'Added new CIP: ' + str(event['time_start']) + ' circuit: ' + str(event['circuit_id']) + ' eventid: ' + str(event_id), show=True)
        
        system.db.commitTransaction(txId)
    
    except Exception as e:
        help_send_log_message('CIPReport Error', 'Error during bulk database write: ' + str(e) + ' ' + str(event), show=True)
        system.db.rollbackTransaction(txId)
    
    finally:
        system.db.closeTransaction(txId)
        return

	
		
#=========================================================================================================================================
# Sub Function to Insert Event Steps into the Database cip_report.dbo.history_events_steps
#=========================================================================================================================================
def db_write_steps(steps,event_id, txId):

	try:

		if not steps:
			return  # Nothing to insert if steps list is empty
		
		query = """
			INSERT INTO cip_report.dbo.history_events_steps
			  (event_id, time_start, time_end, duration, step_number, step_description, 
			   pause_count, held_count, advanced_count, pause_duration, held_duration,
			   supply_temp_avg, supply_temp_min, supply_temp_max,
			   supply_flow_avg, supply_flow_min, supply_flow_max,
			   supply_press_avg, supply_press_min, supply_press_max,
			   supply_cond_avg, supply_cond_min, supply_cond_max,
			   return_temp_avg, return_temp_min, return_temp_max,
			   return_flow_avg, return_flow_min, return_flow_max,
			   return_press_avg, return_press_min, return_press_max,
			   return_cond_avg, return_cond_min, return_cond_max)
			VALUES
			  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
		"""
		
		
		# Insert only steps that are associated with the current event_id
		for step in steps:
			params = [
				event_id,
				step['start_time'],
				step['end_time'],
				step['step_duration'],
				step['step_number'],
				step['step_description'],
				step['pause_count'],
				step['held_count'],
				step['advanced_count'],
				step['pause_duration'],
				step['held_duration'],
				step['supply_temp_avg'],
				step['supply_temp_min'],
				step['supply_temp_max'],
				step['supply_flow_avg'],
				step['supply_flow_min'],
				step['supply_flow_max'],
				step['supply_press_avg'],
				step['supply_press_min'],
				step['supply_press_max'],
				step['supply_cond_avg'],
				step['supply_cond_min'],
				step['supply_cond_max'],
				step['return_temp_avg'],
				step['return_temp_min'],
				step['return_temp_max'],
				step['return_flow_avg'],
				step['return_flow_min'],
				step['return_flow_max'],
				step['return_press_avg'],
				step['return_press_min'],
				step['return_press_max'],
				step['return_cond_avg'],
				step['return_cond_min'],
				step['return_cond_max']
				]
			system.db.runPrepUpdate(query, params, tx=txId)
			
	except Exception as e: 
		help_send_log_message('CIPReport Error','Error during bulk step write' + str(e),show=True)
		system.db.rollbackTransaction(txId)
		return
	
#=========================================================================================================================================
# Sub Function to Insert Operation Event into the Database cip_report.dbo.history_events_op
#=========================================================================================================================================        
def db_write_operator(operation_events,event_id, txId):

	try:

		if not operation_events:
			return  # Nothing to insert 
				
		query = """
			INSERT INTO cip_report.dbo.history_events_op
			    (event_id, type_event, time_start, time_end, duration)
			VALUES
			    (?, ?, ?, ?, ?)
		"""
		# Insert only operation events that are associated with the current event_id
		for operation in operation_events:
		    params = [
		        event_id,
		        operation['type_event'],
		        operation['time_start'],
		        operation['time_end'],
		        operation['duration']
		    ]
		    system.db.runPrepUpdate(query, params, tx=txId)
		    
	except Exception as e: 
		help_send_log_message('CIPReport Error','Error during bulk operation write' + str(e),show=True)
		system.db.rollbackTransaction(txId)
		return

#=========================================================================================================================================
# Sub Function to save last time a circuit was checked
#=========================================================================================================================================  	

def update_last_check_time(circuit_id, last_check_time):
    try:
        query = """
                    MERGE cip_report.dbo.circuit_last_check AS target
                    USING (SELECT ? AS circuit_id, ? AS last_check_time) AS source
                    ON (target.circuit_id = source.circuit_id)
                    WHEN MATCHED THEN
                        UPDATE SET target.last_check_time = source.last_check_time
                    WHEN NOT MATCHED THEN
                        INSERT (circuit_id, last_check_time)
                        VALUES (source.circuit_id, source.last_check_time);
                """
        params = [circuit_id, last_check_time]
        system.db.runPrepUpdate(query, params)
    except Exception as e: 
		help_send_log_message('CIPReport Error','Error updating last check time' + str(e),show=True)
		return