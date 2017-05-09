from abc import ABCMeta, abstractmethod

from InferenceEngine.ForwardChainingWithVariables import ForwardChainingWithVariables
from InferenceEngine.Knowledge import KnowledgeBase
from InferenceEngine.RuleWithVariable import RuleWithVariable
from InferenceEngine.Unificator import Unificator
from Scraping import WikiRules
from Scraping import WikiScraper
from Scraping.WikiRules import B_RULES


class InferenceChecker(metaclass=ABCMeta):
    def __init__(self, rules, facts=None):
        if facts is None:
            facts = []
        self.rules = rules

        self.bc = KnowledgeBase(lambda descr: RuleWithVariable(descr[0], descr[1]))
        self.bc.addFacts(facts)
        self.bc.addRules(rules)
        unificator = Unificator()
        self.moteur = ForwardChainingWithVariables(knowledge=self.bc, method=unificator)

    def addFact(self, fact):
        self.bc.addFact(fact)

    def addFacts(self, facts):
        self.bc.addFacts(facts)

    @abstractmethod
    def checkIfErrors(self):
        pass


class BirthInferenceChecker(InferenceChecker):
    def __init__(self, facts=None):
        super().__init__(B_RULES, facts)

    def checkIfErrors(self):

        # Insert the url to check from
        wikiData = \
            WikiScraper.run(
                ['http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_page_test_-_Secundinus_Aurelianus'])

        births = list(wikiData.births)
        deaths = list(wikiData.deaths)

        birthsFacts = list(map(lambda x: x.toPredicate(), births))
        deathFacts = list(map(lambda x: x.toPredicate(), deaths))

        self.addFacts(birthsFacts)
        self.addFacts(deathFacts)

        for d in deaths:
            for b in births:
                self.addFact(d.date.isBeforePredicate(b.date))

        for i in range(0, len(births)):
            for j in range(i, len(births)):
                self.addFact(births[i].date.isDifferentPredicate(births[j].date))

        for i in range(0, len(deaths)):
            for j in range(i, len(deaths)):
                self.addFact(deaths[i].date.isDifferentPredicate(deaths[j].date))

        return self.moteur.chain()


class EncounterInferenceChecker(InferenceChecker):
    def __init__(self, facts=None):
        super().__init__(WikiRules.ENCOUNTER_RULES, facts)

    def checkIfErrors(self):

        # Insert the url to check from
        resData = \
            WikiScraper.run(
                ['http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_page_test_-_Secundinus_Aurelianus'])

        encounters = resData.encounters
        positions = resData.positions

        encountersFacts = list(map(lambda x: x.toPredicate(), encounters))
        positionsFacts = list(map(lambda x: x.toPredicate(), positions))

        self.addFacts(encountersFacts)
        self.addFacts(positionsFacts)

        for e in encounters:
            for p in positions:
                temp = e.location.isFarPredicate(p.location)
                if temp is not None:
                    if e.person1 == p.person:
                        self.addFact(temp)
                    if e.person2 == p.person:
                        self.addFact(temp)

        return self.moteur.chain()


class ElectionInferenceChecker(InferenceChecker):
    def __init__(self, facts=None):
        super().__init__(WikiRules.ELECTION_RULES, facts)

    def checkIfErrors(self):

        resData = \
            WikiScraper.run(
                ['http://wikipast.epfl.ch/wikipast/index.php/InferenceBot_page_test_-_Secundinus_Aurelianus'])

        births = resData.births
        deaths = resData.deaths
        elections = resData.elections

        electionsFacts = list(map(lambda x: x.toPredicate(), elections))
        birthsFacts = list(map(lambda x: x.toPredicate(), births))
        deathFacts = list(map(lambda x: x.toPredicate(), deaths))

        self.addFacts(electionsFacts)
        self.addFacts(birthsFacts)
        self.addFacts(deathFacts)

        for e in elections:
            for d in deaths:
                self.addFact(d.date.isBeforePredicate(e.date))
            for b in births:
                self.addFact(e.date.isBeforePredicate(b.date))

        return self.moteur.chain()


if __name__ == '__main__':
    t = EncounterInferenceChecker()
    print(t.checkIfErrors())
