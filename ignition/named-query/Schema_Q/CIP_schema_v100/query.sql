CREATE DATABASE [cip_report]
GO

USE [cip_report]
GO

--------------------------------------------------------------------------------
-- Permissions stuf
--------------------------------------------------------------------------------
IF NOT EXISTS(SELECT * FROM system.dbo.projects WHERE project_name = 'CIPReport') 
BEGIN
	INSERT INTO system.dbo.projects (project_name, project_display_name, is_active) 
	VALUES ('CIPReport', 'CIP Report', 1)
END

GO

-- Create SITEADMIN permission
insert into system.dbo.project_permissions (project_id, permission_code, permission_display_name, area_type)
values ((select project_id from system.dbo.projects where project_name = 'CIPReport'), 'SITEADMIN', 'Site Admin', 'site');
insert into system.dbo.project_permissions (project_id, permission_code, permission_display_name, area_type)
values ((select project_id from system.dbo.projects where project_name = 'CIPReport'), 'USERADMIN', 'User Admin', 'site');

GO

--------------------------------------------------------------------------------
-- Versions table
--------------------------------------------------------------------------------
CREATE TABLE cip_report.dbo.versions
	(
	version_number decimal(5,2) NOT NULL,
	install_dt smalldatetime NOT NULL
	)  ON [PRIMARY];
GO	
ALTER TABLE cip_report.dbo.versions ADD CONSTRAINT
	DF_Table_1_install_dt DEFAULT CURRENT_TIMESTAMP FOR install_dt;
GO
ALTER TABLE cip_report.dbo.versions ADD CONSTRAINT
PK_Table_1 PRIMARY KEY CLUSTERED (version_number) WITH( STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY];
GO
insert into cip_report.dbo.versions (version_number) values (1.00);
GO
