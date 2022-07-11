from django.forms.widgets import DateTimeInput
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.fields import DateTimeField
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from .models import Architect, Cart, Design, DesignPayment, Item, Meeting, MeetingPayment, Order, OrderPayment, Project, User
from .serializers import ArchitectSerializer, CartSerializer, DesignSerializer, ItemSerializer, MeetingPaymentSerializer, MeetingSerializer, OrderSerializer, OrderPaymentSerializer, DesignPaymentSerializer, ProjectSerializer, UserSerializer
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from datetime import datetime


class UserCartApi(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def retrieve(self, request,  *args, **kwargs):
        queryset = Cart.objects.all()
        try:
            cart = queryset.get(user_id=kwargs['pk'])

        except Cart.DoesNotExist:
            try:
                user = User.objects.get(id=kwargs['pk'])
                new_cart = Cart.objects.create(user_id=user)
                new_cart.save()
                return Response(CartSerializer(new_cart).data, status=status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({'Error': 'User does not exist'})
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    def update(self, request,  *args, **kwargs):
        queryset = Cart.objects.all()
        try:
            cart = queryset.get(id=kwargs['pk'])
            id = request.data['item']
            item = Item.objects.get(id=id)
            cart.items.add(item)
            cart.save()
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'Error': 'Cart Does not exist'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)


class ArchitectViewSet(viewsets.ModelViewSet):
    queryset = Architect.objects.all()
    serializer_class = ArchitectSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # def create(self, request):
    #     cart_id = request.data['cart_id']
    #     user_id = request.data['user_id']
    #     address = request.data['address']
    #     ship_days = request.data['ship_days']
    #     method = request.data['payment_method']
    #     today = datetime.now()
    #     ship_date = datetime(today.year, today.month,
    #                          (today.day + int(ship_days)), 0, 0, 0, 0)
    #     try:
    #         cart = Cart.objects.get(id=cart_id)
    #         order = Order.objects.create(
    #             user_id=User.objects.get(id=user_id), address=address, ship_date=ship_date)
    #         order.save()
    #         order.items.set(cart.items.all())
    #         cost = 0
    #         for i in cart.items.all():
    #             cost += i.price

    #         payment = OrderPayment.objects.create(
    #             order_id=order, amount=cost, status=False, method=method)
    #         payment.save()

    #         return Response(OrderPaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
    #     except (Cart.DoesNotExist, User.DoesNotExist):
    #         return Response({'Error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    # def retrieve(self, request,  *args, **kwargs):
    #     queryset = Order.objects.all()
    #     try:
    #         queryset.objects.all().select_related('')
    #         orders = queryset.filter(user_id=kwargs['pk'])
    #         return Response(OrderSerializer(orders, many=True).data, status=status.HTTP_200_OK)
    #     except Order.DoesNotExist:
    #         return Response({'Error': 'Order does not exist'})


class OrderPaymentViewSet(viewsets.ModelViewSet):
    queryset = OrderPayment.objects.all()
    serializer_class = OrderPaymentSerializer

    def retrieve(self, request,  *args, **kwargs):
        try:

            payments = OrderPayment.objects.filter(
                order_id__user_id=kwargs['pk'])
            return Response(OrderPaymentSerializer(payments, many=True).data, status=status.HTTP_200_OK)
        except OrderPayment.DoesNotExist:
            return Response({'Error': 'Order payment does not exist'})


class DesignPaymentViewSet(viewsets.ModelViewSet):
    queryset = DesignPayment.objects.all()
    serializer_class = DesignPaymentSerializer

    def retrieve(self, request,  *args, **kwargs):
        try:

            payments = DesignPayment.objects.filter(
                design_id__user_id=kwargs['pk'])
            return Response(DesignPaymentSerializer(payments, many=True).data, status=status.HTTP_200_OK)
        except DesignPayment.DoesNotExist:
            return Response({'Error': 'Design payment does not exist'})


class MeetingPaymentViewSet(viewsets.ModelViewSet):
    queryset = MeetingPayment.objects.all()
    serializer_class = MeetingPaymentSerializer

    def retrieve(self, request,  *args, **kwargs):
        try:

            payments = MeetingPayment.objects.filter(
                meeting_id__user_id=kwargs['pk'])
            return Response(MeetingPayment(payments, many=True).data, status=status.HTTP_200_OK)
        except MeetingPayment.DoesNotExist:
            return Response({'Error': 'Meeting payment does not exist'})


class DesignViewSet(viewsets.ModelViewSet):
    queryset = Design.objects.all()
    serializer_class = DesignSerializer

    def retrieve(self, request,  *args, **kwargs):
        queryset = Design.objects.all()
        try:
            designs = queryset.get(client_id=kwargs['pk'])
            return Response(DesignSerializer(designs, many=True).data, status=status.HTTP_200_OK)
        except Design.DoesNotExist:
            return Response({'Error': 'Design does not exist'})


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def retrieve(self, request,  *args, **kwargs):
        queryset = Project.objects.all()
        try:
            projects = queryset.filter(client_id=kwargs['pk'])
            return Response(ProjectSerializer(projects, many=True).data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'Error': 'Project does not exist'})


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def retrieve(self, request,  *args, **kwargs):
        queryset = Meeting.objects.all()
        try:
            meetings = queryset.get(client_id=kwargs['pk'])
            return Response(MeetingSerializer(meetings, many=True).data, status=status.HTTP_200_OK)
        except Meeting.DoesNotExist:
            return Response({'Error': 'Meeting does not exist'})

# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = (TokenAuthentication,)


#     @action(detail=False, methods=['post'])
#     def get_info(self, request, token=None):
#         user = Token.objects.get(key=token).user
#         serializer = UserSerializer(user)
#         if serializer.is_valid():
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,
#                             status=status.HTTP_400_BAD_REQUEST)


# class CheckoutApi(viewsets.ViewSet):
#     def create(self, request):
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ArticleViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
#                      mixins.CreateModelMixin, mixins.RetrieveModelMixin,
#                      mixins.UpdateModelMixin, mixins.DestroyModelMixin):

#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer


# class ArticleViewSet(viewsets.ViewSet):

#     def list(self, request):
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         queryset = Article.objects.all()
#         article = get_object_or_404(queryset, pk=pk)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)


#     def update(self, request, pk):
#         article = Article.objects.get(pk=pk)

#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#     def destroy(self, request, pk):
#         article = Article.objects.get(pk=pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ArticleList(generics.GenericAPIView, mixins.ListModelMixin,
#                   mixins.CreateModelMixin):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ArticleDetails(generics.GenericAPIView, mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin):


#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer

#     lookup_field = 'id'

#     def get(self, request, id):
#         return self.retrieve(request, id=id)

#     def put(self, request, id):
#         return self.update(request, id=id)

#     def delete(self, request, id):
#         return self.destroy(request, id=id)


# class ArticleList(APIView):

#     def get(self, request):
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)


#     def post(self, request):
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ArticleDetails(APIView):

#     def get_object(self, id):
#         try:
#            return Article.objects.get(id = id)
#         except Article.DoesNotExist:
#             return HttpResponse(status=status.HTTP_404_NOT_FOUND)


#     def get(self, request, id):
#         article = self.get_object(id)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)


#     def put(self, request, id):
#         article = self.get_object(id)
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#     def delete(self, request, id):
#         article = self.get_object(id)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def article_list(request):

#     #get all articles
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)


#     elif request.method == 'POST':
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def article_details(request, pk):
#     try:
#         article = Article.objects.get(pk=pk)
#     except Article.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#
