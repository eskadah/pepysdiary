from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

from ..common.utilities import make_url_absolute
from ..diary.models import Entry
from ..encyclopedia.models import Category, Topic


class BaseSerializer(serializers.ModelSerializer):
    """
    Parent class that includes a `web_url` field for the object's
    get_absolute_url() method.
    """

    web_url = serializers.SerializerMethodField()

    def get_web_url(self, obj):
        return make_url_absolute(obj.get_absolute_url())


class CategorySerializer(BaseSerializer):

    api_url = serializers.HyperlinkedIdentityField(
        view_name='api:category_detail',
        lookup_field='slug',
        lookup_url_kwarg='category_slug'
    )

    children = serializers.SerializerMethodField()
    parents = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('slug',
                    'title', 'topic_count',
                    'parents', 'children',
                    'api_url', 'web_url',
                )

    def get_children(self, obj):
        children = []
        for child in obj.get_children():
            children.append( _make_category_url(child) )
        return children

    def get_parents(self, obj):
        parents = []
        for ancestor in obj.get_ancestors():
            parents.append( _make_category_url(ancestor) )
        return parents



class EntrySerializer(BaseSerializer):

    api_url = serializers.HyperlinkedIdentityField(
        view_name='api:entry_detail',
        lookup_field='diary_date',
        lookup_url_kwarg='entry_date'
    )

    # Rename model fields to more publicly-useful names:
    date = serializers.DateField(source='diary_date', read_only=True)
    entry_html = serializers.CharField(source='text', read_only=True)
    footnotes_html = serializers.CharField(source='footnotes', read_only=True)
    annotation_count = serializers.IntegerField(source='comment_count', read_only=True)
    last_annotation_time = serializers.DateTimeField(source='last_comment_time', read_only=True)

    class Meta:
        model = Entry
        fields = ('date',
                    'title', 'entry_html', 'footnotes_html',
                    'annotation_count', 'last_annotation_time',
                    'api_url', 'web_url',
                )


class TopicSerializer(BaseSerializer):

    api_url = serializers.HyperlinkedIdentityField(
        view_name='api:topic_detail',
        lookup_field='id',
        lookup_url_kwarg='topic_id'
    )

    # Rename model fields to more publicly-useful names:
    annotation_count = serializers.IntegerField(source='comment_count', read_only=True)
    last_annotation_time = serializers.DateTimeField(source='last_comment_time', read_only=True)
    thumbnail_url = serializers.ImageField(source='thumbnail', read_only=True)
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ('id',
                    'title', 'order_title',
                    # 'summary',
                    'wheatley_html', 'tooltip_text',
                    'wikipedia_url', 'thumbnail_url',
                    'annotation_count', 'last_annotation_time',
                    'is_person', 'is_place',
                    'latitude', 'longitude', 'zoom', 'shape',
                    'categories',
                    'api_url', 'web_url',
                )

    def get_categories(self, obj):
        cats = []
        for cat in obj.categories.all():
            cats.append( _make_category_url(cat) )
        return cats


def _make_category_url(category):
    "Shortcut for making the API URL for a Category."
    return make_url_absolute(
        reverse_lazy('api:category_detail', kwargs={'category_slug': category.slug})
    )
