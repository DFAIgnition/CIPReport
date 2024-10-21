USE [cip_report]
GO  

CREATE TABLE cip_report.dbo.circuit_last_check (
  circuit_id        INT PRIMARY KEY,
  last_check_time   DATETIME2,
  FOREIGN KEY (circuit_id) REFERENCES cip_report.dbo.circuit (id)
);
GO

--------------------------------------------------------------------------------
-- Versions table
--------------------------------------------------------------------------------

insert into cip_report.dbo.versions (version_number) values (1.03);
GO