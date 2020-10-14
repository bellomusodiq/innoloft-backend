from django.shortcuts import render
from .models import User, Account
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class CreateAccount(APIView):

    def post(self, request):
        errors = {}
        username = request.data.get('username')
        if not username:
            errors['username'] = 'username field is required'
        if username and User.objects.filter(username=username).first():
            errors['username'] = 'username has been taken'
        email = request.data.get('email')
        if not email:
            errors['email'] = 'email field is required'
        if email and User.objects.filter(email=email).first():
            errors['email'] = 'email has been taken'
        first_name = request.data.get('first_name')
        if not first_name:
            errors['first_name'] = 'first_name field is required'
        last_name = request.data.get('last_name')
        if not last_name:
            errors['last_name'] = 'last_name field is required'
        house_number = request.data.get('house_number')
        if not house_number:
            errors['house_number'] = 'house_number field is required'
        street = request.data.get('street')
        if not street:
            errors['street'] = 'street field is required'
        postal_code = request.data.get('postal_code')
        if not postal_code:
            errors['postal_code'] = 'postal_code field is required'
        password = request.data.get('password')
        if not password:
            errors['password'] = 'password field is required'
        country = request.data.get('country')
        if not country:
            errors['country'] = 'country field is required'

        if len(errors) > 0:
            return Response({'errors': errors}, 400)
        
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )   
        user.set_password(password)  
        user.save()
        account = Account.objects.create(
            user=user,
            house_number=house_number,
            street=street,
            postal_code=postal_code,
            country=country
        )  
        return Response({'message': 'user account created successfully'}, 201) 


class GetUser(APIView):

    def get(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            return Response({
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'house_number': user.account.house_number,
                'street': user.account.street,
                'postal_code': user.account.postal_code,
                'country': user.account.country
            }) 
        except User.DoesNotExist:
            return Response({'message': 'user not found'}, 404) 


    def patch(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            user.username = request.data.get('username', user.username)
            user.email = request.data.get('email', user.email)
            user.first_name = request.data.get('first_name', user.first_name)
            user.last_name = request.data.get('last_name', user.last_name)
            user.account.house_number = request.data.get('house_number', user.account.house_number)
            user.account.street = request.data.get('street', user.account.street)
            user.account.postal_code = request.data.get('postal_code', user.account.postal_code)
            user.account.country = request.data.get('country', user.account.country)
            user.account.save()
            user.save()
            return Response({'message': 'user update was successful'}) 
        except User.DoesNotExist:
            return Response({'message': 'user not found'}, 404) 



def jwt_response_payload_handler(token, user=None, request=None):
    return dict(token=token, userid=user.id)
