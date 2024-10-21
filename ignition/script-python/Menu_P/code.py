
###############################################################################################
# getProjectMenu
###############################################################################################
def getProjectMenu():
	"""
	Called by the CORE_P.Menu module, to build the project menu for this application
	Returns: {'menu_header':menu_header, 'menu_items':menu_items}
		
	"""
	project_name	= system.project.getProjectName()
	menu_header		= 'CIP Report'
	
	menu_items = [
		{'label': "CIP Main",					'icon':"material/linear_scale",			"target": "/main"},
		{'label': "Admin",						'icon':"material/settings",				"target": "", "items":[
			{'label': "Admin",					'icon':"material/settings",				"target": "/admin", 		'permission_code':'SITEADMIN', 'project_name':project_name},
			{'label': "User Admin",				'icon':"material/settings",				"target": "/admin/useradmin", 			'permission_code':'SITEADMIN', 'project_name':project_name}
		]},
		{'label': "Help",'icon':"material/help","target": "", "items":[
    		{'label': "How to use CIP Reporting",'icon':"material/picture_as_pdf","target": "../../../../system/webdev/CIPReport/Help/CIP%20User%20Documentation%20v100.pdf"},         
        ]},			
	]
	
	return {'menu_header':menu_header, 'menu_items':menu_items}