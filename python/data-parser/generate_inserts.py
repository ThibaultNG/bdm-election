import insert_state
import insert_district
import insert_year
import insert_party
import insert_person
import insert_candidate
import insert_vote

state = insert_state.insert_state()
district = insert_district.insert_district()
year = insert_year.insert_year()
person = insert_person.insert_person()
party = insert_party.insert_party()
candidate = insert_candidate.insert_candidate()
vote = insert_vote.insert_vote()

insert_all = state + district + year + person + party + candidate + vote

with open("../../sql/insert_all.sql", "w") as file:
    file.write(insert_all)
    file.close()

print("ALL FINISHED")
