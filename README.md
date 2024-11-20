# Cats spying system API project

The Spy Cat Agency (SCA) Management System is a web application designed to streamline the management of spy cat
missions. The system allows users to:

1. Manage Spy Cats: Create, update, view and delete spy cats, each with details like experience, breed, and salary.
2. Create and Manage Missions: Assign missions to spy cats, manage mission details.
3. Target Management: Manage and update targets within missions, including the ability to mark targets as completed.
4. Mission Notes: Add and update notes associated with targets within a mission

## Deploy steps

1. Install [docker](https://docs.docker.com/engine/install/)
2. Fork my repo `git clone https://github.com/senyehor/sca_test_task`
3. Rename `._env` extension to `.env` from `api.production._env` and `db.production._env` *I know it is a crime in production, but it is a sacrifice for you to deploy easily*
4. Just `run docker-compose up`

## Then, you can easily test API using Postman

1. Install Postman [app](https://www.postman.com/downloads/)
2. Play around with my
   Postman [collection](https://elements.getpostman.com/redirect?entityId=39883568-d53d288e-6479-4ea2-9003-aece731f0dd5&entityType=collection)