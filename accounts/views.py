from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.admin import User
from django.core.mail import EmailMessage

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .tokens import account_activation_token
from .serializers import UserSerializer

# Create your views here.


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUser(APIView):
    """
    Creates the user.
    """
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                print(type(uid))
                message = render_to_string('acc_activation.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': account_activation_token.make_token(user)
                })
                to_email = request.data['email']
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send
                return Response({'message': 'Please confirm your email address to complete the registration'},
                                status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


#activation link
def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        print(e)
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')  

