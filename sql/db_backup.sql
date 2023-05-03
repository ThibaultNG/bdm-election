

-- drop all tables
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- give access to postgres
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

-- create tables
-- dimensional tables
CREATE TABLE state (
    id_state SERIAL PRIMARY KEY,
    state_name VARCHAR(255),
    po_code VARCHAR(2),
    fips_code INTEGER,
    cen_code INTEGER,
    ic_code INTEGER
);

CREATE TABLE district (
    id_district SERIAL PRIMARY KEY,
    number_district INTEGER,
    id_state INTEGER NOT NULL REFERENCES state(id_state)
);

CREATE TABLE year (
    id_year SERIAL PRIMARY KEY,
    year INTEGER
);

CREATE TABLE party (
    id_party SERIAL PRIMARY KEY,
    name_party VARCHAR(255)
);

CREATE TABLE person (
    id_person SERIAL PRIMARY KEY,
    name_person VARCHAR(255)
);

CREATE TABLE candidate (
    id_candidate SERIAL PRIMARY KEY,
    write_in_candidate BOOLEAN,
    fusion_ticket_candidate BOOLEAN,
    id_party INTEGER NOT NULL REFERENCES party(id_party),
    id_person INTEGER NOT NULL REFERENCES person(id_person)
);

-- factual tables
CREATE TABLE fait_de_vote (
    id_district INTEGER NOT NULL REFERENCES district(id_district),
    id_year INTEGER NOT NULL REFERENCES year(id_year),
    id_candidate INTEGER NOT NULL REFERENCES candidate(id_candidate),
    candidate_vote INTEGER,
    total_vote INTEGER,
    run_off_vote BOOLEAN,
    special_vote BOOLEAN,
    PRIMARY KEY (id_district, id_year, id_candidate)
);