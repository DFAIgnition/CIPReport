/****** Create project tables   ******/

USE [cip_report]
GO  

--------------------------------------------------------------------------------
-- History Tables
--------------------------------------------------------------------------------

CREATE TABLE cip_report.dbo.history_events (
  id                  					INT IDENTITY(1,1) PRIMARY KEY,
  created_at         					DATETIME2 DEFAULT GETDATE(),
  updated_at          					DATETIME2 DEFAULT GETDATE(),
  updated_by							NVARCHAR(255) DEFAULT 'Ignition',
  circuit_id       						INT NOT NULL,
  time_start          					DATETIME2,
  time_end          					DATETIME2,
  duration								DECIMAL(10,0) NOT NULL,
  stop_reason							NVARCHAR(255) NOT NULL,
  pause_count							INT NOT NULL,
  held_count							INT NOT NULL,
  advanced_count						INT NOT NULL,
  pause_duration						DECIMAL(10,0) NOT NULL,
  held_duration							DECIMAL(10,0) NOT NULL,
  type_sanitizer						BIT NOT NULL,
  type_acid								BIT NOT NULL,
  type_caustic							BIT NOT NULL,
  type_alkaline							BIT NOT NULL,
  
  CONSTRAINT FK_circuit_ID FOREIGN KEY (circuit_id) REFERENCES cip_report.dbo.circuit (id)
);
GO

CREATE INDEX idx_history_events_time_start ON cip_report.dbo.history_events (time_start);
CREATE INDEX idx_history_events_time_end ON cip_report.dbo.history_events (time_end);
CREATE INDEX idx_history_events_circuit_id ON cip_report.dbo.history_events (circuit_id);


CREATE TABLE cip_report.dbo.history_events_steps (
  id                  					INT IDENTITY(1,1) PRIMARY KEY,
  created_at         					DATETIME2 DEFAULT GETDATE(),
  updated_at          					DATETIME2 DEFAULT GETDATE(),
  updated_by							NVARCHAR(255) DEFAULT 'Ignition',
  event_id       						INT NOT NULL,
  time_start          					DATETIME2,
  time_end          					DATETIME2,
  duration								DECIMAL(10,0) NOT NULL,
  step_number							NVARCHAR(255) NOT NULL,
  step_description						NVARCHAR(255) NOT NULL,
  pause_count							INT NOT NULL,
  held_count							INT NOT NULL,
  advanced_count						INT NOT NULL,
  pause_duration						DECIMAL(10,0) NOT NULL,
  held_duration							DECIMAL(10,0) NOT NULL,
  supply_temp_avg						REAL,
  supply_temp_min						REAL,
  supply_temp_max						REAL,
  supply_flow_avg						REAL,
  supply_flow_min						REAL,
  supply_flow_max						REAL,
  supply_press_avg						REAL,
  supply_press_min						REAL,
  supply_press_max						REAL,
  supply_cond_avg						REAL,
  supply_cond_min						REAL,
  supply_cond_max						REAL,
  return_temp_avg						REAL,
  return_temp_min						REAL,
  return_temp_max						REAL,
  return_flow_avg						REAL,
  return_flow_min						REAL,
  return_flow_max						REAL,
  return_press_avg						REAL,
  return_press_min						REAL,
  return_press_max						REAL,
  return_cond_avg						REAL,
  return_cond_min						REAL,
  return_cond_max				  		REAL,
  
  CONSTRAINT FK_event_ID_step FOREIGN KEY (event_id) REFERENCES cip_report.dbo.history_events (id)
  CREATE INDEX idx_history_events_steps_event_id ON cip_report.dbo.history_events_steps (event_id);
);
GO

CREATE INDEX idx_history_events_steps_event_id ON cip_report.dbo.history_events_steps (event_id);


CREATE TABLE cip_report.dbo.history_events_op (
  id                  					INT IDENTITY(1,1) PRIMARY KEY,
  created_at         					DATETIME2 DEFAULT GETDATE(),
  updated_at          					DATETIME2 DEFAULT GETDATE(),
  updated_by							NVARCHAR(255) DEFAULT 'Ignition',
  event_id       						INT NOT NULL,
  type_event							INT NOT NULL,
  time_start          					DATETIME2,
  time_end          					DATETIME2,
  duration								DECIMAL(10,0) NOT NULL,
  
  CONSTRAINT FK_event_ID_op FOREIGN KEY (event_id) REFERENCES cip_report.dbo.history_events (id)
);
GO

CREATE INDEX idx_history_events_op_event_id ON cip_report.dbo.history_events_op (event_id);
CREATE INDEX idx_history_events_op_time_start ON cip_report.dbo.history_events_op (time_start);
CREATE INDEX idx_history_events_op_time_end ON cip_report.dbo.history_events_op (time_end);

--------------------------------------------------------------------------------
-- Versions table
--------------------------------------------------------------------------------

insert into cip_report.dbo.versions (version_number) values (1.02);
GO