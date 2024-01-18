-- A SQL script that creates a stored procedure ComputeAverageScoreForUser

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT)
BEGIN
    DECLARE avg_score FLOAT;

    SELECT AVG(score) INTO avg_score
    FROM corrections AS C
    WHERE C.user_id = user_id;

    IF avg_score IS NOT NULL THEN
        UPDATE users
        SET average_score = avg_score
        WHERE id = user_id;
    ELSE
    END IF;
END;
$$
DELIMITER ;
