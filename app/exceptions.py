class UserNotExistsError(Exception):
    pass

class AccountNotExistsError(Exception):
    pass

class SameAccountError(Exception):
    pass

class NegativeValueError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

class NotEnoughtPermissionsError(Exception):
    pass