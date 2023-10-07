from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from main.models import Course, Lesson, Payment
from main.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from main.permissions import IsModeratorOrReadOnly, IsCourseOrLessonOwner, IsPaymentOwner, IsCourseOwner
from users.models import UserRoles


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOwner]

    def get_queryset(self):
        if self.request.user.role == UserRoles.MODERATOR:
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вы не можете создавать курсы")
        else:
            new_payment = serializer.save()
            new_payment.owner = self.request.user
            new_payment.save()

    def perform_delete(self, instance):
        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вы не можете удалять курсы")
        instance.delete()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def perform_create(self, serializer):
        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вы не можете создать урок")
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def get_queryset(self):
        if self.request.user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def get_queryset(self):
        if self.request.user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def get_queryset(self):
        if self.request.user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def get_queryset(self):
        if self.request.user.role == UserRoles.MODERATOR:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)

    def perform_destroy(self, instance):
        if self.request.user.role == UserRoles.MODERATOR:
            raise PermissionDenied("Вы не можете удалять уроки")
        instance.delete()


class PaymentListAPIView(generics.ListAPIView):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsPaymentOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('course', 'lesson', 'owner', 'method',)
    ordering_fields = ('payment_date',)

    def get_queryset(self):
        if self.request.user.role == UserRoles.MODERATOR:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(owner=self.request.user)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsPaymentOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'owner', 'payment_method',)
    ordering_fields = ('payment_date',)

    def get_queryset(self):
        if self.request.user.role == UserRoles.MODERATOR:
            return Payment.objects.all()
        else:
            return Payment.objects.filter(owner=self.request.user)
