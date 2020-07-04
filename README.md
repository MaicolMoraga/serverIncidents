  **SERVER INCIDENTS IN PYTHON.FLASK WHITH MOCKAPI**

  **Rest API that allows the creation of problems on servers**

    - The entry of problems by the agent is validated with basic
      outh or previously generated token.

    - You can get the list of all registered problems,
      filter by agent, date, sort by date in asc or desc.

    - The creation of new agents is allowed.

    - The creation of new token sesion.

  * The data is saved in mockapi.io in two resources (agent, issue), URL public Mockapi data: https://mockapi.io/clone/5ef62e652c0f2c0016949868.

  **API REST possible responses**

  http://localhost:7000/agent
  - Allows the registration of a new agent.
  - Authentication is not required.
  - Body Json data must contain userName and password parameters).
  - returns in response to success or failure.

  http://localhost:7000/token
  - Returns a token for agent validation on issue entry.
  - Auth:BasicAuth (entering username and password).
  - returns in response to success or failure.

  http://localhost:7000/issue 
  - Allows the entry of a new issue to a previously registered agent.
  - Auth:BasicAuth (entering username and password or validation token). 
  - Body Json data must contain title and descripcion parameters).
  - returns in response to success or failure.

  http://localhost:7000/issues
  - Returns response in json of all the registered issues (return date, title, description and agent).
  - Authentication is not required.

  http://localhost:7000/issues/filter=(name_agent)
  - Returns response in json of all the registered issues specific agent(return date, title, description and agent).
  - Authentication is not required.

  http://localhost:7000/issues/filter=(date_format m-d-y)
  - Returns response in json of all the registered issues specific date(return date, title, description and agent).
  - Authentication is not required.

  http://localhost:7000/issues/orderBy=date&order=(asc or desc)
  - Returns response in json of all the registered issues sorted in ascending or descending order (return date, title, description and agent).
  - Authentication is not required.

  *For more information check the Postman Collection: https://documenter.getpostman.com/view/11862302/T17GdmpL

  **Implementation in a local environment with docker**

  - The file is included with all the steps of the docker process.
  - Go to the directory where the project is located.
  - In console run the following command, make sure you have desktop docker installed and running previously.

    1. docker build -t serverincidents . (generates the api docker image)
    
    2. docker images (to validate if the image is in the docker directory)
    
    3. docker run -it --publish 7000:4000 -d  serverincidents (Run the server in the background with the api image in the 
      port 7000)
      
    4. docker container ls (allows you to see the processes currently running docker, in which the process of our api 
      will be found)
      
    5. docker stop CONTEINER ID (stop the api process in docker, enter the container id shown in the list above)

  **Helpful Links**
  
  ● Docker:  https://www.docker.com/
  
  ● Flask:   https://flask.palletsprojects.com/en/master/
  
  ● Postman: https://learning.postman.com/
  
  ● Mockapi: https://www.mockapi.io/
