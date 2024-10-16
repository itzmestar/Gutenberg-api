# Gutenberg-api

## Introduction

Gutenberg-api is the FastAPI app to search free ebooks from Gutenberg postgresql database.
Note that postgresql database should already be setup in order to run this app.

## Setup

1. Clone the repository

`git clone https://github.com/itzmestar/Gutenberg-api`

2. Change directory

`cd Gutenberg-api`

3. Set these environment variables:

`DB_HOST,
DB_USER,
DB_PASS,
DB_NAME,`

4. Install requirements

`pip3 install -r requirements.txt`

## Run

`uvicorn gutenberg_app.main:app`

## Docker

docker image can be found on the Docker-hub: `itzmetariq/gutenberg-api`
