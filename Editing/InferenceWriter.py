from Editing.PrettyPrinter import pretty
from Editing.WikiWriter import write_on_page_after_title, delete_on_page_if_exists
from Scraping.WikiGraph import WikiGenealogyTree
from Scraping.WikiInference import *


def write_inferences(resData, allLinks):

    birth_facts = BirthInferenceChecker()
    multibirth_facts = MultiBirthInferenceChecker()
    multideath_facts = MultiDeathInferenceChecker()
    encounter_facts = EncounterInferenceChecker()
    election_bef_birth_facts = ElectionBefBirthInferenceChecker()
    election_aft_death_facts = ElectionAftDeathInferenceChecker()
    mariage_bef_birth_facts = MariageBefBirthInferenceChecker()
    mariage_aft_death_facts = MariageAftDeathInferenceChecker()
    divorce_facts = DivorceInferenceChecker()

    wikiGenalogyTree = WikiGenealogyTree()
    wikiGenalogyTree.addData(resData)
    wikiGenalogyTree.generateGraph()

    list_birth_facts = birth_facts.checkIfErrors(resData)
    list_multibirth_facts = multibirth_facts.checkIfErrors(resData)
    list_multideath_facts = multideath_facts.checkIfErrors(resData)
    list_encounter_facts = encounter_facts.checkIfErrors(resData)
    list_election_bef_birth_facts = election_bef_birth_facts.checkIfErrors(resData)
    list_election_aft_death_facts = election_aft_death_facts.checkIfErrors(resData)
    list_mariage_bef_birth_facts = mariage_bef_birth_facts.checkIfErrors(resData)
    list_mariage_aft_death_facts = mariage_aft_death_facts.checkIfErrors(resData)
    list_divorce_facts = divorce_facts.checkIfErrors(resData)

    list_facts = []
    if list_birth_facts is not None:
        list_facts.extend(list_birth_facts)
    if list_multibirth_facts is not None:
        list_facts.extend(list_multibirth_facts)
    if list_multideath_facts is not None:
        list_facts.extend(list_multideath_facts)
    if list_encounter_facts is not None:
        list_facts.extend(list_encounter_facts)
    if list_election_bef_birth_facts is not None:
        list_facts.extend(list_election_bef_birth_facts)
    if list_election_aft_death_facts is not None:
        list_facts.extend(list_election_aft_death_facts)
    if list_mariage_bef_birth_facts is not None:
        list_facts.extend(list_mariage_bef_birth_facts)
    if list_mariage_aft_death_facts is not None:
        list_facts.extend(list_mariage_aft_death_facts)
    if list_divorce_facts is not None:
        list_facts.extend(list_divorce_facts)

    (list_filtered, pagesWithNothing) = pretty(list_facts, allLinks)
    writeOnPages(list_filtered)

    for url in pagesWithNothing:
        delete_on_page_if_exists(url)

def writeOnPages(factsWithPages):
    dict = {}
    for fact in factsWithPages:
        for page in fact[1]:
            value = dict.get(page)
            if value is None:
                dict[page] = [fact[0]]
            else:
                value.append(fact[0])
    for k, e in dict.items():
        head, *tail = e

        head = '* ' + head
        tail = [head] + tail

        s = '\n* '.join(tail)
        write_on_page_after_title(s, k)
