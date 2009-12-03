import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        import re

        cre = re.compile(r"com\.facebook\.libmc(\.|$)")

        # conflict checking
        for module_name in env.loaded_modules:
            if (cre.match(module_name)):
                raise pyenv.ModulePreloadError("Cannot load two libmc modules at the same time")

        return ["com.facebook.libfbi"]


    def load(self, env, shell):
        import os
        home = os.path.expanduser("~")
        machtype = os.getenv("MACHTYPE")
        ostype = os.getenv("OSTYPE")

        if (machtype is None or
            ostype is None):
            raise pyenv.ModuleLoadError("Cannot determine machine type or os type")

        libmc_pi_base = os.path.join(home, "software", "libmc") # platform-independent
        libmc_pd_base = os.path.join(home, "software", "%s-%s" % (machtype, ostype),
                                     "libmc") # platform-dependent

	shell.append_compiler_flag(os.path.join(libmc_pi_base, "include"),
                                   "CPPFLAGS",
                                   prefix = "-I",
                                   path_checking = pyenv.ShellConstants.ENFORCE_PATH)
        shell.append_path(os.path.join(libmc_pi_base, "lib"), "PYTHON_EXTRA_PATH")

        shell.append_path(os.path.join(libmc_pd_base, "lib"), "LD_LIBRARY_PATH")
	shell.append_compiler_flag(os.path.join(libmc_pd_base, "lib"),
                                   "LDFLAGS",
                                   prefix = "-L",
                                   path_checking = pyenv.ShellConstants.ENFORCE_PATH)


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)
