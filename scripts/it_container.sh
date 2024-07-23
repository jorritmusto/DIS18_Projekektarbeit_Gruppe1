#!/bin/sh

docker run -it luigi-pipeline /bin/bash

-e PYTHONPATH=":./tasks"