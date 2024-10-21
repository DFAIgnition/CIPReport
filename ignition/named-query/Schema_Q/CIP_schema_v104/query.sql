USE [cip_report]
GO  

--------------------------------------------------------------------------------
-- Add a note column to events for operator notes
--------------------------------------------------------------------------------

ALTER TABLE cip_report.dbo.history_events
ADD notes nvarchar(max);
GO

--------------------------------------------------------------------------------
-- Versions table
--------------------------------------------------------------------------------

insert into cip_report.dbo.versions (version_number) values (1.04);
GO