from django.urls import include, path, re_path

from .views import (
    AboutView,
    ContactView,
    EmailSubscriptionView,
    HomeView,
    LogoutView,
    PrivacyPolicy,
    ServiceView,
    SignInView,
    SignUpView,
    SitemapView,
    TermsOfUse,
)

app_name = "Ehub"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    re_path(r'^sitemap\.xml/$', SitemapView.as_view(), name="sitemap"),
    re_path(r'^robots\.txt', include('robots.urls')),
    path("email-subscription/", EmailSubscriptionView.as_view(), name="email-subscription"),
    path("services/", ServiceView.as_view(), name="services"),    
    path("about-us/", AboutView.as_view(), name="about-us"),
    path("contact-us/", ContactView.as_view(), name="contact-us"),
    path("privacy-policy/", PrivacyPolicy.as_view(), name="privacy-policy"),
    path("termsofuse/", TermsOfUse.as_view(), name="termsofuse"),
    # Authentication
    path("account/sign-in/", SignInView.as_view(), name="sign-in"),
    path("account/sign-up/", SignUpView.as_view(), name="sign-up"),
    path("account/logout/", LogoutView.as_view(), name="logout"),
]
