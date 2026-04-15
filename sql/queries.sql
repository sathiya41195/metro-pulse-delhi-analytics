#1.Which metro routes have the highest passenger traffic?
SELECT `From_Station`, `To_Station`, SUM(passengers) AS traffic_count FROM delhi_metro_trips
GROUP BY `From_Station`, `To_Station`
order by 3 desc LIMIT 1;
#2. Which routes generate the highest total revenue?
SELECT `From_Station`, `To_Station`, SUM(Fare) AS Total_Revenue FROM delhi_metro_trips
GROUP BY `From_Station`, `To_Station`
order by 3 desc LIMIT 1;

#3. What is the average fare for each route?
SELECT `From_Station`, `To_Station`, AVG(Fare) AS Avg_Revenue FROM delhi_metro_trips
GROUP BY `From_Station`, `To_Station`
order by 3 desc;

#4. Which routes have the longest travel distances?

SELECT `From_Station`, `To_Station`, Max(`Distance_km`) AS Longest_distance FROM delhi_metro_trips
GROUP BY `From_Station`, `To_Station`
order by 3 desc LIMIT 1;

#5. Which stations have the highest number of trip departures?

SELECT `From_Station`,  SUM(passengers) AS High_departure FROM delhi_metro_trips
GROUP BY `From_Station`
order by 2 desc LIMIT 1;

#6. Which stations receive the highest number of passengers?

SELECT To_Station,  SUM(Passengers) AS High_Receiver FROM delhi_metro_trips
GROUP BY To_Station
order by 2 desc LIMIT 1;

#7. What are the top 10 most frequently used metro stations?

SELECT Station, SUM(Trip_count) AS Frequently_used_trips FROM (
    SELECT `From_Station` AS Station,  count(`TripID`) AS trip_count FROM delhi_metro_trips
    GROUP BY `From_Station`
    UNION
    SELECT To_Station,  count(`TripID`) AS trip_count FROM delhi_metro_trips
    GROUP BY To_Station
) AS trip_data
GROUP BY Station
order by 2 desc lIMIT 10;

#8. Which station pairs are most frequently used for travel?
# need to change the logic 
SELECT A.From_station, A.To_station, A.Frequently_used_count + COALESCE(B.Frequently_used_count,0) AS Most_used FROM(SELECT `From_Station`,To_Station,  count(`TripID`) AS Frequently_used_count FROM delhi_metro_trips
GROUP BY `From_Station`,To_Station) AS A
LEFT JOIN (SELECT `From_Station`,To_Station,  count(`TripID`) AS Frequently_used_count FROM delhi_metro_trips
GROUP BY `From_Station`,To_Station) AS B ON A.From_station = B.To_station AND A.To_station = B.From_station
ORDER BY 3 DESC LIMIT 1;

#9. What is the total revenue generated from all trips?

SELECT SUM(`Fare`) AS total_revenue FROM delhi_metro_trips;
#10. What is the average fare per trip?

SELECT AVG(`Fare`) AS average_revenue FROM delhi_metro_trips;
#11. Which routes generate the highest revenue per kilometer?

SELECT `From_Station`, `To_Station`, SUM(`Fare`)/Sum(`Distance_km`) AS revenue_per_km FROM delhi_metro_trips
GROUP BY `From_Station`, `To_Station`
order by 3 desc LIMIT 1;

#12. Which ticket type generates the highest revenue?

select Ticket_Type, SUM(Fare) AS Total_Revenue from delhi_metro_trips
WHERE Ticket_Type IS NOT NULL
GROUP BY Ticket_Type
order by 2 desc LIMIT 1;

#13. What is the average number of passengers per trip?

SELECT AVG(`Passengers`) AS average_passengers FROM delhi_metro_trips;

#14. Which trips recorded the highest passenger counts?

SELECT `From_Station`,`To_Station`,Max(`passengers`) AS highest_passengers FROM delhi_metro_trips
GROUP BY `From_Station`, `To_Station`
order by 3 desc LIMIT 1;

#15. What is the passenger distribution by ticket type?

SELECT `Ticket_type`, SUM(`Passengers`) AS total_passengers FROM delhi_metro_trips
WHERE Ticket_Type IS NOT NULL
GROUP BY `Ticket_type`
order by 2 desc;

#16. What is the total passenger count for each station?

SELECT station, sum(Total_passenger) AS total_passengers FROM (
    SELECT `From_Station` AS station,  SUM(Passengers) AS Total_passenger FROM delhi_metro_trips
    GROUP BY `From_Station`
    UNION
    SELECT To_Station AS station,  SUM(Passengers) AS Total_passenger FROM delhi_metro_trips
    GROUP BY To_Station
) AS passenger_data
GROUP BY station
order by 2 desc;

#17. How many trips occur during peak, off-peak, festival, and weekend conditions?

SELECT `Remarks`, COUNT(`TripID`) AS trip_count FROM delhi_metro_trips
WHERE `Remarks` in('festival', 'peak', 'off-peak', 'weekend')
GROUP BY `Remarks` order by 2 desc;

#18. Which travel condition generates the highest revenue?

SELECT `Remarks`, SUM(`Fare`) AS total_revenue FROM delhi_metro_trips
#WHERE `Remarks` in('festival', 'peak', 'off-peak', 'weekend')
GROUP BY `Remarks` order by 2 desc;

#19. What is the monthly passenger trend across the dataset?
# will change the logic to calculate month alone
SELECT monthname(`Date`) AS month, SUM(`passengers`) AS monthly_trend FROM delhi_metro_trips
GROUP BY month
order by 2 desc

#20. Which travel condition has the highest average passenger count per trip?

SELECT `Remarks`, AVG(`passengers`) AS Avg_revenue FROM delhi_metro_trips
#WHERE `Remarks` in('festival', 'peak', 'off-peak', 'weekend')
GROUP BY `Remarks`
order by 2 desc;
