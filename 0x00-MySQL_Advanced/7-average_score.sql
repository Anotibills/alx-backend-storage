-- A SQL script that creates a stored procedure ComputeAverageScoreForUser

DELIMITER $$
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
CREATE PROCEDURE ComputeAverageScoreForUser(IN `user_id` INT)
BEGIN
    DECLARE avg_score FLOAT;

    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE corrections.user_id = user_id;

    IF avg_score IS NOT NULL THEN
        UPDATE users
        SET average_score = avg_score
        WHERE id = user_id;
    END IF;
END $$
DELIMITER ;
