-- SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUsers that computes
-- and store the average weighted score for all students.

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE user_id INT;

    -- Declare a cursor to get the list of user IDs
    DECLARE user_cursor CURSOR FOR 
        SELECT id FROM users;

    -- Declare continue handler for the cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- Open the cursor
    OPEN user_cursor;

    -- Start looping through users
    user_loop: LOOP
        FETCH user_cursor INTO user_id;

        IF done THEN
            LEAVE user_loop;
        END IF;
	
	SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
	INTO @get_avg, @get_weight
       	FROM users INNER JOIN corrections
	ON corrections.user_id = users.id
	INNER JOIN projects ON projects.id = corrections.project_id
	WHERE users.id = user_id;

        -- Update each user with a new value
        UPDATE users SET average_score = @get_avg / @get_weight WHERE id = user_id;

    END LOOP;
END//
DELIMITER ;
