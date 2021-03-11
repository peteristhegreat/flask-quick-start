from wtforms.widgets import PasswordInput, CheckboxInput, TextInput
from wtforms.widgets.html5 import EmailInput


class BootstrapVerifyEmail(EmailInput):
    """Bootstrap Validator for email"""

    def __init__(self, error_class=u"is-invalid"):
        super(BootstrapVerifyEmail, self).__init__()
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop("class", "") or kwargs.pop("class_", "")
            kwargs["class"] = u"%s %s" % (self.error_class, c)
        return super(BootstrapVerifyEmail, self).__call__(field, **kwargs)


class BootstrapVerifyPassword(PasswordInput):
    """Bootstrap Validator for password"""

    def __init__(self, error_class=u"is-invalid"):
        super(BootstrapVerifyPassword, self).__init__()
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop("class", "") or kwargs.pop("class_", "")
            kwargs["class"] = u"%s %s" % (self.error_class, c)
        return super(BootstrapVerifyPassword, self).__call__(field, **kwargs)


class BootstrapVerifyBoolean(CheckboxInput):
    """Bootstrap Validator for boolean"""

    def __init__(self, error_class=u"is-invalid"):
        super(BootstrapVerifyBoolean, self).__init__()
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop("class", "") or kwargs.pop("class_", "")
            kwargs["class"] = u"%s %s" % (self.error_class, c)
        return super(BootstrapVerifyBoolean, self).__call__(field, **kwargs)


class BootstrapVerifyText(TextInput):
    """Bootstrap Validator for text"""

    def __init__(self, error_class=u"is-invalid"):
        super(BootstrapVerifyText, self).__init__()
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop("class", "") or kwargs.pop("class_", "")
            kwargs["class"] = u"%s %s" % (self.error_class, c)
        return super(BootstrapVerifyText, self).__call__(field, **kwargs)