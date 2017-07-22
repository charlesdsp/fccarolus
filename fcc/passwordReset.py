from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models.query_utils import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from fccarolus.settings import DEFAULT_FROM_EMAIL
from django.views.generic import *
from fcc.forms import PasswordResetRequestForm, SetPasswordForm
from django.contrib import messages
from django.contrib.auth.models import User


class ResetPasswordRequestView(FormView):
    # code for template is given below the view's code
    template_name = "fcc/password.html"
    success_url = '/fcc/login'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        """
        This method here validates the if the input is an email address or not.
        Its return type is boolean, True if the input is a email address or False if its not.
        """
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def reset_password(self, user, request):
        c = {
            'email': user.email,
            'domain': request.META['HTTP_HOST'],
            'site_name': 'FC Carolus',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
        }
        subject_template_name = 'password_reset_subject.txt'
        # copied from
        # django/contrib/admin/templates/registration/password_reset_subject.txt
        # to templates directory
        email_template_name = 'password_reset_email.html'
        # copied from
        # django/contrib/admin/templates/registration/password_reset_email.html
        # to templates directory
        subject = loader.render_to_string(subject_template_name, c)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        email = loader.render_to_string(email_template_name, c)
        send_mail(subject, email, DEFAULT_FROM_EMAIL,
                  [user.email], fail_silently=False)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                data = form.cleaned_data["email_or_username"]
                print(data)
            # uses the method written above
            if self.validate_email_address(data) is True:
                '''
                If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
                '''
                associated_users = User.objects.filter(
                    Q(email=data) | Q(username=data))
                if associated_users.exists():
                    for user in associated_users:
                        c = {
                                'email': user.email,
                                'domain': request.META['HTTP_HOST'],
                                'site_name': 'your site',
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                'user': user,
                                'token': default_token_generator.make_token(user),
                                'protocol': 'http',
                                }
                        subject_template_name = 'fcc/password_reset_subject.txt'
                        # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                        email_template_name = 'fcc/password_reset_email.html'
                        # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                    result = self.form_valid(form)
                    messages.success(
                        request, "Un email a été envoyé à {0}. Consultez votre email pour poursuivre votre demande.".format(data))
                    return result
                result = self.form_invalid(form)
                messages.error(
                    request, 'Adresse email inconnue')
                return result
            else:
                '''
                If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
                '''
                associated_users = User.objects.filter(username=data)
                if associated_users.exists():
                    for user in associated_users:
                        for user in associated_users:
                            c = {
                                    'email': user.email,
                                    'domain': request.META['HTTP_HOST'],
                                    'site_name': 'your site',
                                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                    'user': user,
                                    'token': default_token_generator.make_token(user),
                                    'protocol': 'http',
                                    }
                        subject_template_name = 'fcc/password_reset_subject.txt'
                        # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                        email_template_name = 'fcc/password_reset_email.html'
                        # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                    result = self.form_valid(form)
                    messages.success(
                        request, "Un email a été envoyé à {0}. Consultez votre email pour poursuivre votre demande.".format(data))
                    return result
                result = self.form_invalid(form)
                messages.error(
                    request, 'Login inconnu.')
                return result
            messages.error(request, 'Invalid Input')
        except Exception as e:
            print(e)
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):
    template_name = "fcc/password.html"
    success_url = '/fcc/login'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(
                    request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(
                request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)
