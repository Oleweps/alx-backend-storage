-- script that creates a stored procedure
-- AddBonus that adds a new correction for a student.

DELIMITER //
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name CHAR(255), IN score INT)
BEGIN
   SELECT COUNT(*) INTO @value_exists
   FROM projects 
   WHERE name = project_name;

   IF @value_exists < 1 THEN
      INSERT INTO projects (name) VALUES (project_name);
   END IF;
   
   SELECT id INTO @project_id
   FROM projects
   WHERE name = project_name;
   
   INSERT INTO corrections(user_id, project_id, score)
   VALUES (user_id, @project_id, score);
END//
DELIMITER ;
