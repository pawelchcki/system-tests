import os

from utils.tools import logger


class VmProviderFactory:
    """Use the correct provider specified by Id"""

    def get_provider(self, provider_id):
        logger.info(f"Using {provider_id} provider")
        if provider_id == "aws":
            from utils.virtual_machine.aws_provider import AWSPulumiProvider

            return AWSPulumiProvider()
        elif provider_id == "vagrant":
            from utils.virtual_machine.vagrant_provider import VagrantProvider

            return VagrantProvider()
        elif provider_id == "krunvm":
            from utils.virtual_machine.krunvm_provider import KrunVmProvider

            return KrunVmProvider()
        else:
            raise ValueError("Not supported provided", provider_id)


class VmProvider:
    """Provider responsible of manage the virtual machines
    Start up all the stack (group of virtual machines)"""

    def __init__(self):
        self.vms = None
        self.provision = None
        # Responsibility of the commander to execute commands on the VMs
        self.commander = None

    def configure(self, required_vms):
        self.vms = required_vms

    def stack_up(self):
        """Each provider should implement the method that start up all the machines.
        After each machine is up, you will call the install_provision method for each machine."""
        raise NotImplementedError

    def stack_destroy(self):
        """Stop and destroy machines"""
        raise NotImplementedError

    def install_provision(self, vm, server, server_connection, create_cache=True):
        """
        This method orchestrate the provision installation for a machine
        Vm object contains the provision for the machine.
        The provision structure must satisfy the class utils/virtual_machine/virtual_machine_provisioner.py#Provision
        This is a common method for all providers"""
        logger.stdout(f"Provisioning [{vm.name}]")
        provision = vm.get_provision()
        last_task = server
        if create_cache:
            # First install cacheable installations
            for installation in provision.installations:
                if installation.cache:
                    logger.stdout(f"[{vm.name}] Provisioning cacheable {installation.id}")
                    last_task = self._remote_install(server_connection, vm, last_task, installation)

            # Then install lang variant if needed (cacheable)
            if provision.lang_variant_installation:
                logger.stdout(f"[{vm.name}] Provisioning lang variant {provision.lang_variant_installation.id}")
                last_task = self._remote_install(server_connection, vm, last_task, provision.lang_variant_installation)
            last_task = self.commander.create_cache(vm, server, last_task)

        # Then install non cacheable installations
        for installation in provision.installations:
            if not installation.cache:
                logger.stdout(f"[{vm.name}] Provisioning no cacheable {installation.id}")
                last_task = self._remote_install(server_connection, vm, last_task, installation)

        # Extract tested/installed components
        logger.stdout(f"[{vm.name}] Extracting {provision.tested_components_installation.id}")

        output_callback = lambda args: args[0].set_tested_components(args[1])
        last_task = self._remote_install(
            server_connection,
            vm,
            last_task,
            provision.tested_components_installation,
            logger_name="tested_components",
            output_callback=output_callback,
        )

        # Finally install weblog
        logger.stdout(f"[{vm.name}] Installing {provision.weblog_installation.id}")
        last_task = self._remote_install(server_connection, vm, last_task, provision.weblog_installation)

    def _remote_install(self, server_connection, vm, last_task, installation, logger_name=None, output_callback=None):
        """Manages a installation.
        The installation must satisfy the class utils/virtual_machine/virtual_machine_provisioner.py#Installation"""
        local_command = None
        command_environment = vm.get_command_environment()
        # Execute local command if we need
        if installation.local_command:
            local_command = installation.local_command

        # Execute local script if we need
        if installation.local_script:
            local_command = "sh " + installation.local_script

        if local_command:
            last_task = self.commander.execute_local_command(
                f"local-script_{vm.name}_{installation.id}", local_command, command_environment, last_task, vm.name
            )

        # Copy files from local to remote if we need
        if installation.copy_files:
            for file_to_copy in installation.copy_files:

                # If we don't use remote_path, the remote_path will be a default remote user home
                if file_to_copy.remote_path:
                    remote_path = file_to_copy.remote_path
                else:
                    remote_path = os.path.basename(file_to_copy.local_path)

                if not os.path.isdir(file_to_copy.local_path):
                    # If the local path contains a variable, we need to replace it
                    for key, value in command_environment.items():
                        file_to_copy.local_path = file_to_copy.local_path.replace(f"${key}", value)
                        remote_path = remote_path.replace(f"${key}", value)

                    logger.debug(f"Copy file from {file_to_copy.local_path} to {remote_path}")
                    # Launch copy file command
                    last_task = self.commander.copy_file(
                        file_to_copy.name + f"-{vm.name}-{installation.id}",
                        file_to_copy.local_path,
                        remote_path,
                        server_connection,
                        last_task,
                        vm=vm,
                    )
                else:
                    last_task = self.commander.remote_copy_folders(
                        file_to_copy.local_path,
                        file_to_copy.remote_path,
                        f"-{vm.name}-{installation.id}",
                        server_connection,
                        last_task,
                        vm=vm,
                    )

        # Execute a basic command on our server.
        return self.commander.remote_command(
            vm,
            installation.id,
            installation.remote_command,
            command_environment,
            server_connection,
            last_task,
            logger_name=logger_name,
            output_callback=output_callback,
        )


class Commander:
    """Run commands on the VMs. Each provider should implement this class."""

    def create_cache(self, vm, server, last_task):
        """Create a cache from existing server.
        Use vm.get_cache_name() to get the cache name.
        Server is the started server to create the cache from.
        Use last_task to depend on the last executed task.
        Return the current task executed."""
        return last_task

    def execute_local_command(self, local_command_id, local_command, env, last_task, logger_name):
        """Execute a local command in the current machine.
        Env contain environment variables to be used in the command.
        logger_name is the name of the logger to use to store the output of the command.
        Use last_task to depend on the last executed task.
        Return the current task executed."""
        raise NotImplementedError

    def copy_file(self, id, local_path, remote_path, connection, last_task, vm=None):
        """Copy a file from local to remote.
        Use last_task to depend on the last executed task.
        Return the current task executed."""
        raise NotImplementedError

    def remote_command(self, id, remote_command, connection, last_task, logger_name, output_callback=None):
        """Execute a command in the remote server.
        Use last_task to depend on the last executed task.
        logger_name is the name of the logger to use to store the output of the command.
        output_callback is a function to be called with the output of the command.
        Return the current task executed."""
        raise NotImplementedError

    def remote_copy_folders(
        self, source_folder, destination_folder, command_id, connection, depends_on, relative_path=False, vm=None
    ):
        """The best option would be zip folder on local system and copy to remote machine
        There is a weird behaviour synchronizing local command and remote command
        Uggly workaround: Copy files and folder one by one :-( )"""

        raise NotImplementedError(f"Copy folders not implemented")
