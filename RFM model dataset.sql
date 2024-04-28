SELECT 
h.strSoldToPartnerName as "Customer Name",
h.dteDeliveryDate as Date, 
SUM(numQuantity) as "Total Quantity",
 SUM(r.numDeliveryValue) as "Total Sales Amount"
From 
 
  [APON].[pos].[tblPosDeliveryHeader] h 
  JOIN [APON].[pos].[tblPosDeliveryRow] r ON h.intDeliveryId = r.intDeliveryId
WHERE 
  h.isActive = 1 
  AND r.isActive = 1 
  AND h.dteDeliveryDate >= '2024-02-01'
  Group by
h.strSoldToPartnerName ,
h.dteDeliveryDate 