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

import os

## WINDRUNNER CONFIGURATION VALUES
VOLDEF = "/mnt/vol"
VOLUME = os.environ.get("VOLUME",VOLDEF)

## WINDSTORM VALUES
WINDSTORMAPIHOST = os.environ.get(
    "WINDSTORMAPIHOST",
    "http://windstorm-api-service.windstorm:8000/"
)
WINDSTORMAPICLIENT = os.environ.get("WINDSTORMAPICLIENT","")
WINDSTORMAPISECRET = os.environ.get("WINDSTORMAPISECRET","")

## MINIO VALUES
MINIOHOST = os.environ.get("MINIOHOST","storage-minio.artifacts:9000")
MINIOUSER = os.environ.get("MINIOUSER","CcgP5DINKOfemEXcjYyL")
MINIOTOKEN = os.environ.get("MINIOUSER","YS62HYwroWYozFGoWyeZjYsmGwFLEULu047lquE6")

## ARTIFACT GIT VALUES
GITHOST = os.environ.get("GITHOST","https://configs.digitalforge.app")
