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
DECLARE id integer;
BEGIN
    INSERT INTO greetings (content) VALUES (rtext) RETURNING greetings.gid INTO id;
    RETURN id;
    RETURN id;
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

CREATE OR REPLACE FUNCTION clean () 
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    DROP TABLE greetings;
    DROP FUNCTION register_user, registered_user, store_greeting;
END;
$$;
