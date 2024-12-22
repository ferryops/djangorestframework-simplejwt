from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Profile, Contract, TrainingSchedule
from .serializers import ProfileSerializer, ContractSerializer, TrainingScheduleSerializer, UserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import NotFound
from django.db.models import Q

# Register View
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        is_superuser = request.data.get('is_superuser', False)
        is_staff = request.data.get('is_staff', False)
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        is_active = request.data.get('is_active', True)

        if not username or not password or not email:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            is_superuser=is_superuser,
            is_staff=is_staff,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active
        )
        return Response({"message": "User created successfully", "user": {
            "username": user.username,
            "email": user.email,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active
        }}, status=status.HTTP_201_CREATED)

class DeleteUserView(APIView):
    permission_classes = [AllowAny]
    
    def delete(self, request, pk=None):
        if not request.user.is_superuser:
            return Response({"error": "You do not have permission to delete users"}, status=status.HTTP_403_FORBIDDEN)

        if not pk:
            return Response({"error": "User ID is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                raise User.DoesNotExist
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "data": user_data,
        })


# Profile View
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

    def put(self, request, pk=None):
        if pk:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "User ID is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# Contract View
class ContractView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                contract = Contract.objects.get(id=pk, user=request.user)
            except Contract.DoesNotExist:
                raise NotFound("Contract not found")
            serializer = ContractSerializer(contract)
            return Response(serializer.data)

        filters = Q(user=request.user)
        contract_id = request.query_params.get('id')
        user_id = request.query_params.get('user')

        if contract_id:
            filters &= Q(id=contract_id)
        if user_id:
            filters &= Q(user_id=user_id)

        contracts = Contract.objects.filter(filters)
        serializer = ContractSerializer(contracts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "Contract ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            contract = Contract.objects.get(id=pk, user=request.user)
        except Contract.DoesNotExist:
            raise NotFound("Contract not found")

        serializer = ContractSerializer(contract, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "Contract ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            contract = Contract.objects.get(id=pk, user=request.user)
        except Contract.DoesNotExist:
            raise NotFound("Contract not found")
        contract.delete()
        return Response({"message": "Contract deleted"}, status=status.HTTP_204_NO_CONTENT)

# Training Schedule View
class TrainingScheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            try:
                schedule = TrainingSchedule.objects.get(id=pk)
            except TrainingSchedule.DoesNotExist:
                raise NotFound("Training schedule not found")
            serializer = TrainingScheduleSerializer(schedule)
            return Response(serializer.data)

        schedule_id = request.query_params.get('id')
        user_id = request.query_params.get('user')

        if not schedule_id and not user_id:
            schedules = TrainingSchedule.objects.all()
        else:
            schedules = TrainingSchedule.objects.all()
            if schedule_id:
                schedules = schedules.filter(id=schedule_id)
            if user_id:
                schedules = schedules.filter(user_id=user_id)

        serializer = TrainingScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    def post(self, request):
        if 'user' in request.data and request.data['user'] != request.user.id:
            if request.user.is_staff:
                return Response(
                    {"error": "You do not have permission to assign user"},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        data = request.data.copy()
        data['user'] = request.data.get('user', request.user.id)

        serializer = TrainingScheduleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "Training schedule ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            schedule = TrainingSchedule.objects.get(id=pk)
        except TrainingSchedule.DoesNotExist:
            raise NotFound("Training schedule not found")

        serializer = TrainingScheduleSerializer(schedule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "Training schedule ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            schedule = TrainingSchedule.objects.get(id=pk)
        except TrainingSchedule.DoesNotExist:
            raise NotFound("Training schedule not found")

        schedule.delete()
        return Response({"message": "Training schedule deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

