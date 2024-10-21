#######################################################################################################################################
# generate an empty csv file that can be used to upload a new set of step descriptions
#######################################################################################################################################

def generateEmptyCSV(self):

#######################################################################################################################################

	try:

		time = CORE_P.Time.display_local_dt(CORE_P.Time.currentTimestamp(), self=self, format='yyyy-MM-dd_HHmm')
		filename = "Step_Table_" + str(time) + '.csv'
		
		# Define the headers and create an empty dataset
		headers = ["Set Name", "Set Description", "Step Number", "Step Description", 'Edit']
		
		# Define example data rows
		data = [
		    ["Step_Set_01", "Milk Tank CIP", "0", "IDLE", 'new'],
		    ["Step_Set_01", "Milk Tank CIP", "1", "Initializing", 'new'],
		    ["Step_Set_01", "Milk Tank CIP", "2", "Opening path", 'new'],
		    ["Above lines serve as example", "", "", "", ""],
		]
		
		# Create an empty BasicDataset with specified headers and empty data
		dataset = system.dataset.toDataSet(headers, data)
		
		# Convert the dataset to a CSV string
		csvstring = system.dataset.toCSV(dataset, showHeaders=1)
		
		# Download the file in a Perspective session
		system.perspective.download(filename, csvstring)
		
	except:
	
		CORE_P.Utils.errorPopup('Error generating empty csv:') #  + str(sys.exc_info())
	
	return
	
	
#######################################################################################################################################
# generate an empty csv file that can be used to upload a new set of step descriptions
#######################################################################################################################################

def saveDetailsToCSV(self, set_name, site_id):

#######################################################################################################################################	
	
	time = CORE_P.Time.display_local_dt(CORE_P.Time.currentTimestamp(), self=self, format='yyyy-MM-dd_HHmm')
	filename = "Step_Table_" + str(set_name.replace(" ", "_")) + "_" + str(time) + '.csv'
	
	parameters = {	'site_id': 		site_id,
				 	'name' : 		set_name}
				 	
	dataset = system.db.runNamedQuery(system.project.getProjectName(),'CIP_Q/DB_Query/Get_Step', parameters, tx=None, getKey=0)
	
	# Convert dataset to a list of PyDataSets (each inner list is a row)
	data = system.dataset.toPyDataSet(dataset)
	
	# Prepare new headers
	newHeaders = ["Set Name", "Set Description", "Step Number", "Step Description", "Edit"]
	
	# Prepare new data list
	newData = []
	
	# Iterate through original data and modify
	for row in data:
		# Create new row matching the new header structure, adding 'update' to the 'Edit' column
		newRow = [row['name'], row['description'], row['step_number'], row['step_description'], 'update']
		newData.append(newRow)
	
	# Create a new dataset with the modified data
	newDataset = system.dataset.toDataSet(newHeaders, newData)
	
	csvstring = system.dataset.toCSV(newDataset, showHeaders=1)
	
	system.perspective.download(filename, csvstring)
	
	return
	
#######################################################################################################################################
# load step datasets from the csv file
#######################################################################################################################################

def loadCSV(self, event, site_id):

