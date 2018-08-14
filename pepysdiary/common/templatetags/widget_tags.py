# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.urls import reverse
from django.utils.html import mark_safe

from pepysdiary.encyclopedia.models import Topic
from pepysdiary.encyclopedia import topic_lookups
from pepysdiary.indepth.models import Article
from pepysdiary.news.models import Post

register = template.Library()

# Things that appear in the sidebar or footer on several pages.


def put_in_block(body, title=''):
    """
    All sidebar content should be wrapped in this.
    `body` should be an HTML/text string.
    `title` is an optional title HTML/text string.
    """
    header = ''
    if title:
        header = '<header class="aside-header"><h1 class="aside-title">%s</h1></header>' % title

    return """<aside class="aside-block">
%s
    <div class="aside-body">
%s
    </div>
</aside>
""" % (header, body)


@register.simple_tag
def twitter_and_email(*args):
    return mark_safe(put_in_block("""
<p><a href="http://feedburner.google.com/fb/a/mailverify?uri=PepysDiary&amp;loc=en_US">Receive diary entries by email daily</a></p>
<p>Follow in real time <a href="http://twitter.com/samuelpepys" title="@samuelpepys">on&nbsp;Twitter</a> or <a href="https://mastodon.social/@samuelpepys" title="@samuelpepys@mastodon.social">on&nbsp;Mastodon</a></p>
""", 'Email, Twitter &amp;&nbsp;Mastodon'))


@register.simple_tag
def credit(*args):
    return mark_safe(put_in_block("""<p>This site is run by <a href="http://www.gyford.com/">Phil&nbsp;Gyford</a></p>
<p><a href="https://twitter.com/philgyford">@philgyford</a> on Twitter</p>
<p><a href="%s">More about this site</a></p>
""" % (reverse('about')), 'About'))


@register.simple_tag
def rss_feeds(*args):
    """
    Display a list of links to RSS feeds. Use something like:
        {% rss_feeds 'entries' 'posts' 'topics' %}
    Where the arguments are valid feed kinds from `rss_feed_link()`.
    Or do this, to display links to all possible feeds:
        {% rss_feeds %}
    """
    feeds = (
        ('entries', {
            'url': 'http://feeds.feedburner.com/PepysDiary',
            'things': 'Diary entries',
        }),
        ('topics', {
            'url': 'http://feeds.feedburner.com/PepysDiary-Encyclopedia',
            'things': 'Encyclopedia topics',
        }),
        ('articles', {
            'url': 'http://feeds.feedburner.com/PepysDiary-InDepthArticles',
            'things': 'In-Depth articles',
        }),
        ('posts', {
            'url': 'http://feeds.feedburner.com/PepysDiary-SiteNews',
            'things': 'Site News posts',
        }),
        # Not on Feedburner yet:
        # ('letters', {
        #     'url': 'http://feeds.feedburner.com/PepysDiary-SiteNews',
        #     'things': 'Site News posts',
        # }),
    )
    html = ''
    kinds = []
    # What feeds are we linking to?
    if len(args) == 0:
        kinds = [k for k, v in feeds]
    else:
        kinds = args

    feeds_dict = dict(feeds)
    for kind in kinds:
        if kind in feeds_dict:
            html += '<li class="feed"><a href="%s">%s</a></li>' % (
                        feeds_dict[kind]['url'], feeds_dict[kind]['things'])
    if html != '':
        html = put_in_block("""<ul class="feeds">
%s
</ul>
""" % html, 'RSS feeds')
    return mark_safe(html)


def recent_list(queryset, title, date_format):
    """
    Generates a <dl> containing titles of posts, entries, articles, etc,
    linking to each one, with the date in its <dd>.

    queryset is the queryset of things to show.
    title is the text to use for the block's title.
    date_format is a date format suitable for strftime()
    """
    html = ''
    if queryset:
        for item in queryset:
            if hasattr(item, 'date_published'):
                # Posts and Articles.
                item_date = item.date_published
            else:
                item_date = item.date_created

            html += """<dt><a href="%s">%s</a></dt>
<dd class="text-muted">%s</dd>
""" % (item.get_absolute_url(),
        item.title,
        item_date.strftime(date_format))

        html = """<dl class="dated">
%s
</dl>
""" % (html)
    return put_in_block(html, title)


@register.simple_tag(takes_context=True)
def latest_posts(context, quantity=5):
    """Displays links to the most recent Site News Posts."""
    post_list = Post.published_posts.all().only('title', 'date_published')[:quantity]
    return mark_safe(recent_list(post_list, 'Latest Site News',
                                        context['date_format_long_strftime']))


@register.simple_tag(takes_context=True)
def latest_articles(context, quantity=5):
    """Displays links to the most recent In-Depth Articles."""
    article_list = Article.published_articles.all().only('title', 'date_published', 'slug')[:quantity]
    return mark_safe(recent_list(article_list, 'Latest In-Depth Articles',
                                        context['date_format_long_strftime']))


@register.simple_tag(takes_context=True)
def latest_topics(context, quantity=5):
    """Displays links to the most recent Encyclopedia Topics"""
    topic_list = Topic.objects.order_by('-date_created').only('title', 'date_created')[:quantity]
    return mark_safe(recent_list(topic_list, 'Latest Encyclopedia Topics',
                                        context['date_format_long_strftime']))


