from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth import logout

class AuthView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
            }
        )
        if self.request.path == reverse("auth-register-basic"):
            context['form'] = RegistrationForm()
        elif self.request.path == reverse("auth-login-basic"):
            context['form'] = LoginForm()
        return context

    def post(self, request, *args, **kwargs):
        # Handle registration form submission
        if request.path == reverse("auth-register-basic"):
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect("auth-login-basic")
            else:
                # Use get_context_data to include layout_path and other context variables
                context = self.get_context_data()
                context["form"] = form  # Pass the form with errors
                return render(request, "auth_register_basic.html", context)

        # Handle login form submission
        elif request.path == reverse("auth-login-basic"):
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                login(request, form.get_user())
                return redirect("index")
            else:
                # Use get_context_data to include layout_path and other context variables
                context = self.get_context_data()
                context["form"] = form  # Pass the form with errors
                return render(request, "auth_login_basic.html", context)

        # Default GET request handling
        return super().get(request, *args, **kwargs)
    def logout_view(request):
        logout(request)
        return redirect('auth-login-basic')