from rest_framework import serializers
from main.models import Course, Lesson, Payment, Subscription
from rest_framework.relations import SlugRelatedField
from main.validators import LinksValidator

from users.models import User


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lesson_set.count', read_only=True)
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            LinksValidator(fields=['name', 'description']),
            serializers.UniqueTogetherValidator(fields=['name', 'description'], queryset=Course.objects.all())
        ]

        def get_lessons(self, course):
            return LessonListSerializer(Lesson.objects.filter(course=course), many=True).data

        def get_is_subscribed(self, obj):
            user = self.context['request'].user
            return Subscription.objects.filter(user=user, course=obj).exists()


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='name', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            LinksValidator(fields=['name', 'description', 'video_url']),
            serializers.UniqueTogetherValidator(fields=['name', 'description'], queryset=Lesson.objects.all())
        ]


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url']


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


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
