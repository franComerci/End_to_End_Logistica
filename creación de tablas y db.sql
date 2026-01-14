if not exists (select * from sys.databases where name = 'logistica')
begin
	create database logistica
end

go

use logistica 
go

--esta tabla va a ser para la "zona sucia" → los datos como vienen
if object_id('Staging', 'U') is null
begin
	create table Staging (
		enviosID int, 
		fecha date,
		costo decimal(10,2),
		estado varchar(50),
		fechaIngreso datetime default getdate()
	);
end
go

--esta seria la tabla final → si un dato no cumple con el script no entra
if object_id('Fact', 'U') is null
begin
	create table Fact (
		enviosID int primary key,
		fecha date not null, 
		costo decimal(10,2) check(costo >= 0),
		fechaProcesado datetime default getdate()
	);
end
go