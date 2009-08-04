import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
	# conflict checking
        for module_name in env.loaded_modules:
            if (module_name.startswith("oss.libevent")):
                raise pyenv.ModulePreloadError("Cannot load two libevent modules at the same time")

        return []


    def load(self, env, shell):
        # quick and dirty search for libevent, if present, then we don't need to do anything.
        try:
            import ctypes.util

            lib = ctypes.util.find_library('event')
            if (lib is None):
                raise Exception("cannot find libevent")
        except:
            pass
        else:
            return

        import os
        home = os.path.expanduser("~")
        machtype = os.getenv("MACHTYPE")
        ostype = os.getenv("OSTYPE")

        if (machtype is None or
            ostype is None):
            raise pyenv.ModuleLoadError("Cannot determine machine type or os type")

        libevent_pi_base = os.path.join(home, "software", "libevent-1.3c") # platform-independent
        libevent_pd_base = os.path.join(home, "software", "%s-%s" % (machtype, ostype),
                                        "libevent-1.3c") # platform-dependent

	shell.append_compiler_flag(os.path.join(libevent_pi_base, "include"),
                                   "CPPFLAGS",
                                   prefix = "-I",
                                   path_checking = pyenv.ShellConstants.ENFORCE_PATH)
	shell.append_path(os.path.join(libevent_pi_base, "share", "man"), "MANPATH")

	shell.append_path(os.path.join(libevent_pd_base, "lib"), "LD_LIBRARY_PATH")
	shell.append_compiler_flag(os.path.join(libevent_pd_base, "lib"),
                                   "LDFLAGS",
                                   prefix = "-L",
                                   path_checking = pyenv.ShellConstants.ENFORCE_PATH)


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)

