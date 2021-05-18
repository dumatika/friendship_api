from rest_framework.exceptions import ErrorDetail

FRIENDSHIP_WITH_YOURSELF_ERROR = ErrorDetail(
    string='You cannot create friendship with yourself',
    code='unique'
)
