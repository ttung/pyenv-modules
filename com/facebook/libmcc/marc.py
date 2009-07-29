import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        # conflict checking
        for module_name in env.loaded_modules:
            if (module_name.startswith('com.facebook.libmcc')):
                raise pyenv.ModulePreloadError("Cannot load two libmcc modules at the same time")

        return ["com.facebook.libfbi", "com.facebook.libasox", "com.facebook.libmc"]


    def load(self, env, shell):
        import os
        home = os.path.expanduser("~")
        machtype = os.getenv("MACHTYPE")
        ostype = os.getenv("OSTYPE")

        if (machtype is None or
            ostype is None):
            raise pyenv.ModuleLoadError("Cannot determine machine type or os type")

        libmc_pi_base = os.path.join(home, "software", "libmcc") # platform-independent
        libmc_pd_base = os.path.join(home, "software", "%s-%s" % (machtype, ostype),
                                     "libmcc") # platform-dependent

        # python extra paths are expanded in ~/software/python/sitecustomize.py
        shell.append_path(os.path.join(libmc_pi_base, "lib"), "PYTHON_EXTRA_PATHS",
                          check_path = shell.ENFORCE_PATH)
        shell.append_path(os.path.join(libmc_pd_base, "lib"), "LD_LIBRARY_PATH",
                          check_path = shell.ENFORCE_PATH)


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)
