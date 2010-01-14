import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        import re

        cre = re.compile(r"com\.facebook\.mcproxy(\.|$)")

        # conflict checking
        for module_name in env.loaded_modules:
            if (cre.match(module_name)):
                raise pyenv.ModulePreloadError("Cannot load two mcproxy modules at the same time")

        return ["oss.libevent.1_3c"]


    def load(self, env, shell):
        import os
        home = os.path.expanduser("~")
        machtype = os.getenv("MACHTYPE")
        ostype = os.getenv("OSTYPE")

        if (machtype is None or
            ostype is None):
            raise pyenv.ModuleLoadError("Cannot determine machine type or os type")

        # no platform-independent files for mcproxy
        # mcproxy_pi_base = os.path.join(home, "software", "mcproxy") # platform-independent
        mcproxy_pd_base = os.path.join(home, "software", "%s-%s" % (machtype, ostype),
                                         "mcproxy-1.1") # platform-dependent

        # path needs to go in front since on FB machines, mcproxy is already in the path.
        shell.prepend_path(os.path.join(mcproxy_pd_base, "bin"), "PATH")


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)
