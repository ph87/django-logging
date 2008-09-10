import cProfile
import hotshot
import hotshot.stats
import pstats
try:
    from gprof2dot import PstatsParser, Profile
except ImportError:
    PstatsParser = object


class HotshotParser(PstatsParser):
    def __init__(self, filename):
        self.stats = hotshot.stats.load(filename)
        self.profile = Profile()
        self.function_ids = {}


class HotshotProfiler(object):
    def profile(self, outfile, func, *func_args, **func_kwargs):
        p = hotshot.Profile(outfile)
        p.runcall(func, *func_args, **func_kwargs)
        p.close()
    def load(self, filename):
        return hotshot.stats.load(filename)
    def parser(self, filename):
        return HotshotParser(filename)


class CProfileProfiler(object):
    def profile(self, outfile, func, *func_args, **func_kwargs):
        p = cProfile.Profile()
        p.runcall(func, *func_args, **func_kwargs)
        p.dump_stats(outfile)
    def load(self, filename):
        return pstats.Stats(filename)
    def parser(self, filename):
        return PstatsParser(filename)


# Supported profilers
profilers = {
    'hotshot': HotshotProfiler(),
    'cProfile': CProfileProfiler(),
    }