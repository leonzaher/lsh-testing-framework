
class ExpressionData(object):
    def __init__(self, expression, index, is_duplicate, parent_expression, parent_index):
        self.expression = expression
        self.index = index
        self.is_duplicate = is_duplicate
        self.parent_expression = parent_expression
        self.parent_index = parent_index

    def __str__(self):
        return "ExpressionData(expression = {}, index = {}, is_duplicate = {}, parent_expression = {}, " \
               "parent_index = {}"\
            .format(self.expression, self.index, self.is_duplicate, self.parent_expression, self.parent_index)

    def __repr__(self):
        return self.__str__()
