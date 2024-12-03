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

    # Make a minio client
    client = login_minio()

    # Get a token from windstorm to access the API via oauth
    token = login_windstorm_api()

    # Update status to started
    thread_name = update_thread_status(
        token, thread_execution_id, 'windrunner_1'
    )

    # Check for previous action
    action, action_prev = check_thread_dependency(action, prev_thread_name)

    # Download the required output, if necessary
    if action_prev is not None:
        download_dependent_output(client, action_prev)

    # Clone the template artifact repo
    repo = clone(action)

    # Build the artifacts
    template_render(action)

    # Collect and push a input archive to storage
    create_bucket(client, action, thread_name)

    # Initialize a local repo in the attached volume
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
