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
    fips_code VARCHAR(2),
    cen_code INTEGER,
    ic_code INTEGER
);

CREATE TABLE district (
    id_district SERIAL PRIMARY KEY,
    district_number VARCHAR(2),
    id_state INTEGER,
    CONSTRAINT fk_district_state FOREIGN KEY (id_state) REFERENCES state(id_state)
);

CREATE TABLE year (
    id_year SERIAL PRIMARY KEY,
    year_label INTEGER
);

CREATE TABLE party (
    id_party SERIAL PRIMARY KEY,
    party_name VARCHAR(255)
);

CREATE TABLE person (
    id_person SERIAL PRIMARY KEY,
    person_name VARCHAR(255)
);

CREATE TABLE candidate (
    id_candidate SERIAL PRIMARY KEY,
    fusion_ticket BOOLEAN,
    id_party INTEGER,
    id_person INTEGER,
    CONSTRAINT fk_candidate_party FOREIGN KEY (id_party) REFERENCES party(id_party),
    CONSTRAINT fk_candidate_person FOREIGN KEY (id_person) REFERENCES person(id_person)
);

-- factual tables
CREATE TABLE vote_fact (
    id_district INTEGER,
    id_year INTEGER,
    id_candidate INTEGER,
    candidate_vote INTEGER,
    total_vote INTEGER,
    run_off_election BOOLEAN,
    special_election BOOLEAN,
    PRIMARY KEY (id_district, id_year, id_candidate),
    CONSTRAINT fk_vote_district FOREIGN KEY (id_district) REFERENCES district(id_district),
    CONSTRAINT fk_vote_year FOREIGN KEY (id_year) REFERENCES year(id_year),
    CONSTRAINT fk_vote_candidate FOREIGN KEY (id_candidate) REFERENCES candidate(id_candidate)
);