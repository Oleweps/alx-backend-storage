-- SQL script that creates a stored procedure
-- ComputeAverageScoreForUser that computes
-- and store the average score for a student

DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
   SELECT AVG(corrections.score) INTO @get_avg
   FROM users INNER JOIN corrections
   ON corrections.user_id = users.id
   WHERE users.id = user_id;

   UPDATE users SET average_score = @get_avg WHERE id = user_id;
END//
DELIMITER ;
