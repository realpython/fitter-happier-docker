# Docker in Action - fitter, happier, more productive (continuous delivery)

So, in the last [tutorial](link), we went over a nice development workflow that included continuous integration with [CircleCI](https://circleci.com/) (steps 1 through 6). In this final piece we'll add continuous delivery into the mix (step 7).

1. Code locally on a feature branch
1. Open a pull request on Github against the master branch
1. Run automated tests against the Docker container
1. If the tests pass, manually merge the pull request into master
1. Once merged, the automated tests run again
1. If the second round of tests pass, a build is created on Docker Hub
1. Once the build is created, it's then automatically (err, automagically) deployed to production

## Digital Ocean

To set up Docker on Digital Ocean, create a new [Droplet](https://cloud.digitalocean.com/droplets), and choose "Applications" and then select the Docker Application. Make sure you also set up an SSH key. For help with adding an SSH key, please see [this](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2) tutorial.

Once setup, SSH into the server as the 'root' user:

```sh
$ ssh root@<some_ip_address>
```

Pull the Docker image from Docker Hub, install the requirements, and run the containers:

```sh
$ docker pull mjhea0/fitter-happier-docker
$ pip install -r requirements.txt
$ docker run --name flask -d -p 80:80 mjhea0/fitter-happier-docker
```

> Make sure you replace `mjhea0` with your Docker Hub username.

Sanity check. Navigate to your Droplet's IP address in the browser. You should see, "Hello! This page has been seen 1 times.".

Now, instead of having to SSH into the server and pull down the new image each time we want to deploy, let's automate the process so that once a new build is generated, we pull in the new image and run the containers *automatically*.

## Deploy Script

We can utilize Docker Hub's [webhooks](https://docs.docker.com/docker-hub/repos/#webhooks) to trigger a post request to a URL on our Digital Ocean server. On the server, we then need to have a "listener" setup to trigger a simple bash script:

```sh
docker pull mjhea0/flask-docker-workflow
docker stop flask
docker rm flask
docker run --name flask -d -p 80:80 mjhea0/flask-docker-workflow
```

Here we pull in the new image, remove the currently running container, and then run the new container. It's not exactly *zero-downtime*; it's more like *as-minimal-as-possible-downtime*.

Let's get this set up along with the listener...

## Docker Listener

To set up the listener, we can use a separate Docker container that's already [set up](https://registry.hub.docker.com/u/mjhea0/docker-hook-listener/). You will need to update the code before you can use it, though. So clone the [Github repo](https://github.com/realpython/docker-hook-listener).

Update the *app/deploy.sh* file, replacing `mjhea0` with your Docker Hub username. If you're curious, check out the the Flask app code within *app/app.py*. Essentially, we just confirm that the token is correct when a post request hits the `/ping` endpoint. If it's correct, then the deploy script is fired. Make sense?

After you clone the repo and update the deploy script. Add this repository to Docker Hub, just as you did in the last [tutorial](https://blog.rainforestqa.com/2014-12-08-docker-in-action-from-deployment-to-delivery-part-2-continuous-integration/).

Next, SSH back into Digital Ocean, and then pull the image and run the container (making sure to add the `TOKEN` to the environment with the `-e` flag:

```sh
$ docker pull mjhea0/docker-hook-listener
$ docker run --name listener -e TOKEN="test654321" -d -p 5000:5000 mjhea0/docker-hook-listener
```

> Again, replace `mjhea0` with your Docker Hub username.

With the listener running, add a webhook (under *Settings*) to your Docker build: [http://your-hostname:5000/ping?token=test654321](http://your-hostname:5000/ping?token=test654321).

## Profit!

Now after every single build completes on Docker Hub-

- A post request is sent.
- The listener handles the post request by ensuring that the token is valid and then firing *deploy.sh*.

Time to test. On the feature branch, update the app - Add some cities to the cities list, perhaps. Commit your changes. Open a pull request. Once the automated tests pass, merge the request. After the tests run again, a new build will trigger on Docker Hub. After the build is complete, the post request is sent and handled by the listener, which fires the bash script.

Make sure these changes are reflected in the browser.

## Conclusion

Well, this concludes our look at a powerful Docker workflow - from development to deployment. What's left?

1. Staging server: We need a pre-production server for one last line of tests.
1. Integration tests: Right now we just have some basic unit tests, so make sure to add integration tests.
1. Create a new user: Add a new user to your Linux server so that you're not using 'root'.
1. Tagging: It's a good idea to introduce a system of tagging so that Docker images can be traced back to a commit (and ultimately back to the code).

Thanks for reading!


## Conclusion

Well, this concludes our look at a powerful Docker workflow - from development to deployment. What's left?

1. Staging server: We need a pre-production server for one last line of tests.
1. Integration tests: Right now we just have some basic unit tests, so make sure to add integration tests.
1. Create a new user: Add a new user to your Linux server so that you're not using 'root'.
1. Tagging: It's a good idea to introduce a system of tagging so that Docker images can be traced back to a commit (and ultimately back to the code).

Thanks for reading!
