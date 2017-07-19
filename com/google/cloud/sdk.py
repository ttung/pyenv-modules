import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        import re

        cre = re.compile(r"com\.google\.cloud.sdk(\.|$)")

        # conflict checking
        for module_name in env.loaded_modules:
            if (cre.match(module_name)):
                raise pyenv.ModulePreloadError("Cannot load two google cloud SDK modules at the same time")

        return []


    def load(self, env, shell):
        import os
        home = os.path.expanduser("~")

        google_cloud_sdk_base = os.path.join(home, "software", "google-cloud-sdk")

        shell.append_path(os.path.join(google_cloud_sdk_base, "bin"), "PATH")


    def unload(self, env, shell):
        pyenv.Module.unload_by_reversal(self, env, shell)
