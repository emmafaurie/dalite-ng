from django.contrib.auth.models import User
from django.core import mail
from django.urls import reverse

from peerinst.forms import SignUpForm
from peerinst.models import NewUserRequest, UserUrl


def test_signup__get(client):
    resp = client.get(reverse("sign_up"))
    assert "registration/sign_up.html" in [t.name for t in resp.templates]
    assert isinstance(resp.context["form"], SignUpForm)


def test_signup__post(client, mocker):
    data = {"username": "test", "email": "test@test.com", "url": "test.com"}
    mail_admins = mocker.patch("peerinst.views.admin_.mail_admins_async")
    resp = client.post(reverse("sign_up"), data)
    assert "registration/sign_up_done.html" in [t.name for t in resp.templates]
    assert User.objects.filter(
        username=data["username"], email=data["email"]
    ).exists()
    assert (
        UserUrl.objects.get(user__username=data["username"]).url
        == f"http://{data['url']}"
    )
    assert NewUserRequest.objects.filter(
        user__username=data["username"]
    ).exists()
    mail_admins.assert_called_once()


def test_signup__backend_missing(client, mocker):
    data = {"username": "test", "email": "test@test.com", "url": "test.com"}
    settings = mocker.patch("peerinst.views.admin_.settings")
    settings.EMAIL_BACKEND = ""
    mail_admins = mocker.patch("peerinst.views.admin_.mail_admins_async")
    resp = client.post(reverse("sign_up"), data)
    assert resp.status_code == 503


def test_new_user_approval_page(client, staff, new_user_requests):
    assert client.login(username=staff.username, password="test")
    resp = client.get(reverse("admin--new-user-approval"))
    assert "admin/peerinst/new_user_approval.html" in [
        t.name for t in resp.templates
    ]
    assert len(new_user_requests) == len(resp.context["new_users"])
    for req in new_user_requests:
        assert req.user.username in [
            u["username"] for u in resp.context["new_users"]
        ]

    for i, u in enumerate(resp.context["new_users"]):
        assert all(
            u_["date_joined"] <= u["date_joined"]
            for u_ in resp.context["new_users"][i + 1 :]
        )


def test_verify_user__approve(client, staff, new_user_requests):
    client.login(username=staff.username, password="test")
    user = new_user_requests[0].user
    assert not user.is_active

    resp = client.post(
        reverse("admin--verify-user"),
        {"username": user.username, "approve": True},
        content_type="application/json",
    )
    assert resp.status_code == 200

    user_ = User.objects.get(username=user.username)
    assert user_.is_active

    assert mail.outbox[0].subject == "Please verify your myDalite account"

    assert not NewUserRequest.objects.filter(user=user).exists()


def test_verify_user__refuse(client, staff, new_user_requests):
    client.login(username=staff.username, password="test")
    user = new_user_requests[0].user
    assert not user.is_active

    resp = client.post(
        reverse("admin--verify-user"),
        {"username": user.username, "approve": False},
        content_type="application/json",
    )
    assert resp.status_code == 200

    assert not User.objects.filter(username=user.username).exists()

    assert not mail.outbox

    assert not NewUserRequest.objects.filter(
        user__username=user.username
    ).exists()
