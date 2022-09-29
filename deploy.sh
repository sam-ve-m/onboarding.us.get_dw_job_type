#!/bin/bash

fission spec init
fission env create --spec --name get-employ-type-env --image nexus.sigame.com.br/fission-env-cx-async:0.0.1 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name get-employ-type-fn --env get-employ-type-env --src "./func/*" --entrypoint main.get_employ_type --executortype newdeploy --maxscale 3
fission route create --spec --name get-employ-type-rt --method GET --url /enum/get_employ_type --function get-employ-type-fn