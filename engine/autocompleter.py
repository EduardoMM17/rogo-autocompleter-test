
from .term_index import TermIndex, Term
from .utils import Utils

class Autocompleter:

    def __init__(self, term_index: TermIndex, utils: Utils) -> None:
        self.term_index = term_index
        self.utils = utils
        
    def suggestions(self, input: str) -> list[list[Term]]:
        input_words = input.split(' ')
        definitive_matches = self.get_definitive_matches(input_words)
        result = self.generate_suggestion_combinations(definitive_matches)
         
        return result


    def get_definitive_matches(self, input_list: list[str]) -> list[list[Term]]:
        definitive_matches = []
        index = 0
        while index < len(input_list):
            input_term = input_list[index]
            matched_terms = self.term_index.search(input_term)
            if not matched_terms:
                return []
            index, filtered_matched_terms = self.filter_matching_terms(input_list, matched_terms, index)
            definitive_matches.append(filtered_matched_terms)
            index += 1
        return definitive_matches


    def filter_matching_terms(self, input: list[str], matched_terms: list[Term], index: int) -> tuple[int, list[Term]]:
        filtered_matched_terms = []
        input = input[index:]
        for term in matched_terms:
            term_splitted = term.value.split(" ")
            if len(term_splitted) == 2:
                if len(input) == 1:
                    match = term_splitted[0].startswith(input[0])
                else:
                    match = term_splitted[0] == input[0] and term_splitted[1].startswith(input[1])
            elif len(term_splitted) == 3:
                if len(input) == 1:
                    match = term_splitted[0].startswith(input[0])
                elif len(input) == 2:
                    match = term_splitted[0] == input[0] and term_splitted[1].startswith(input[1])
                else:
                    match = term_splitted[0] == input[0] and term_splitted[1] == input[1] and term_splitted[2].startswith(input[2])
            else:
                continue

            if match:
                filtered_matched_terms.append(term)
                index += len(term_splitted) - 1
        if not filtered_matched_terms:
            filtered_matched_terms = matched_terms
        return index, filtered_matched_terms

    
    def generate_suggestion_combinations(self, definitive_matches: list[Term]) -> list[list[Term]]: 
        suggestion_combinations = []
        for terms in definitive_matches:
            if not suggestion_combinations:
                suggestion_combinations = [[term] for term in terms]
            else:
                if len(terms) == 1:
                    suggestion_combinations = [elem + [terms[0]] for elem in suggestion_combinations]
                else:
                    initial_list_size = len(suggestion_combinations)
                    suggestion_combinations = self.utils.copy_lists(suggestion_combinations, len(terms))
                    counter = 0
                    terms_index = 0
                    for elem in suggestion_combinations:
                        counter += 1
                        elem.append(terms[terms_index])
                        if counter % initial_list_size == 0:
                            terms_index += 1
                        
        return suggestion_combinations




