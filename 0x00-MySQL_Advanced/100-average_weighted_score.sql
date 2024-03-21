-- SQL script that creates a stored procedure
-- ComputeAverageScoreForUser that computes
-- and store the average score for a student

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
   SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
   INTO @get_avg, @get_weight
   FROM users INNER JOIN corrections
   ON corrections.user_id = users.id
   INNER JOIN projects ON projects.id = corrections.project_id
   WHERE users.id = user_id;

   UPDATE users SET average_score = @get_avg / @get_weight WHERE id = user_id;
END//
DELIMITER ;
