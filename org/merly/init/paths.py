import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        return []


    def load(self, env, shell):
        import os
        import platform

        home = os.path.expanduser("~")
        machtype = platform.machine()
        ostype = platform.system()

        if (machtype == "" or
            ostype == ""):
            raise pyenv.ModuleLoadError("Cannot determine machine type or os type")

        compat_machtype = [machtype]
        compat_ostype = [ostype]

        # extend compatibility.
        if (machtype == "x86_64"):
            compat_machtype.append("i386") # x86-64 can run i386 binaries.
        if (ostype == "FreeBSD"):
            compat_ostype.append("Linux") # freebsd has the linux compatibility layer.
        if (ostype == "Darwin" and machtype == "i386"):
            compat_machtype.append("powerpc") # macosx has rosetta, allowing it to run ppc binaries.

        # reset the paths
        shell.reset_path("PATH")
        shell.reset_path("MANPATH")
        shell.reset_path("INFOPATH")
        shell.reset_path("LD_LIBRARY_PATH")
        shell.reset_path("PYTHONPATH")
        shell.reset_path("INCLUDE_PATH")
        shell.reset_path("LIB_PATH")

        prefixes = [{'path': os.path.join(home, "software"),
                     'development_paths': True}]
        for mt in compat_machtype:
            for ost in compat_ostype:
                prefixes.append({'path': os.path.join(home, "software",
                                                      "%s-%s" % (mt, ost)),
                                 'development_paths': True})

        prefixes.extend([
                {'path': os.path.join(os.sep, "usr", "local"), 'sbin_paths': True},
                {'path': os.path.join(os.sep, "opt", "local"), 'sbin_paths': True},
                {'path': os.path.join(os.sep, "usr"), 'sbin_paths': True},
                {'path': os.path.join(os.sep, "opt"), 'sbin_paths': True},
                {'path': os.path.join(os.sep), 'sbin_paths': True},
                {'path': os.path.join(os.sep, "usr", "X11R6"), 'sbin_paths': True},
                ])

        for prefix_data in prefixes:
            prefix = prefix_data.get('path')
            do_development_paths = prefix_data.get('development_paths', False)
            do_sbin_paths = prefix_data.get('sbin_paths', False)

            # path
            shell.append_path(os.path.join(prefix, "bin"), "PATH", pyenv.ShellConstants.VALIDATE_PATH)
            if (do_sbin_paths):
                shell.append_path(os.path.join(prefix, "sbin"), "PATH", pyenv.ShellConstants.VALIDATE_PATH)

            # ld_library_path
            shell.append_path(os.path.join(prefix, "lib"), "LD_LIBRARY_PATH", pyenv.ShellConstants.VALIDATE_PATH)
            if machtype == "x86_64":
                shell.append_path(os.path.join(prefix, "lib64"), "LD_LIBRARY_PATH",
                                  pyenv.ShellConstants.VALIDATE_PATH)

            # manpath
            shell.append_path(os.path.join(prefix, "man"), "MANPATH", pyenv.ShellConstants.VALIDATE_PATH)
            shell.append_path(os.path.join(prefix, "share", "man"), "MANPATH", pyenv.ShellConstants.VALIDATE_PATH)

            # infopath
            shell.append_path(os.path.join(prefix, "info"), "INFOPATH", pyenv.ShellConstants.VALIDATE_PATH)
            shell.append_path(os.path.join(prefix, "share", "info"), "INFOPATH", pyenv.ShellConstants.VALIDATE_PATH)

            if do_development_paths:
                # development paths
                shell.append_path(os.path.join(prefix, "include"), "INCLUDE_PATH", pyenv.ShellConstants.VALIDATE_PATH)
                shell.append_path(os.path.join(prefix, "lib"), "LIB_PATH", pyenv.ShellConstants.VALIDATE_PATH)
                if machtype == "x86_64":
                    shell.append_path(os.path.join(prefix, "lib64"), "LIB_PATH",
                                      pyenv.ShellConstants.VALIDATE_PATH)
                shell.append_path(os.path.join(prefix, "python"), "PYTHONPATH", pyenv.ShellConstants.VALIDATE_PATH)


    def unload(self, env, shell):
        shell.write("Unloaded, but paths not reset.")
