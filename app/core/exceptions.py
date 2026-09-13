class UserAlreadyExistsError(Exception):
    pass

class ExpenseNotFoundError(Exception):
    pass


class ExpenseAccessDeniedError(Exception):
    pass


class ExpenseLockedError(Exception):
    pass

class InvlaidExpenseStateError(Exception):
    pass