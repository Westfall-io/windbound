# Copyright (c) 2023-2024 Westfall Inc.
#
# This file is part of Windbound.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, and can be found in the file NOTICE inside this
# git repository.
#
# This program is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Main entrypoint for the Windbound input builder.

This module coordinates the steps required to prepare an input artifact for
Windbound. It performs the following high-level actions:

- Create a MinIO client to access artifact storage.
- Authenticate to the Windstorm API to retrieve/update thread execution status.
- Check for and download outputs produced by dependent threads.
- Clone the template artifact repository for the current action.
- Render/build the template artifacts.
- Create and push an input archive to object storage.
- Initialize a local repository in the attached volume (used for attaching
    output/input artifacts to the runner environment).

The `main` function is exposed as a CLI via `fire.Fire` when run as a
script. The module expects environment configuration provided by the
`env` module.
"""

from env import *

import time
start_time = time.time()

from windbinder.sample_action import SAMPLE_ACTION
from windbinder.minio.login import login_minio
from windbinder.minio.bucket import download_dependent_output, create_bucket
from windbinder.windstorm.authentication import login_windstorm_api
from windbinder.windstorm.thread import update_thread_status, \
    check_thread_dependency, template_render

from windbinder.git.clone import clone, init

def main(action=SAMPLE_ACTION, thread_execution_id=0, prev_thread_name=None):
    """Run the input build flow for a single action.

    Parameters
    - action: identifier of the action/template to build. Defaults to
        `SAMPLE_ACTION` imported from the package.
    - thread_execution_id: numeric id used to update execution status in
        Windstorm for this run.
    - prev_thread_name: optional name of a previous thread whose output this
        action depends on; if provided, the dependent output will be downloaded
        before building.

    The function performs authentication, dependency checks, cloning, rendering,
    and pushes the input archive to object storage. It updates the external
    execution status at key checkpoints so orchestrators can observe progress.
    """

    # Make a MinIO client for accessing object storage
    client = login_minio()

    # Get a token from Windstorm to access the API via OAuth2
    token = login_windstorm_api()

    # Update status to indicate build started
    thread_name = update_thread_status(
        token, thread_execution_id, 'windrunner_1'
    )

    # Check for a dependency on a previous thread and resolve the action
    action, action_prev = check_thread_dependency(action, prev_thread_name)

    # Download the required output from object storage, if necessary
    if action_prev is not None:
        download_dependent_output(client, action_prev, prev_thread_name)

    # Clone the template artifact repository for this action
    repo = clone(action)

    # Render/build the template artifacts for the action
    template_render(action)

    # Package and upload the input archive to object storage
    create_bucket(client, action, thread_name)

    # Initialize a local repository in the attached volume (for runner use)
    repo2 = init()

    print('Input build complete.')

    # Update status
    thread_name = update_thread_status(
        token, thread_execution_id, 'windrunner_2'
    )

if __name__ == "__main__":
    import os
    os.mkdir('tmp')
    # This part is a workaround until volume is attached.
    if not os.path.exists(VOLUME):
        raise NotImplementedError('Volume is not attached.')

    import fire
    fire.Fire(main)
    print("--- %s seconds ---" % (time.time() - start_time))
