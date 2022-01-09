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

CREATE OR REPLACE FUNCTION store_greeting (rtext varchar)
RETURNS integer
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO greetings (content) VALUES (rtext);
    RETURN currval(pg_get_serial_sequence('greetings','gid'));
END;
$$;

CREATE OR REPLACE FUNCTION remove_greeting (rgid integer)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM greetings WHERE gid = rgid;
END;
$$;

CREATE OR REPLACE FUNCTION get_greeting (rgid integer)
RETURNS varchar
LANGUAGE plpgsql
AS $$
DECLARE result varchar;
BEGIN
    SELECT content FROM greetings WHERE gid = rgid INTO result;
    RETURN result;
END;
$$;

CREATE OR REPLACE FUNCTION get_random_user ()
RETURNS bigint
LANGUAGE plpgsql
AS $$
DECLARE uid bigint;
BEGIN
    SELECT * FROM users OFFSET floor(random() * (
		SELECT
			COUNT(*)
			FROM users)) LIMIT 1 INTO uid;
    RETURN uid;
END;
$$;

CREATE OR REPLACE FUNCTION clean () 
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    DROP TABLE greetings;
    DROP FUNCTION register_user, registered_user, store_greeting;
END;
$$;
