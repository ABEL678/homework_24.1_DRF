from rest_framework import serializers
from main.models import Course, Lesson, Payment
from rest_framework.relations import SlugRelatedField

from users.models import User


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lesson_set.count', read_only=True)
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='course_name', queryset=Course.objects.all())
    lesson = SlugRelatedField(slug_field='lesson_name', queryset=Lesson.objects.all())
    user = SlugRelatedField(slug_field='first_name', queryset=User.objects.all())
    owner = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentForOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_date', 'payment_method']