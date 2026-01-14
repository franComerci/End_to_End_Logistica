USE logistica;

CREATE OR ALTER PROCEDURE spLimpiarDatos
AS 
BEGIN
    SET NOCOUNT ON;
    PRINT 'Iniciando proceso de limpieza...';
    
    WITH datosUnicos AS (
        SELECT 
            enviosID, 
            fechaIngreso,  
            estado, 
            ROW_NUMBER() OVER (PARTITION BY enviosID ORDER BY fechaIngreso DESC) as nroFila
        FROM Staging  
        WHERE fechaIngreso IS NOT NULL AND costo >= 0
    )
    INSERT INTO Fact(enviosID, fecha, costo, estado)
    SELECT 
        d.enviosID, 
        d.fechaIngreso, 
        d.costo, 
        d.estado 
    FROM datosUnicos d

    LEFT JOIN Fact f ON d.enviosID = f.enviosID
    WHERE d.nroFila = 1
      AND f.enviosID IS NULL; 

    DECLARE @Nuevos INT = @@ROWCOUNT;
    PRINT 'Registros nuevos insertados: ' + CAST(@Nuevos AS VARCHAR);

    TRUNCATE TABLE Staging;
    PRINT 'Staging vaciado.';
END
GO
