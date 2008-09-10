import os
import StringIO
import subprocess
import sys

from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.utils.cache import patch_response_headers

try:
    import gprof2dot
except ImportError:
    gprof2dot = None
from decorators import supress_logging_output
from middleware import profiler, profiling_enabled, profiler_name


def _get_filename(request, request_id):
    try:
        recent_profiles = request.session['djangologging.recent_profiles']
        return recent_profiles[request_id]    
    except KeyError:
        raise Http404

def _get_path():
    return os.environ.get('PATH', '').split(os.pathsep)

def _find_dot():
    filename = 'dot'
    if sys.platform == 'win32':
        filename = '%s.exe' % filename

    for path in _get_path():
        filepath = os.path.join(path, filename)
        if os.path.exists(filepath) and os.access(filepath, os.F_OK | os.X_OK):
            return filepath
    
    return False


@supress_logging_output
def profile(request, request_id):
    filename = _get_filename(request, request_id)
    stats = profiler.load(filename)
    stats.sort_stats("time", "name")
    stats.stream = StringIO.StringIO()
    stats.print_stats()
    context = {
        'dot': _find_dot(),
        'gprof2dot': gprof2dot and gprof2dot.__file__,
        'graph_url': reverse(profile_graph, kwargs={'request_id': request_id}),
        'stats': stats.stream.getvalue(),
        }
    return render_to_response('profile.html', context)


@supress_logging_output
def profile_graph(request, request_id):
    # Check the request_id is valid
    _get_filename(request, request_id)
    context = {
        'dot': _find_dot(),
        'gprof2dot': gprof2dot and gprof2dot.__file__,
        'path': _get_path(),
        'pythonpath': sys.path,
        'statistics_url': reverse(profile, kwargs={'request_id': request_id}),
        'image_url': reverse(graph_image, kwargs={'request_id': request_id}),
        'profiler_name': profiler_name,
        }
    return render_to_response('profile_graph.html', context)


@supress_logging_output
def graph_image(request, request_id):

    filename = _get_filename(request, request_id)
    dot = subprocess.Popen(['dot', '-Tpng', '-Gbgcolor=#f6f6f6'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    parser = profiler.parser(filename)
    
    instance = gprof2dot.Main()
    instance.profile = parser.parse()
    instance.output = dot.stdin
    instance.colormap = instance.colormaps['color']
    class Options(object):
        node_thres = 0.5
        edge_thres = 0.1
        strip = False
        wrap = False
    instance.options = Options()
    instance.write_graph()

    dot.stdin.close()
    
    response = HttpResponse(dot.stdout.read(), 'image/png')
    patch_response_headers(response, cache_timeout=3600)
    return response
