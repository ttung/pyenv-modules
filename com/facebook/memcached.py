import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        import re

        cre = re.compile(r"com\.facebook\.memcached(\.|$)")

        # conflict checking
        for module_name in env.loaded_modules:
            if (cre.match(module_name)):
                raise pyenv.ModulePreloadError("Cannot load two memcached modules at the same time")

        return ["oss.libevent.1_3c"]


    def load(self, env, shell):
        import os
        home = os.path.expanduser("~")
        machtype = os.getenv("MACHTYPE")
        ostype = os.getenv("OSTYPE")

        if (machtype is None or
            ostype is None):
            raise pyenv.ModuleLoadError("Cannot determine machine type or os type")

        memcached_pi_base = os.path.join(home, "software", "memcached") # platform-independent
        memcached_pd_base = os.path.join(home, "software", "%s-%s" % (machtype, ostype),
                                         "memcached") # platform-dependent

        shell.append_path(os.path.join(memcached_pi_base, "share", "man"), "MANPATH")

        shell.append_path(os.path.join(memcached_pd_base, "bin"), "PATH")


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)
