CREATE TABLE `delhi_metro_trips` (
  `ID` int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
  `TripID` bigint DEFAULT NULL,
  `Date` datetime DEFAULT NULL,
  `From_Station` text,
  `To_Station` text,
  `Distance_km` double DEFAULT NULL,
  `Fare` double DEFAULT NULL,
  `Cost_per_passenger` double DEFAULT NULL,
  `Passengers` double DEFAULT NULL,
  `Ticket_Type` text,
  `Remarks` text
) ;