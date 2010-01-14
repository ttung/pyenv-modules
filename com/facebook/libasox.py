import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        # conflict checking
        for module_name in env.loaded_modules:
            if (module_name.startswith('com.facebook.libasox')):
                raise pyenv.ModulePreloadError("Cannot load two libasox modules at the same time")

        return ["oss.libevent-1.3c"]


    def load(self, env, shell):
        import os
        home = os.path.expanduser("~")
        machtype = os.getenv("MACHTYPE")
        ostype = os.getenv("OSTYPE")

        if (machtype is None or
            ostype is None):
            raise pyenv.ModuleLoadError("Cannot determine machine type or os type")

        libasox_pi_base = os.path.join(home, "software", "libasox") # platform-independent
        libasox_pd_base = os.path.join(home, "software", "%s-%s" % (machtype, ostype),
                                       "libasox") # platform-dependent

	shell.append_compiler_flag(os.path.join(libasox_pi_base, "include"),
                                   "CPPFLAGS",
                                   prefix = "-I",
                                   path_checking = pyenv.ShellConstants.ENFORCE_PATH)
        shell.append_path(os.path.join(libasox_pi_base, "lib"), "PYTHON_EXTRA_PATH")

        shell.append_path(os.path.join(libasox_pd_base, "lib"), "LD_LIBRARY_PATH")
	shell.append_compiler_flag(os.path.join(libasox_pd_base, "lib"),
                                   "LDFLAGS",
                                   prefix = "-L",
                                   path_checking = pyenv.ShellConstants.ENFORCE_PATH)


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)
