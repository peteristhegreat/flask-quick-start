import os

#from django.conf import settings
from flask import current_app as app
from jinja2 import nodes # it is here, don't believe pycharm
from jinja2.exceptions import TemplateSyntaxError
from jinja2.ext import Extension


class AssetExtension(Extension):
    '''Jinja2 extension to append modified timestamp for cachebreaking

    Add extension in flask:
        from path.to.jinja_asset import AssetExtension
        # ...
        app.jinja_env.add_extension('path.to.jinja_asset.AssetExtension')

    Usage: {% asset '/some/path.js' %}

    Returns: `/static/some/path.js?1320713645`'''

    tags = set(['asset'])

    def parse(self, parser):
        stream = parser.stream

        tag = next(stream)
        if stream.current.test('string'):
            path = parser.parse_primary()
        else:
            raise TemplateSyntaxError('''
"%s" requires path to asset file''' % tag.value, tag.lineno)
        while not parser.stream.current.type == 'block_end':
            next(parser.stream)
        result = self.call_method('_build_url', args=[path])
        return nodes.Output([nodes.MarkSafe(result)]).set_lineno(tag.lineno)

    def _build_url(self, path):
        file_path = '%s%s' % (app.static_folder, path)
        try:
            modified_timestamp = int(os.path.getmtime(file_path))
        except:
            modified_timestamp = ''
        href = '%s%s' % (app.static_url_path, path)
        if modified_timestamp:
            href += '?%s' % modified_timestamp
        return href

asset = AssetExtension