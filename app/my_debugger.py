from inspect import currentframe


def get_line_number():
    cf = currentframe()
    return cf.f_back.f_lineno