#######################################################################################################################################

	try:

		#----------------------------------------------------------------------------------------------------------------------------------
		# Process the file and turn it into a useful data structure / Make sure data is valid
		#----------------------------------------------------------------------------------------------------------------------------------
		
		filename = event.file.name
		
		# Check file is csv
		if (filename.endswith('.csv'))==False:
			CORE_P.Utils.errorPopup("Can't process this file - expected to see a CSV file")
			return False	
		
		# Move csv data to array	
		data = CORE_P.Files.csvUploadToArray(event)		
		
		# Make sure file is not empty
		if not data:
		    CORE_P.Utils.errorPopup("Can't process this file - The CSV file is empty.")
		    return False
		
		# Check if the headers match the expected headers
		actual_header = set(data[0].keys())
		expected_header =set(["Set Name", "Set Description", "Step Number", "Step Description", 'Edit'])
		if actual_header != expected_header:
		    CORE_P.Utils.errorPopup("Header mismatch - The headers in the CSV file do not match the expected headers." + str(expected_header) + str(actual_header))
		    return False

		 # Prepare for validation
		unique_combinations = set()
		set_name_to_description = {}
		error_details = []
		
		# Skip headers and iterate through rows
		for index, row in enumerate(data, start=2):  # Adjust index to reflect line numbers if needed
		    # Check for required entries
		    set_name = row.get('Set Name')
		    set_description = row.get('Set Description')
		    step_number = row.get('Step Number')
		    step_description = row.get('Step Description')
		
		    if not (set_name and step_number and step_description):
		        missing_fields = [key for key in ['Set Name', 'Step Number', 'Step Description'] if not row.get(key)]
		        error_details.append((index, "Missing required data: " + ", ".join(missing_fields)))
		        continue
		
		    # Check for unique Set Name and Step Number combination
		    if (set_name, step_number) in unique_combinations:
		        error_details.append((index, "Duplicate 'Set Name' and 'Step Number' combination found."))
		    else:
		        unique_combinations.add((set_name, step_number))
		
		    # Check for consistent Set Description for each Set Name
		    if set_name in set_name_to_description:
		        if set_name_to_description[set_name] != set_description:
		            error_details.append((index, "Inconsistent 'Set Description' for the same 'Set Name'."))
		    else:
		        set_name_to_description[set_name] = set_description
		
		# Report errors if any
		if error_details:
		    error_message = "Data validation failed for the following reasons:\n" + "\n".join("Line %s: %s" % (line, reason) for line, reason in error_details)
		    CORE_P.Utils.errorPopup(error_message)
		    return False
		
		
		
		#----------------------------------------------------------------------------------------------------------------------------------
		# Kept updates and deletes in case they are needed in the future. Not used now.
		#----------------------------------------------------------------------------------------------------------------------------------
		
		inserts=[]
		updates=[]
		deletes=[]
		
		insert_count = 0
		update_count = 0
		delete_count = 0
		
		rowcount=2 # We start on row 2 of the csv file, because row 1 is the headers
		for row in data:
		
			row['rowcount'] = rowcount # Keep track of which row this is, so we can report errors
			
			# If this is a new entry
			if ((row['Edit'] == 'new') and (str(row['Set Name']) != '' )):
				inserts.append(row)
			
			# Or, an edit
			elif ((row['Edit'] == 'update') and (str(row['Set Name']) != '' )):
				updates.append(row)
			
			# Or a delete...
			elif ((row['Edit'] == 'delete') and (str(row['Set Name']) != '' )):
				deletes.append(row)
			
			# Otherwise, not sure what to do. Could be dodgy data?
			else:
				CORE_P.Utils.errorPopup("Can't work out what to do with row " + str(rowcount) + str(inserts) + str(updates) + str(deletes) + str(row))
				return False				
	
			rowcount = rowcount + 1

	
	except Exception as e:
		CORE_P.Utils.errorPopup('General error: '+str(e))
		return
		
	#----------------------------------------------------------------------------------------------------------------------------------
	# Insert new sets and steps
	#----------------------------------------------------------------------------------------------------------------------------------
	
	txId = system.db.beginTransaction(timeout=5000)
	
	try:
	
		for row in inserts:
			thisrow = row['rowcount']
			
			# Prepare parameters for checking and inserting
			
			parameters = {
				'site_id': 				site_id,
				'name':					row['Set Name'],
				'description':			row['Set Description'],
			}
			
			# Check if the entry already exists if not add new set
			exists_count = system.db.runNamedQuery(system.project.getProjectName(), 'CIP_Q/DB_Scalar/Get_Step_Type', parameters, tx=txId)
			
			if exists_count == 0:
				# Insert Step Dataset if it doesn't exist yet
				step_type_id = system.db.runNamedQuery(system.project.getProjectName(),'CIP_Q/DB_Insert/Insert_Step_Type', parameters, tx=txId, getKey=1)
				
			system.db.commitTransaction(txId)
			
			step_type_id = system.db.runNamedQuery(system.project.getProjectName(), 'CIP_Q/DB_Scalar/Get_Step_Type_ID', parameters, tx=txId)
			
			parameters = {
							'step_type_id': 		step_type_id,
							'step_number':			row['Step Number'],
							'step_description':		row['Step Description'],
									}
			# Check if the entry already exists in detail table if not add it
			exists_count = system.db.runNamedQuery(system.project.getProjectName(), 'CIP_Q/DB_Scalar/Get_Step', parameters, tx=txId)
			
			if exists_count == 0:
				# Insert Step Detail if it doesn't exist yet
				rows_affected = system.db.runNamedQuery(system.project.getProjectName(), 'CIP_Q/DB_Insert/Insert_Step', parameters, tx=txId)
				insert_count = insert_count + rows_affected
				system.db.commitTransaction(txId)
				

		# Audit log
		CORE_P.Utils.logChanges(self, 'CIPStepSet', 'Added ' + str(insert_count) + 'new steps.', txId=txId, site_id=site_id)
		CORE_P.Utils.successPopup('Import complete. Added ' + str(insert_count) + ' rows of steps')
		system.perspective.sendMessage("update_bindings", payload = {}, scope = "page")
		system.db.closeTransaction(txId) 

		
	except Exception as e:
		error_msg = "Failed to insert step dataset at row:  " + str(thisrow) + ". Error: " + str(e)
		CORE_P.Utils.errorPopup(error_msg)
		system.db.rollbackTransaction(txId)
		system.db.closeTransaction(txId) # Always close the transaction, on either success or failure
		system.perspective.sendMessage("update_bindings", payload = {}, scope = "page") # Just in case
		return

		
	return