@register.simple_tag(takes_context=True)
def all_articles(context, exclude_id=None):
    """
    Displays links to all the In-Depth Articles.
    If `exclude_id` is set, then we include that Article, but don't link to it.
    """
    article_list = Article.published_articles.all().only(
                                            'title', 'date_published', 'slug')
    date_format = context['date_format_long_strftime']
    html = ''
    for item in article_list:
        if (item.id == exclude_id):
            html += """<li>%s<br>%s</li>""" % (
                                    item.title,
                                    item.date_published.strftime(date_format))
        else:
            html += """<li><a href="%s">%s</a><br>%s</li>""" % (
                                    item.get_absolute_url(),
                                    item.title,
                                    item.date_published.strftime(date_format))
    return mark_safe(put_in_block("""<ul class="list-spaced list-small list-unstyled">%s</ul>""" % (html), 'All In-Depth Articles'))



@register.simple_tag
def summary_year_navigation(current_year):
    """
    The list of years for the Diary Summary sidebar navigation.
    current_year will either be 'year' or a date object.
    """
    css_class = ''
    if current_year == 'before':
        css_class = 'active'
    else:
        current_year = current_year.year
    html = '<a class="list-group-item %s" href="%s">Before the diary</a>' % (
                                                    css_class,
                                                    reverse('diary_summary'))
    for y in [1660, 1661, 1662, 1663, 1664, 1665, 1666, 1667, 1668, 1669,]:
        css_class = ''
        if y == current_year:
            css_class = 'active'
        html += '<a class="list-group-item %s" href="%s">%s</a>' % (
                        css_class,
                        reverse('summary_year_archive', kwargs={'year': y}),
                        y)
    html += '<a class="list-group-item" href="%s">After the diary (In-Depth Article)</a>' % (
                        reverse('article_detail', kwargs={
                            'year': '2012', 'month': '05', 'day': '31',
                            'slug': 'the-next-chapter'}
                        ))
    return mark_safe('<div class="list-group">%s</div>' % html)


@register.simple_tag
def family_tree_link(topic=None):
    """
    Displays a thumbnail of the family tree and a link to it.
    If `topic` is present, and the topic is featured on the family tree, then
    the text is different.
    """
    text = "See the Pepys family tree"
    if topic is not None and topic.on_pepys_family_tree:
        text = "See this person on the Pepys family&nbsp;tree"
    link_url = reverse('encyclopedia_familytree')

    body = """
        <p><a href="%s"><img class="img-responsive" src="%scommon/img/sidebar_family_tree.png" width="330" height="110" alt="Family tree thumbnail" /></p>
        <p><a href="%s">%s</a></p>
    """ % (link_url, settings.STATIC_URL, link_url, text)

    return mark_safe(put_in_block(body, 'Family tree'))


@register.simple_tag
def pepys_wealth_link():
    """
    Displays a thumbnail of the Pepys' Wealth chart and a link to it.
    If `topic` is present, and the topic is featured on the family treet, then
    the text is different.
    """
    text = "See his wealth during the diary"
    link_url = reverse('topic_detail', kwargs={'pk': topic_lookups.PEPYS_WEALTH})

    body = """
        <p><a href="%s"><img class="img-responsive" src="%scommon/img/sidebar_wealth_chart.png" width="330" height="110" alt="Wealth chart thumbnail" /></p>
        <p><a href="%s">%s</a></p>
    """ % (link_url, settings.STATIC_URL, link_url, text)

    return mark_safe(put_in_block(body, 'Samuel Pepys&#8217; wealth'))


@register.simple_tag
def category_map_link(category_id=None):
    """
    Displays a thumbnail of the category map and a link to it.
    If `category_id` is present, we link to that category's map.
    """
    if category_id is None:
        link_url = reverse('category_map')
        text = "See places from the Diary on a&nbsp;map"
    else:
        link_url = reverse('category_map', kwargs={'category_id': category_id})
        text = "See all places in this category on one&nbsp;map"

    body = """<p class="clearfix">
    <a href="%s"><img class="pull-right" src="%scommon/img/sidebar_category_map.png" width="110" height="62" alt="Map thumbnail" /></a>
    <a href="%s">%s</a>
    </p>
    """ % (link_url, settings.STATIC_URL, link_url, text)

    return mark_safe(put_in_block(body, 'Maps'))


@register.simple_tag
def admin_link_change(url):
    return mark_safe("""<p class="admin-links"><a class="admin" href="%s">Edit</a></p>""" % (url))


@register.simple_tag
def detailed_topics():
    topics = (
        (150,  "Elizabeth Pepys"),
        (112,  "Sir Edward Mountagu (Pepys’ patron)"),
        (2381, "Catherine of Braganza (Queen)"),
        (5036, "Frances Stuart (Duchess of Richmond)"),
        (1062, "Barbara Palmer (Countess of Castlemaine)"),
        (370,  "17th Century Mathematics"),
        (5344, "John Wilmot (2nd Earl of Rochester)"),
        (804,  "Sir Edward Hyde (Earl of Clarendon)"),
        (1686, "Sir Charles Berkeley"),
        (1018, "Sir George Carteret"),
    )

    body = '<ul>'
    for topic in topics:
        body += '<li><a href="%s">%s</a></li>' % (reverse('topic_detail', kwargs={'pk': topic[0]}), topic[1])
    body += '</ul><p>Written by readers of this site</p>'
    return mark_safe(put_in_block(body, 'Detailed topics'))
