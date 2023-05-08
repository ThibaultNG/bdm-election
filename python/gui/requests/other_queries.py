winning_candidate_by_year_and_district = """
    SELECT y.year_label, d.district_number, max(vf.id_candidate) FROM vote_fact vf
    JOIN district d on vf.id_district = d.id_district
    JOIN state s on d.id_state = s.id_state
    JOIN year y on vf.id_year = y.id_year
    JOIN candidate c on vf.id_candidate = c.id_candidate
    JOIN person pe on c.id_person = pe.id_person
    JOIN party pa on c.id_party = pa.id_party
    GROUP BY y.id_year, d.id_district, vf.candidate_vote
"""

all_write_in_winners = """
    SELECT y.year_label, d.district_number, p.person_name, pa.party_name
    FROM vote_fact vf
    JOIN year y ON vf.id_year = y.id_year
    JOIN district d ON vf.id_district = d.id_district
    JOIN candidate c ON vf.id_candidate = c.id_candidate
    JOIN person p ON c.id_person = p.id_person
    JOIN party pa ON pa.id_party = c.id_party
    WHERE (vf.id_year, vf.id_district, vf.candidate_vote) IN (
        SELECT id_year, id_district, MAX(candidate_vote)
        FROM vote_fact
        GROUP BY id_year, id_district
    ) AND pa.party_name = 'WRITE-IN';
"""

number_of_seats_by_party = """
    SELECT y.year_label, p.party_name, COUNT(*) AS seat_count
    FROM (
      SELECT vf.id_year, vf.id_district, MAX(vf.candidate_vote) AS max_vote
      FROM vote_fact vf
      GROUP BY vf.id_year, vf.id_district
    ) AS max_votes
    JOIN vote_fact vf ON vf.id_year = max_votes.id_year AND vf.id_district = max_votes.id_district AND vf.candidate_vote = max_votes.max_vote
    JOIN candidate c ON vf.id_candidate = c.id_candidate
    JOIN party p ON c.id_party = p.id_party
    JOIN year y ON vf.id_year = y.id_year
    GROUP BY y.year_label, p.party_name
"""