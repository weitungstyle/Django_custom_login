# HTTP APIs for Account and Password Management

Demo project for Senao Networks Inc.
Written by Python and Django framework.

### Docker hub

[Docker hub](https://hub.docker.com/repository/docker/weitungstyle/senao-victor/general)

### Features

- Sign-up

  User can sign up an account by providing following information:

  - username : 3~32 characters, can't use reapted username
  - password : 8~32 characters, including at least 1 uppercase letter, 1 lowercase letter, and 1 number.

- Sign-in

  After signing up, user can sign in the server.

  - If user continuously attempts to sign in with wrong password (over 5 times/hour), user should wait one minute before attempting to verify the password again.

### Launch Server

1. Make shure that you have installed Install Docker. If it's not already installed, You can download and install Docker from the official website at https://www.docker.com/products/docker-desktop.

2. Open terminal, then pull Docker image from Docker Hub using the docker pull command:

```
docker pull weitungstyle/senao-victor:latest
```

3. Once the image is downloaded, You can run a Docker container using the docker run command:

```
docker run -p 8000:8000 weitungstyle/senao-victor:latest
```

4. The server is successfully running on localhost, if the following message shows:

```
Watching for file changes with StatReloader
```

5. Now, You can use a web browser or Postman application to access API through the following address:
   (user1 to user3 have been registed.)
   http://127.0.0.1:8000/users/signup/
   http://127.0.0.1:8000/users/signin/

### Usage

| HTTP method |      API       |
| :---------: | :------------: |
|    POST     | /users/signup/ |
|    POST     | /users/signin/ |

- The API accept a JSON payload as input and return a JSON payload as output.

  - input format：

    ```
    {
        "username":"user1",
        "password":"Aa12345678"
    }
    ```

  - output format：

  1. If the request is handled correctly, the 'success' field will be returned as true.

  ```
  {
      "success": true
  }
  ```

  2. If the server fails to handle the request, the 'success' field will be returned as false, and the error message will be put in the 'reason' field.

  ```
  {
    "success": false,
    "reason": "Password must be between 8 - 32 characters."
  }
  ```

### Error Code

- Sign Up
  | Error Code | Description |
  | :--------- | :------------ |
  | 200 | Successful. |
  | 400 | Username already exists. |
  | 400 | Username is required. |
  | 400 | Password is required. |
  | 400 | Username cannot be empty. |
  | 400 | Username must be between 3 - 32 characters. |
  | 400 | Password must be between 8 - 32 characters. |
  | 400 | Password must contain at least one uppercase letter. |
  | 400 | Password must contain at least one lowercase letter. |
  | 400 | Password must contain at least one digit. |
  | 400 | Any unexpected error. |
  | 405 | Invalid request method. |

- Sign In
  | Error Code | Description |
  | :--------- | :------------ |
  | 200 | Successful. |
  | 400 | Username and password are required. |
  | 400 | Any unexpected error. |
  | 401 | Invalid username or password. |
  | 423 | Too many failed login attempts. |
  | 405 | Invalid request method. |
