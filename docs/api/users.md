## GET /get-user
This endpoint looks for idfv and statistics date parameters from the GET request and firstly searches the database for the given idfv. If it is found, it also tries to get the user daily statistics data from the current day. And if there is no statistics data for the current day it inserts a new row for the current day's statistic. And if it is found it increases the session count by 1.

## POST /create-user
This endpoint gets the idfv parameter from the request parameters and create relevant user in the users table with this parameter. Besides that it creates a UserDailyStatistics row in the UserStatistics table with the given statistics date parameter.

## POST /update-user
This endpoint gets the relevant user by user_id and also all the saved attributes from the request parameter. And after fetching the relevant user by the user_id, it updates the user's attributes with the parameters inside these attributes.