CREATE OR REPLACE FUNCTION register_user (ruid bigint)
RETURNS void
LANGUAGE plpgsql
AS $$
DECLARE known boolean;
BEGIN
    SELECT registered_user(ruid) INTO known;
    IF NOT known THEN 
        INSERT INTO users (uid) VALUES (ruid);
    END IF;
END;
$$;

CREATE OR REPLACE FUNCTION registered_user (ruid bigint)
RETURNS boolean
LANGUAGE plpgsql
AS $$
    BEGIN
        RETURN EXISTS(SELECT 1 FROM users where uid = ruid);
    END;
$$;
