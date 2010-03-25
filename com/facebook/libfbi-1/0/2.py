import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        # conflict checking
        for module_name in env.loaded_modules:
            if (module_name.startswith('com.facebook.libfbi')):
                raise pyenv.ModulePreloadError("Cannot load two libfbi modules at the same time")

        return []


    def load(self, env, shell):
        import os
        home = os.path.expanduser("~")
        machtype = os.getenv("MACHTYPE")
        ostype = os.getenv("OSTYPE")

        if (machtype is None or
            ostype is None):
            raise pyenv.ModuleLoadError("Cannot determine machine type or os type")

        libfbi_pi_base = os.path.join(home, "software", "libfbi-1.0.2") # platform-independent
        libfbi_pd_base = os.path.join(home, "software", "%s-%s" % (machtype, ostype),
                                     "libfbi-1.0.2") # platform-dependent

	shell.append_compiler_flag(os.path.join(libfbi_pi_base, "include"),
                                   "CPPFLAGS",
                                   prefix = "-I",
                                   path_checking = pyenv.ShellConstants.ENFORCE_PATH)
        shell.append_path(os.path.join(libfbi_pi_base, "lib"), "PYTHON_EXTRA_PATH")
        shell.append_path(os.path.join(libfbi_pi_base, "share", "aclocal"), "ACLOCAL_PATH")

        shell.append_path(os.path.join(libfbi_pd_base, "lib"), "LD_LIBRARY_PATH")
        shell.append_compiler_flag(os.path.join(libfbi_pd_base, "lib"),
                                   "LDFLAGS",
                                   prefix = "-L",
                                   path_checking = pyenv.ShellConstants.ENFORCE_PATH)

        # aclocal is weird.  even on a remove, we may need to forcibly set it.
        if ("ACLOCAL_PATH" in shell.paths and
            len(shell.paths['ACLOCAL_PATH']) != 0):
            shell.environment_variables['ACLOCAL'] = ("aclocal %s" %
                                                      (" ".join(["-I %s" % path
                                                                 for path in shell.paths['ACLOCAL_PATH']])))
        else:
            # this will remove it.
            shell.add_env("ACLOCAL", None)


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)
