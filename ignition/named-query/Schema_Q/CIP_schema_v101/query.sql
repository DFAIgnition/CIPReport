/****** Create project tables   ******/

USE [cip_report]
GO  

--------------------------------------------------------------------------------
-- Type Table
--------------------------------------------------------------------------------
CREATE TABLE cip_report.dbo.system_type (
  id                  					INT IDENTITY(1,1) PRIMARY KEY,
  created_at          					DATETIME2 DEFAULT GETDATE(),
  updated_at          					DATETIME2 DEFAULT GETDATE(),
  updated_by							NVARCHAR(255) DEFAULT 'Ignition',
  name                					NVARCHAR(255) NOT NULL,
  description         					NVARCHAR(MAX),
  CONSTRAINT UC_System_Type_Name UNIQUE (name)
);
GO

--------------------------------------------------------------------------------
-- System Table
--------------------------------------------------------------------------------
CREATE TABLE cip_report.dbo.system (
  id                  					INT IDENTITY(1,1) PRIMARY KEY,
  created_at          					DATETIME2 DEFAULT GETDATE(),
  updated_at          					DATETIME2 DEFAULT GETDATE(),
  updated_by							NVARCHAR(255) DEFAULT 'Ignition',
  site_id             					INT NOT NULL,
  type_id								INT NOT NULL,
  name                					NVARCHAR(255) NOT NULL,
  description         					NVARCHAR(MAX),
  CONSTRAINT UC_System_SiteId_Name UNIQUE (site_id, name),
  CONSTRAINT FK_system_type FOREIGN KEY (type_id) REFERENCES cip_report.dbo.system_type (id)
);
GO

--------------------------------------------------------------------------------
-- Line Table (each system might feed several lines)
--------------------------------------------------------------------------------
CREATE TABLE cip_report.dbo.line (
  id                  					INT IDENTITY(1,1) PRIMARY KEY,
  created_at          					DATETIME2 DEFAULT GETDATE(),
  updated_at          					DATETIME2 DEFAULT GETDATE(),
  updated_by							NVARCHAR(255) DEFAULT 'Ignition',
  system_id           					INT NOT NULL,
  name                					NVARCHAR(255) NOT NULL,
  description         					NVARCHAR(MAX),
  supply_temp_transmitter  			NVARCHAR(255),  
  supply_flow_transmitter  			NVARCHAR(255),
  supply_cond_transmitter  			NVARCHAR(255),
  supply_press_transmitter 			NVARCHAR(255),
  supply_temp_switch  					NVARCHAR(255),
  supply_flow_switch  					NVARCHAR(255),
  supply_cond_switch  					NVARCHAR(255),
  supply_press_switch 					NVARCHAR(255),
  return_temp_transmitter  			NVARCHAR(255),
  return_flow_transmitter  			NVARCHAR(255),
  return_cond_transmitter  			NVARCHAR(255),
  return_press_transmitter 			NVARCHAR(255),
  return_temp_switch  					NVARCHAR(255),
  return_flow_switch  					NVARCHAR(255),
  return_cond_switch  					NVARCHAR(255),
  return_press_switch					NVARCHAR(255),
  type_acid								NVARCHAR(255),
  type_caustic							NVARCHAR(255),
  type_sanitizer						NVARCHAR(255),
  type_alkaline							NVARCHAR(255),
  cmd_advance							NVARCHAR(255),
  cmd_pause								NVARCHAR(255),
  cmd_hold								NVARCHAR(255),
  cmd_resume							NVARCHAR(255),
  CONSTRAINT FK_Line_System FOREIGN KEY (system_id) REFERENCES cip_report.dbo.system(id),
  CONSTRAINT UC_Line_SystemId_Name UNIQUE (system_id, name)
);
GO

--------------------------------------------------------------------------------
-- Step Lookup Tables
--------------------------------------------------------------------------------

CREATE TABLE cip_report.dbo.step_type (
  id                  					INT IDENTITY(1,1) PRIMARY KEY,
  created_at         					DATETIME2 DEFAULT GETDATE(),
  updated_at          					DATETIME2 DEFAULT GETDATE(),
  updated_by							NVARCHAR(255) DEFAULT 'Ignition',
  name             						NVARCHAR(255) NOT NULL,
  description         					NVARCHAR(MAX),
  site_id             					INT NOT NULL,
  CONSTRAINT UC_stepname_SiteId_Name UNIQUE (site_id, name)
);
GO

CREATE TABLE cip_report.dbo.step (
  created_at          					DATETIME2 DEFAULT GETDATE(),
  updated_at          					DATETIME2 DEFAULT GETDATE(),
  updated_by		   					NVARCHAR(255) DEFAULT 'Ignition',
  step_type_id		      				INT NOT NULL,
  step_number         					INT NOT NULL,
  step_description    					NVARCHAR(255) NOT NULL,
  CONSTRAINT FK_Step_Type_ID FOREIGN KEY (step_type_id) REFERENCES cip_report.dbo.step_type (id),
  CONSTRAINT UC_Id_StepNumber UNIQUE (step_type_id, step_number)
);
GO

-- Circuit Table (each line might feed multiple circuits)
--------------------------------------------------------------------------------
CREATE TABLE cip_report.dbo.circuit (
  id                  					INT IDENTITY(1,1) PRIMARY KEY,
  created_at          					DATETIME2 DEFAULT GETDATE(),
  updated_at          					DATETIME2 DEFAULT GETDATE(),
  updated_by		   					NVARCHAR(255) DEFAULT 'Ignition',
  line_id             					INT NOT NULL,
  name                					NVARCHAR(255) NOT NULL,
  description         					NVARCHAR(MAX),
  step_number         					NVARCHAR(255) NOT NULL,
  step_type_id     					INT NOT NULL,
  state_idle         					NVARCHAR(255),
  state_running        				NVARCHAR(255),
  state_held     						NVARCHAR(255),
  state_aborted        				NVARCHAR(255),
  state_completed       				NVARCHAR(255),
  state_stopped        				NVARCHAR(255),
  state_paused       					NVARCHAR(255),

  CONSTRAINT FK_Circuit_Line FOREIGN KEY (line_id) REFERENCES cip_report.dbo.line(id),
  CONSTRAINT UC_Circuit_LineId_Name UNIQUE (line_id, name),
  CONSTRAINT FK_Circuit_StepSetID FOREIGN KEY (step_type_id) REFERENCES cip_report.dbo.step_type (id)
);
GO

--------------------------------------------------------------------------------
-- Versions table
--------------------------------------------------------------------------------

insert into cip_report.dbo.versions (version_number) values (1.01);
GO