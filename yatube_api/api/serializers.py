from rest_framework.serializers import (
    CurrentUserDefault,
    ModelSerializer,
    SlugRelatedField,
    ValidationError
)
from rest_framework.validators import UniqueTogetherValidator


from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'group', 'image')
        model = Post


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created')
        read_only_fields = ('post',)


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    
    validators = (
        UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=('user', 'following',),
            message=('Эта подписка уже оформлена!')
        ),
    )

    def validate(self, data):
        if data['user'] == data['following']:
            raise ValidationError(
                'Подписка на самого себя запрещена!'
            )
        return data

    class Meta:
        fields = ('id', 'user', 'following')
        model = Follow
