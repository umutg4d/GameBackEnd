## GET /get-daily-user-statistics

Returns a user's daily statistics for the requested `user_id` and `stat_date`.

## POST /update-user-daily-stats

It fetches the user_id and which statistic should be changed, delta count of that statistic and the target date which indicates when this statistics change was made and update the UserDailyStatistics table using these values.
