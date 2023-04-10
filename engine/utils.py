
from .term_index import Term

class Utils:
    def copy_lists(self, input_list: list[list[Term]], num_copies: int) -> list[list[Term]]:
        result = []
        for _ in range(num_copies):
            for inside_list in input_list:
                result.append(list(inside_list))
        return result